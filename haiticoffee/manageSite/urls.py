from django.urls import path, include
from . import views

#this creates path 
app_name = 'products'

urlpatterns = [
    path('', views.manageHome, name="manageHome"),
    path('products/', views.manageProducts, name="manageProducts"),
    path('products/<int:product_id>', views.manageAProduct, name="manageAProduct"),
    path('products/<int:product_id>/images', views.manageProductImages, name="manageProductImages")
]