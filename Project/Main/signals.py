from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ApiKey

@receiver(post_save, sender=User)
def create_api_key_for_new_user(sender, instance, created, **kwargs):
    if created:
        api_key = ApiKey().generate_key(instance.id)
        ApiKey.objects.create(user=instance, key=api_key, visible=False)
        print(f'Apikey {api_key} has been created for {instance.id}!')