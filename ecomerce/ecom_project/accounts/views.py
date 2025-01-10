from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        
        user_obj = authenticate(username = email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpass')

        if not first_name or not last_name or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required!')
            return HttpResponseRedirect(request.path_info)
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.warning(request, 'Email has been sent !')

    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        profile = Profile.objects.get(email_token=email_token)
        profile.is_email_verified = True
        profile.save()
        messages.warning(request, 'Profile Activated !')

        return redirect('/accounts/login')
    except Exception as e:  
        return HttpResponse('Invalid token')  
    