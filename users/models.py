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
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    business_phone = models.CharField(max_length=15, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    business_website = models.URLField(blank=True, null=True)
    business_address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.business_name if self.business_name else self.user.username
e

