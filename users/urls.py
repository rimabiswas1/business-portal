from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name = 'home'),
    path('login/', login, name = 'login'),
    path('signup/', signup, name = 'signup'),
    path('reset_password/', reset_password, name = 'reset_password'),
    path('logout_view/', logout_view, name = 'logout_view'),
]