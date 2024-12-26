
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from business_portal.utils import is_valid_email
from datetime import datetime
from .models import *
from datetime import date


@login_required(login_url='/login/')
def home(request):
    return render(request, 'users/home.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Username and password are required.")

    today = date.today()  
    return render(request, 'users/login.html', {'today': today})



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        zip_code = request.POST.get('zip-code')
        role = request.POST.get('role', 'visitor')
        date_of_birth = request.POST.get('date_of_birth')


        print(username, email, password, confirm_password, zip_code, role, date_of_birth)

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'users/signup.html', {
                'username': username, 
                'email': email, 
                'zip_code': zip_code, 
                'role': role,
                'date_of_birth': date_of_birth
            })

       
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return render(request, 'users/signup.html')

        profile = user.profile  
        profile.zip_code = zip_code
        profile.role = role
        
        profile.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'users/signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful! Please log in.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "No account found with this email address!")

    return render(request, 'users/reset_password.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
    

        messages.success(request, "Your message has been sent successfully!")
        return render(request, 'users/contact.html')

    return render(request, 'users/contact.html')

