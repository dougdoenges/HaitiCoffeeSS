from django.contrib import admin
from django.urls import path, include
from . import views

#this creates path 
app_name = 'products'

urlpatterns = [
    path('<int:product_id>', views.getProduct, name="getProduct"),
    path('<int:product_id>/purchase', views.buyProduct, name="buyProduct"),
    path('delete', views.delete, name = "deleteProducts"),
    path('create', views.createProducts, name = "createProducts"),
    path('change', views.changeProduct, name = "changeProducts"),
    path('', views.products, name="products"),
    path('<int:product_id>/manage-images', views.manageProductImages, name='manageProductImages'),
    path('<int:product_id>/images', views.getProductImages, name='getProductImages'),
    path('<int:product_id>/order', views.orders, name = "orderProduct")
]
