from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import DatabaseError
from main.models import Address, Customer, Cart, Product, Product_Image
import json
import datetime
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from .forms import NewAddressForm, SigninForm, RegistrationForm, ChangeAddressForm, DeleteAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


def currentCart(request):
    if(request.user.is_authenticated):
        #get all list of carts
        if(request.method == "GET"):
            getCust = Customer.objects.get(user = request.user)
            if(len(Cart.objects.all().values().filter(customer = getCust)) == 0):
                newCartAssigned = Cart.objects.create(customer = getCust, totalPrice = 0.00)
                newCartAssigned.save()
            currCustomer = Customer.objects.get(user=request.user)
            carts = Cart.objects.all().values().filter(customer=currCustomer)
            #print('2')
            cartList = list(carts)
            #print('3')
            return HttpResponse(cartList, status = status.HTTP_200_OK)