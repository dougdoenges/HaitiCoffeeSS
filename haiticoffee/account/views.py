from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import DatabaseError
from main.models import Address, Customer
import json
import datetime
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NewAddressForm, SigninForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."


@csrf_exempt
@login_required(login_url='/account/signin')
def address(request):
    """
    On GET- returns form to create an address.
    On POST- creates new address for current user.
    """
    try:
        if request.method == 'GET':
            return HttpResponse(render(request, "account/register.html", {'form' : NewAddressForm}), status = 200) 
        elif request.method == 'POST':
            addressData = request.POST
            newAddress = Address(addressLine1 = addressData['addressLine1'],
                                addressLine2 = addressData['addressLine2'],
                                city = addressData['city'],
                                state = addressData['state'],
                                postalCode = addressData['postalCode'],
                                country = addressData['country'])
            newAddress.save()
            currCustomer = Customer.objects.get(user=request.user)
            currCustomer.customerAddress.add(newAddress)
            return HttpResponse('Address created successfully', status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def addressByUser(request):
    """
    On GET- return current user's addresses.
    On PATCH- Updates a users address with data given by user.
    On DELETE- Deletes given address from user profile.
    """
    try:
        if request.method == 'GET':
            currCustomer = Customer.objects.get(user=request.user)
            userAddresses = currCustomer.customerAddress
            userAddresses = list(userAddresses.values())
            return JsonResponse(userAddresses, status=status.HTTP_200_OK, safe=False)
        elif request.method == 'PATCH':
            addressData = json.loads(request.body.decode('utf-8'))

            currAddress = Address.objects.get(id=addressData['id'])
            if not currAddress in Customer.objects.get(user=request.user).customerAddress.all():
                return HttpResponse('You may only edit your own address.', status=status.HTTP_403_FORBIDDEN)
            currAddress.addressLine1 = addressData['addressLine1']
            currAddress.addressLine2 = addressData['addressLine2']
            currAddress.city = addressData['city']
            currAddress.state = addressData['state']
            currAddress.postalCode = addressData['postalCode']
            currAddress.country = addressData['country']
            currAddress.save()
            jsonAddress = list(Address.objects.filter(id=currAddress.id).values())
            return JsonResponse(jsonAddress[0], status=status.HTTP_200_OK, safe=False)
        elif request.method == 'DELETE':
            addressID = json.loads(request.body.decode('utf-8'))
            Address.objects.get(id=addressID['id']).delete()
            return HttpResponse('Deleted address successfully.', status=status.HTTP_200_OK)
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@sensitive_post_parameters('username','password')
@csrf_exempt
def signin(request):
    """
    Render login form on GET request.
    Log in user on POST request.
    """
    if request.user.is_authenticated:
        return HttpResponse("You are already signed in!", status=status.HTTP_200_OK)
    if request.method == 'GET':
        return HttpResponse(render(request, "account/signin.html", {'form' : SigninForm}), status = 200)
    elif request.method == 'POST':
        postdata = request.POST.copy()
        username = postdata.get('username','')
        password = postdata.get('password', '')
        user = authenticate(username = username, password = password)
        if user is not None:
            #print('success')
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid credentials.", status = 401)
    else:
        return HttpResponse("Bad login form.", status = 400)

@sensitive_post_parameters('username','password','passwordconf','email','first_name','last_name')
@csrf_exempt
def register(request):
        """
        Render a new user form on GET request.
        Register new user in database on POST request.
        """
        if request.method == 'GET':
            return HttpResponse(render(request, "account/register.html", {'form' : RegistrationForm}), status = 200)
        elif request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                passwordconf = form.cleaned_data.get('passwordconf')
                email = form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                if(password != passwordconf):
                        return HttpResponse("Passwords did not match.", status=400) 
                user, created = User.objects.get_or_create(username=username, email = email, 
                        first_name = first_name, last_name = last_name)
                user.set_password(password)
                user.save()
                newCustomer = Customer.objects.create(user = user)
                newCustomer.save()
                return HttpResponseRedirect("/account/signin")
            else:
                return HttpResponse("Invalid registration request.", status = 405)
        else:
            return HttpResponse("Method not allowed on /account/register.", status = 405)

@csrf_exempt
def signout(request):
    """
    Signs user out on GET request.
    """
    if request.method == 'GET':
        if (request.user.is_authenticated) :
            logout(request)
            return HttpResponse("Sign out successful", status=200)
        else :
            return HttpResponse("Not logged in", status=200)
    else:
        return HttpResponse("Method not allowed on account/signout.", status = 405)

@csrf_exempt
@login_required(login_url='/account/signin')
def testAdmin(request):
    """
    Turns current user account into Admin account for testing purposes.
    """
    if request.method == "PATCH":
        currCustomer = Customer.objects.get(user=request.user)
        currCustomer.isAdmin = True
        currCustomer.save()
        print(currCustomer)
        return HttpResponse('Your user account now has admin access', status=status.HTTP_200_OK)