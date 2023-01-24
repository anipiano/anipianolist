from django import forms

from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=150, label="Username", required=True)

	class Meta:
		model = User
		fields = ['username']

class ProfileForm(forms.ModelForm):
	pfp = forms.ImageField(label="Profile picture", required=False, widget=forms.FileInput) # Django ImageField automatically handles image verification, naisu! https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ImageField
	location = forms.CharField(max_length=69, label="Location", required=False)
	bio = forms.CharField(max_length=2000, label="About", widget=forms.Textarea, required=False)

	class Meta:
		model = Profile
		fields = ['pfp', 'location', 'bio']