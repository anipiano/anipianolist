from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# H/t https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# Why use your own brain when you can use somebody else's

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
		# like ForeignKey but a one-to-one relationship
		# hence model deleted when User is deleted
	pfp = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
	location = models.CharField(default=None, max_length=69, blank=True)
	bio = models.TextField(default=None, max_length=2000, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()