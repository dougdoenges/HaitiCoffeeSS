from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('<int:collection_id>/', views.getCollection, name='getCollection')
]