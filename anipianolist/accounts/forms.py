from django import forms

from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=150, label="Username", required=True, error_messages={'invalid':'Your username can only contain letters, numbers, periods, hyphens or underscores, baka!'})

	class Meta:
		model = User
		fields = ['username']

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		username = cleaned_data.get('username')
		if ('@') in username:
			self.add_error('username', 'Sorry, the @ symbol cannot be used.')
		if ('+') in username:
			self.add_error('username', 'Sorry, the + symbol cannot be used.')
		return cleaned_data

class ProfileForm(forms.ModelForm):
	pfp = forms.ImageField(label="Profile picture", required=False, widget=forms.FileInput) # Django ImageField automatically handles image verification, naisu! https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ImageField
	location = forms.CharField(max_length=69, label="Location", required=False)
	bio = forms.CharField(max_length=2000, label="About", widget=forms.Textarea, required=False)

	class Meta:
		model = Profile
		fields = ['pfp', 'location', 'bio']