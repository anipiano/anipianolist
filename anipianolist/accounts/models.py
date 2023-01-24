from django.db import models
from django.contrib.auth.models import User

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'anipianolist')))

from anipianolist.validators import validate_file_size 

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
		# This extends on top of the default Django user model
		# like ForeignKey but a one-to-one relationship
		# hence model deleted when User is deleted
	pfp = models.ImageField(default='pfp/default.jpg', upload_to='pfp/%Y/%m/%d/', null=True, validators=[validate_file_size])
	location = models.CharField(default=None, max_length=69, null=True)
	bio = models.TextField(default=None, max_length=2000, null=True)

"""
* In admin centre and the database, there will be blank fields such as First Name, Last Name and Email.
* To get rid of these, we would need to use an AbstractUser custom User model, as opposed to the default Django user model.
* Access this model like `request.user.profile.location`
* There is *very minimal* gain from trying to setting up a custom user model for quite a lot of time cost (especially with integrating it into OAuth2), so we're just going to close our eyes and pretend those fields don't exist :D
* The end user experience is virtually the same because of how we're handling authentication ourselves using a simplified manual process.
* The equivalent analogy would be leaving out that one note in a chord because the same note is already being played on another register X_X
* https://en.wikipedia.org/wiki/Ostrich_algorithm
* https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
"""