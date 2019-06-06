from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.aboutUs, name="aboutUs"),
    path('contact-us/', views.contactUs, name="contact"),
    path('email/', views.emailView, name='email'),
    path('success/', views.successView, name='success'),
]
