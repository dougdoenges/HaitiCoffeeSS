from django.shortcuts import render
from main.models import Product, Product_Image, Customer, Collection, Order
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import DatabaseError
from manageSite.forms import ChangeProductForm, AddImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
@login_required(login_url='/account/signin')
def manageHome(request):
    try:
        if not Customer.objects.get(user=request.user).isAdmin:
            return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            return HttpResponse(render(request, "manageSite/manageHome.html"), status = 200)
        else:
            return HttpResponse("Method not allowed.", status=405)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def manageProducts(request):
    try:
        if not Customer.objects.get(user=request.user).isAdmin:
            return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            productDetails = Product.objects.all()
            productDetails = list(productDetails.values())
            return HttpResponse(render(request, 'manageSite/manageProducts.html', 
                {'productDetails': productDetails}), status=200)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def manageAProduct(request, product_id):
    try:
        if not Customer.objects.get(user=request.user).isAdmin:
            return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            currProduct = Product.objects.get(id=product_id)
            return HttpResponse(render(request, 'manageSite/manageAProduct.html', 
                    {'product': currProduct, 'form': ChangeProductForm }), status=200)
        elif request.method == "POST":
            productData = request.POST
            productImage = request.FILES

            allCollection = Collection.objects.all()

            listOfName = []
            for collection in allCollection:
                listOfName.append(collection.collectionName)

            if (productData['productCollection'] not in listOfName):
                Collection.objects.create(collectionName = productData['productCollection'])
                currCollection = Collection.objects.get(collectionName=productData['productCollection'])
            else:
                currCollection = Collection.objects.get(collectionName=productData['productCollection'])

            getProduct = Product.objects.get(id = product_id)
            getProduct.productName = productData['productName']
            getProduct.productDescription = productData['productDescription']
            getProduct.productPrice = productData['productPrice']
            getProduct.productCollection = currCollection
            getProduct.save()

            if productImage:
                addImageToProduct(productImage['productImage'], getProduct)

            return HttpResponse('Product Changed successfully', status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def manageProductImages(request, product_id):
    try:
        if not Customer.objects.get(user=request.user).isAdmin:
            return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            currProduct = Product.objects.get(id=product_id)
            currImages = Product_Image.objects.filter(product=currProduct)
            currImages = list(currImages.values())
            return HttpResponse(render(request, "manageSite/manageProductImages.html",
                            {'form' : AddImageForm, 'images': currImages}), status = 200)
        elif request.method == "POST":
            currProduct = Product.objects.get(id=product_id)
            addImageToProduct(request.FILES['newImage'], currProduct)
            return HttpResponse('Added image to product', status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            imageData = json.loads(request.body.decode('utf-8'))
            Product_Image.objects.get(id=imageData['id']).delete()
            return HttpResponse('Deleted Image successfully.')
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)


def addImageToProduct(imageData, product):
    newImage = Product_Image(
        product = product,
        img = imageData
    )
    newImage.save()