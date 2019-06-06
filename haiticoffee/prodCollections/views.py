from django.shortcuts import render
from main.models import Product, Product_Image, Collection
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."

# Create your views here.
def getCollection(request, collection_id):
    try:
        if request.method == "GET":
            collectionDetails = Collection.objects.get(id=collection_id)
            collectionProducts = Product.objects.filter(productCollection=collectionDetails).values()
            collectionList = list(collectionProducts)
            for product in collectionList:
                productObj = Product.objects.get(id=product['id'])
                product['productImages'] = list(Product_Image.objects.filter(product=productObj).values())
            allCollections = list(Collection.objects.all().values())
            return HttpResponse(render(request, 'prodCollections/collection.html',
                {'collectionDetails': collectionDetails, 'productDetails': collectionList,
                 'allCollections': allCollections}), status=200)

    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)