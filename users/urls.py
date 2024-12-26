from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('login/', login, name = 'login'),
    path('signup/', signup, name = 'signup'),
    path('reset_password/', reset_password, name = 'reset_password'),
    path('logout/', logout_view, name = 'logout'),
    path('contact/', contact, name = 'contact'),
]