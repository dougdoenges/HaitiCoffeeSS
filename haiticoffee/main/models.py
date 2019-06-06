from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model) :
    addressLine1 = models.CharField('addressLine1', max_length=250)
    addressLine2 = models.CharField('addressLine2', max_length=250, blank=True, null=True)
    city = models.CharField('city', max_length=250)
    state = models.CharField('state', max_length=30)
    postalCode = models.CharField('postalCode', max_length=10)
    country = models.CharField('country', max_length=250, default='United States')
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customerAddress = models.ManyToManyField(Address)
    isAdmin = models.BooleanField('isAdmin', default=False)
    isVendor = models.BooleanField('isVendor', default=False)
    isFarmer = models.BooleanField('isFarmer', default=False)

class Collection(models.Model):
    collectionName = models.CharField('collectionName', max_length=250, unique=True)
    collectionDescription = models.CharField('collectionDescription', max_length=500)
    
class Product(models.Model):
    productName = models.CharField('productName', max_length = 250, unique = True)
    productDescription = models.TextField('productDescription')
    productPrice = models.DecimalField('productPrice', max_digits=5, decimal_places=2)
    productCollection = models.ForeignKey('collection', Collection)
    productSrc = models.CharField

class Order(models.Model):
    statusChoices = (
        ('UNFULFILLED', 'Unfulfilled'),
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('FULFILLED', 'Fulfilled')
    )
    customer = models.ForeignKey('customer', Customer)
    orderDate = models.DateTimeField('orderDate', auto_now_add = True)
    status = models.TextField('status', max_length = 250, default = 'UNFULFILLED')
    totalPrice = models.DecimalField('totalPrice', max_digits=5, decimal_places=2)
    product = models.ForeignKey('product', Product)

class Product_Image(models.Model) :
    product = models.ForeignKey('product', Product)
    img = models.ImageField('img', upload_to='static/staticfiles/img/', blank=True, null=True)
    uploadedAt = models.DateTimeField(auto_now_add=True)