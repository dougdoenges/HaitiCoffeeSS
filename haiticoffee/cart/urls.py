from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.currentCart, name = "cart"),
    # path('myaddress', views.addressByUser, name = 'manageAddress'),
    # path('delete', views.deleteAddress, name = "deleteAddress"),
    # path('change', views.changeAddress, name = "changeaddress"),
    # path('signin', views.signin, name='signin'),
    # path('signout', views.signout, name='signout'),
    # path('register', views.register, name='register'),
    # path('create-an-admin-for-testing', views.testAdmin, name='testAdmin'),
    # path('getusers', views.getAllusers, name = "getallUsers"),
    
]

