from django.urls import path, include
from . import views

#this creates path 
app_name = 'manage-site'

urlpatterns = [
    path('', views.manageHome, name="manageHome"),
    path('products/', views.manageProducts, name="manageProducts"),
    path('products/create/', views.createProduct, name="createProduct"),
    path('products/<int:product_id>/', views.manageAProduct, name="manageAProduct"),
    path('products/<int:product_id>/delete', views.deleteProduct, name="deleteProduct"),
    path('products/<int:product_id>/images/', views.manageProductImages, name="manageProductImages"),
    path('products/<int:product_id>/images/delete/<int:image_id>/', views.deleteAProductImage, name="deleteAProductImage"),

    path('collections/', views.manageCollections, name="manageCollections"),
    path('collections/create/', views.createACollection, name="createACollection"),
    path('collections/<int:collection_id>/', views.manageACollection, name="manageACollection"),
    path('collections/<int:collection_id>/delete/', views.deleteCollection, name="deleteCollection"),

    path('orders/', views.manageOrders, name="manageOrders"),
    path('orders/<int:order_id>/', views.manageAnOrder, name="manageAnOrder")
]