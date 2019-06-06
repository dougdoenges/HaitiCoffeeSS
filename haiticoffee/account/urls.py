from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.accountPage, name = "accountPage"),
    path('address/create', views.address, name = "createAddress"),
    path('myaddress', views.addressByUser, name = 'manageAddress'),
    path('address/delete/<int:address_id>', views.deleteAddress, name = "deleteAddress"),
    path('address/edit/<int:address_id>', views.changeAddress, name = "changeaddress"),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('register', views.register, name='register'),
    path('create-an-admin-for-testing', views.testAdmin, name='testAdmin'),
    path('getusers', views.getAllusers, name = "getallUsers"),
    
]

