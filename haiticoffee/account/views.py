from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import DatabaseError
from main.models import Address, Customer, Order
import json
import datetime
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NewAddressForm, SigninForm, RegistrationForm, ChangeAddressForm, DeleteAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."


@csrf_exempt
@login_required(login_url='/account/signin')
def accountPage(request):
    """
    On GET- return the account page if user is signed in
    """
    try:
        if request.method == "GET":
            currCustomer = Customer.objects.get(user=request.user)
            userAddresses = currCustomer.customerAddress
            userAddresses = list(userAddresses.values())

            ##From Here
            OrderAll = Order.objects.all()
            OrderListss = []

            for eachOrder in OrderAll:
                orderCustomerID = eachOrder.customer.id
                if(orderCustomerID == request.user.id):
                    orderID = eachOrder.id
                    orderDate = (eachOrder.orderDate)
                    orderCust = eachOrder.customer
                    orderStatus = eachOrder.status
                    orderPrice = eachOrder.totalPrice
                    orderProduct = eachOrder.product
                    
                    orderDate = (str(orderDate)[0:10])
                    #print(str(orderDate)[0:10])

                    overallOrder = "OrderID:" + str(orderID) + " Order Date: " + orderDate  + " Order Status:" + orderStatus + " Price:" + str(orderPrice) 
                    OrderListss.append(overallOrder)
            #To Here
            return render(request, "account/account-page.html",
                {'addressDetails': userAddresses, 'orderOverall' : OrderListss}, status=200)
    # except DatabaseError :
    #     return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def address(request):
    """
    On GET- returns form to create an address.
    On POST- creates new address for current user.
    """
    try:
        if request.method == 'GET':
            return HttpResponse(render(request, "account/address/address.html", {'form' : NewAddressForm}), status = 200) 
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
            if request.user.is_authenticated:
                userid = request.user.id
                user = User.objects.get(pk=userid)
                currCustomer = Customer.objects.get(user=request.user)
                userAddresses = currCustomer.customerAddress
                userAddresses = list(userAddresses.values())
            return HttpResponse(render(request, "account/checkAddress.html", {'user' : user, 'address' : userAddresses}), status = 200)
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def deleteAddress(request, address_id):
    """
    On GET- return current user's addresses.
    On PATCH- Updates a users address with data given by user.
    On DELETE- Deletes given address from user profile.
    """
    try:
        if request.user.is_authenticated:
            if request.method == "GET":
                addressID = address_id
                listOfAddressID = []
                for x in Customer.objects.get(user=request.user).customerAddress.all():
                    id = x.id
                    listOfAddressID.append(id)
                intChangedAddressID = int(addressID)
                if not intChangedAddressID in listOfAddressID:
                    return HttpResponse('You may only edit your own address.', status=status.HTTP_403_FORBIDDEN)

                currAddress = Address.objects.get(id=address_id)
                currAddress.delete()
                return HttpResponse('Deleted address successfully.', status=status.HTTP_200_OK)
        else:
            return HttpResponse("Bad login form.", status = 400)
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def changeAddress(request, address_id):
    """
    On GET- return current user's addresses.
    On PATCH- Updates a users address with data given by user.
    On DELETE- Deletes given address from user profile.
    """
    try:
        if request.user.is_authenticated:
            # Get into changeAddress.html 
            if request.method == 'GET':
                currentCustAddress = Customer.objects.get(user = request.user).customerAddress.all()
                if(len(currentCustAddress) == 0):
                    return HttpResponse("You Have Not Putted the Address Yet. Please Visit <a href = https://127.0.0.1:8000/account/create> https://127.0.0.1:8000/account/create</a> to set up", status=status.HTTP_403_FORBIDDEN)
                userid = request.user.id
                user = User.objects.get(pk=userid)
                currCustomer = Customer.objects.get(user=userid)
                userAddresses = currCustomer.customerAddress
                userAddresses = list(userAddresses.values())
                currAddress = Address.objects.get(id=address_id)
                return HttpResponse(render(request, "account/address/changeAddress.html", {'form' : ChangeAddressForm, 'address' : currAddress}), status = 200)
            #Patch Address / Edit ADdress
            elif request.method == 'POST':
                addressData = request.POST
                changedAddressID = address_id

                addressBring = Address.objects.get(id = address_id)
                oldAddressID = addressBring.id
                listOfAddressID = []
                for x in Customer.objects.get(user=request.user).customerAddress.all():
                    id = x.id
                    listOfAddressID.append(id)
                intChangedAddressID = int(changedAddressID)

                #if the ID selected by the user is not owned by the user, throw HttpResponse with the message.
                if not intChangedAddressID in listOfAddressID:
                    return HttpResponse('You may only edit your own address.', status=status.HTTP_403_FORBIDDEN)

                addressBring.addressLine1 = addressData['addressLine1']
                addressBring.addressLine2 = addressData['addressLine2']
                addressBring.city = addressData['city']
                addressBring.state = addressData['state']
                addressBring.postalCode = addressData['postalCode']
                addressBring.country = addressData['country']
                addressBring.save()
                return HttpResponse('Changed address successfully.', status=status.HTTP_200_OK)
        else:
            return HttpResponse("Bad login form.", status = 400)
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
            return HttpResponse("Signed Out!", status =200)
            # return HttpResponseRedirect("account/signin", status=200)
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
    if request.method == "GET":
        currCustomer = Customer.objects.get(user=request.user)
        currCustomer.isAdmin = True
        currCustomer.save()
        print(currCustomer)
        return HttpResponse('Your user account now has admin access', status=status.HTTP_200_OK)


@csrf_exempt
def getAllusers(request):
    if(request.method == "GET"):
        if(not request.user.is_authenticated):
            return HttpResponse("Unauthorized", status = 401)
        else:
            users = User.objects.all().values('id', 'username', 'email')
            userList = list(users)
            return JsonResponse(userList, safe=False, status = status.HTTP_200_OK)


