from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('<collection_name>/', views.getCollection, name='getCollection'),
    path('', views.getCollection, name='getCollection')
]