from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(f"CREATING A PROFILE FOR USER - {instance}")
    if created:
        new_profile = UserProfile.objects.create(user=instance)
        print(f"CREATE PROFILE: {new_profile}")



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    