from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPES = [
        ('visitor', 'Visitor'),
        ('writer', 'Writer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='visitor')
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)  # Optional field for additional roles
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # Automatically sets on creation

    def __str__(self):
        return self.user.username
    

class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


 
