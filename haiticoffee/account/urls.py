from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('create', views.address, name = "createAddress"),
    path('<int:user_id>/address', views.addressByUser, name = 'manageAddress'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('register', views.register, name='register'),
    path('create-an-admin-for-testing', views.testAdmin, name='testAdmin')
]

