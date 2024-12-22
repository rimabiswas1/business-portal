
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def home(request):
    return render(request, 'users/home.html')


# users/views.py


def login(request):
    # Redirect if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')  # Change 'home' to your actual home route

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')  # Change 'home' to your actual home route
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Username and password are required.")

    return render(request, 'users/login.html')



# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         zip_code = request.POST.get('zip_code')

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match!")
#         else:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username already exists!")
#             elif User.objects.filter(email=email).exists():
#                 messages.error(request, "Email already exists!")
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()
#                 messages.success(request, "Account created successfully!")
#                 return redirect('login')

#     return render(request, 'users/signup.html')





def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        zip_code = request.POST.get('zip_code')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            # Check if username or email exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
            else:
                # Use geopy to get location based on zip code
                geolocator = Nominatim(user_agent="myApp")
                location = geolocator.geocode(zip_code)
                latitude = location.latitude if location else None
                longitude = location.longitude if location else None

                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Optionally save location data in the user's profile model
                # profile = user.profile
                # profile.latitude = latitude
                # profile.longitude = longitude
                # profile.save()

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

