from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
#from django_gravatar.helpers import get_gravatar_url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.safestring import mark_safe
import hashlib
from django import template
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

register = template.Library()

@csrf_exempt
def home(request):
    if request.method == 'GET':
        return render(request, 'main/index.html', status=200)
    else:
        return HttpResponse("Method not allowed on /.", status=405)

@csrf_exempt
def aboutUs(request):
    if request.method == 'GET':
        print('1')
        return render(request, 'pages/about-us.html', status=200)
    else:
        return HttpResponse("Method not allowed on /.", status=405)

@csrf_exempt
def contactUs(request):
    if(request.method == 'GET'):
        return render(request, 'pages/contact-us.html', status=200)
    else:
        return HttpResponse("Method not allowed", status=405)

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['justinya07@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Success! Thank you for your message.')
    return render(request, "pages/email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')