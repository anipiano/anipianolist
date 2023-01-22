from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.contrib.auth.models import User
from .models import Profile
from .forms import UserForm, ProfileForm

def generic_render(request, pagename):
	context = {}
	return render(request, 'accounts/' + pagename + '.html', context)

def account_login_redirect(request):
	return redirect(login)

def profile(request):
	return generic_render(request, 'profile')

def login(request):
	if request.user.is_authenticated:
		return redirect(profile)
	else:
		return generic_render(request, 'login')

@login_required
def settings(request):
	profile = Profile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, "Your profile was successfully updated to publicly reveal your true love for mayo pizza, naisu~!")
			return HttpResponseRedirect('/naisu/')
		else:
			messages.error(request, "Something went wrong :(")
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	
	return render(request, 'accounts/settings.html', {'user_form': user_form, 'profile_form': profile_form})

def user(request, username):
	if User.objects.filter(username=username).exists():
		context = {
			'user': username
		}
		return render(request, 'accounts/user.html', context)
	else:
		raise Http404()