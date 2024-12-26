from django.urls import path
from .views import *




urlpatterns = [
    path('business_list/', business_list, name = 'business_list'),
    path('business_create/', business_create, name = 'business_create'),
    path('business_registration/', business_registration, name='business_registration'),
    path('business/<int:business_id>/', business_detail, name='business_detail'),
    path('business/<int:business_id>/', business_information, name='business_information'),
]