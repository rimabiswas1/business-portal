from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
    
class Rating(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='ratings')
    review = models.TextField(blank=True, null=True)
    rating_value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  
    date_added = models.DateTimeField(auto_now_add=True)
    deals = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Rating for {self.business.business_name} - {self.rating_value}"

    class Meta:
        ordering = ['-date_added']




 
