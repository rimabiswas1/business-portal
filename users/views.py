
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
# Create your views here.

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
        print(username , email, password, confirm_password, zip_code, role, date_of_birth, )
        


       
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

       
        try:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None
            if date_of_birth:
               
                today = datetime.today().date()
                age = today.year - date_of_birth.year
                if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
                    age -= 1
                if age < 21:
                    messages.error(request, "You must be at least 21 years old to register.")
                    return redirect('signup')
        except ValueError:
            messages.error(request, "Invalid date of birth format!")
            return redirect('signup')

        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

       
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'zip_code': zip_code,
                'role': role,
                'date_of_birth': date_of_birth,
                'user_type': role,
            }
        )
        if not created:
            messages.error(request, "Profile already exists for this user.")
            return redirect('signup')

        messages.success(request, "Account created successfully!")
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

