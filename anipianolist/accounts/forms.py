from django import forms

from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "Username",
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("This field is required.")

        if not username.isalnum() or any(
            char
            not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
            for char in username
        ):
            raise forms.ValidationError(
                "Your username can only contain letters, numbers, periods, hyphens or underscores."
            )

        if "@" in username or "+" in username:
            raise forms.ValidationError("Your username cannot contain '@' or '+'.")

        return username


class ProfileForm(forms.ModelForm):
    pfp = forms.ImageField(
        label="Profile picture", required=False, widget=forms.FileInput
    )  # Django ImageField automatically handles image verification, naisu! https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ImageField
    location = forms.CharField(max_length=69, label="Location", required=False)
    bio = forms.CharField(
        max_length=2000, label="About", widget=forms.Textarea, required=False
    )

    class Meta:
        model = Profile
        fields = ["pfp", "location", "bio"]
