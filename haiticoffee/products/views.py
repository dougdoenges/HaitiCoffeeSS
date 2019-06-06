from django.shortcuts import render
from main.models import Product, Product_Image, Customer, Collection, Order
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import DatabaseError
from products.forms import NewProductForm, AddImageForm, purchaseProductForm, ChangeProductForm, DeleteProductForm
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup  
import pandas as pd  
import requests 
import re
import datetime



JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."


def webScrapeData(): 
    #print('ASDASDASDASDSA')
    r2 = requests.get('https://www.haiticoffee.com/collections/all')
    soup2 = BeautifulSoup(r2.text, 'html.parser') 
    results = soup2.find_all('div', {'class': 'card bg-white product-card-light'})
    record = []
    for eachResult in results:
        name = eachResult.find('p').text
        price = eachResult.find('span', {'class': 'product-price__price'}).text
        record.append((name,price))
    df = pd.DataFrame(record, columns=['name', 'price'])
    return df 


def insertScrapeData():
    listOfScrape = webScrapeData()
    getCollect = Collection.objects.get(collectionName = 'all')
    #print(getCollect.id)
    for x in range(len(listOfScrape)):
        name = (listOfScrape.iloc[x]['name'])
        price = (listOfScrape.iloc[x]['price'])[1:]
        doublePrice = float(price)

        newProduct = Product.objects.create(productName = name, productDescription = name, productPrice = doublePrice, productCollection = getCollect)
        
#Product Scraped
#insertScrapeData()

        


def getProduct(request, product_id):
    # GET to return the product page
    try:
        if request.method == "GET":
            currProduct = Product.objects.get(id=product_id)
            # currProductImages = Product_Image.objects.filter(product=currProduct).values()
            # #currProduct = list(currProduct)
            # if(len(currProductImages) is not 0):
            #     currProduct['productImages'] = currProductImages
            return render(request, 'products/product-page.html', 
                {'productDetails': currProduct}, status=200)
        else:
            return HttpResponse("Method not allowed.", status=405)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/account/signin') # populate this with the login url
def buyProduct(request, product_id):
    """
    On GET- return purchase form
    On POST- complete order and post order to customers orders
    """
    try:
        if request.method == "GET":
            currProduct = Product.objects.get(id=product_id)
            return render(request, 'products/purchase-product.html',
                {'form': purchaseProductForm, 'productInfo': currProduct}, status=200)
        elif request.method == "POST":
            # Create the order on the user profile
            now = datetime.datetime.now()
            price = Product.objects.get(id = product_id)
            newOrder = Order.objects.create(customer = request.user, orderDate = now, totalPrice = price, product = product_id)
            newOrder.save()
            print(newOrder)
            return HttpResponse("Order Successfully Made!", status = 405)

            # We should have products in a completed order stored in the order table
                # If a product is deleted or price is change, we shouldn't change the details
                # of a completed order.
        else:
            return HttpResponse("Method not allowed.", status=405)

    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
# Admin Needed 
@csrf_exempt
@login_required(login_url='/account/signin')
def createProducts(request):
    """
    On GET- returns form to create new product
    On POST- creates a new product with form input.
    On PATCH- changes specified product details with data given by user.
    On DELETE- deletes product given by user.
    """
    try :
        # if not Customer.objects.get(user=request.user).isAdmin:
        #     return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET" :
            return HttpResponse(render(request, "products/create-a-product.html", 
                                {'form' : NewProductForm}), status = 200)
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
            
            newProduct = Product(
                productName = productData['productName'],
                productDescription = productData['productDescription'],
                productPrice = productData['productPrice'],
                productCollection = currCollection
            )
            newProduct.save()

            if productImage:
                addImageToProduct(productImage['productImage'], newProduct)
            return HttpResponse('Product created successfully', status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def changeProduct(request):
    try :
        # if not Customer.objects.get(user=request.user).isAdmin:
        #     return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET" :
            return HttpResponse(render(request, "products/change-a-product.html", 
                                {'form' : ChangeProductForm}), status = 200)
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

            getProduct = Product.objects.get(id = productData['productID'])
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
def delete(request):
    try :
        # if not Customer.objects.get(user=request.user).isAdmin:
        #     return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET" :
            return HttpResponse(render(request, "products/delete-a-product.html", 
                                {'form' : DeleteProductForm}), status = 200)
        elif request.method == "POST":
            productData = request.POST
            getProduct = Product.objects.get(id = productData['productID'])
            print(getProduct.id, getProduct.productName)
            try:
                getProduct.delete()
            except:
                HttpResponse('You Cannot Delete This', status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse('Product Deleted successfully', status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@login_required(login_url='/account/signin')
def products(request):
    try:
        if request.method == "GET":
            productObjs = Product.objects.all().values()
            productList = list(productObjs)
            for product in productList:
                productObj = Product.objects.get(id=product['id'])
                product['productImages'] = list(Product_Image.objects.filter(product=productObj).values())
            return JsonResponse(productList, safe=False, status=status.HTTP_200_OK)
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/account/signin')
def orders(request, product_id):
    try:
        if request.method == "GET":
            getProduct = Product.objects.get(id = product_id)
            getTotalPrice = getProduct.productPrice
            getCustomer = Customer.objects.get(id = request.user.id)
            newOrder = Order.objects.create(customer = getCustomer, orderDate = datetime.datetime.now(), status = "Order Received", totalPrice = getTotalPrice, product = getProduct)
            newOrder.save()
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

                    overallOrder = "OrderID:" + str(orderID) + " Order Date: " + orderDate + " Order Customer:" + str(orderCust) + " Order Status:" + orderStatus + " Price:" + str(orderPrice) + " Product:" + str(orderProduct) 
                    OrderListss.append(overallOrder)
                    
            return HttpResponse(render(request, 'products/orderList.html', {'orderOverall' : OrderListss}), status = 200)
            # return HttpResponse(render(request, 'products/orderList.html', {'orderID' : orderID, 'orderDate' : orderDate, 'orderCust':orderCust, 'orderStatus':orderStatus, 'orderPrice':orderPrice, 'orderProduct':orderProduct}), status = 200)
            
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    # except Exception :
    #     return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@login_required(login_url = "/account/signin")
def manageProductImages(request, product_id):
    try:
        # if not Customer.objects.get(user=request.user).isAdmin:
        #     return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        currProduct = Product.objects.get(id=product_id)
        if request.method == "GET":
            return HttpResponse(render(request, "products/add-an-image.html", 
                            {'form' : AddImageForm}), status = 200)
        elif request.method == "POST":
            addImageToProduct(request.FILES['newImage'], currProduct)
            return HttpResponse('Added image to product', status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            imageData = json.loads(request.body.decode('utf-8'))
            Product_Image.objects.get(id=imageData['id']).delete()
            return HttpResponse('Deleted Image successfully.')
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def getProductImages(request, product_id):
    """
    On GET- Returns images for product which is taken as a parameter
    """
    try:
        currProduct = Product.objects.get(id=product_id)
        if request.method == "GET":
            images = Product_Image.objects.filter(product=currProduct).values()
            images = list(images)
            return JsonResponse(images, safe=False, status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)


def addImageToProduct(imageData, product):
    newImage = Product_Image(
        product = product,
        img = imageData
    )
    newImage.save()