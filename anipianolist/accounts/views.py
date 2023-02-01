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

@login_required
def account_deletion(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.user.username)
			user.delete()
			messages.success(request, "Your account has been deleted. Bai bai~")
		except:
			messages.error(request, "Something went wrong while trying to delete your account. Please contact support >_<")
		return redirect('/')
	else:
		return generic_render(request, 'account-deletion')

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
			messages.success(request, "Naisu~! Your profile was successfully updated (to publicly reveal your true love for mayo pizza).")
			return HttpResponseRedirect('/settings/')
		else:
			messages.error(request, "Oh no! Something went wrong while trying to update your user settings — please correct the issues below :(")
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	
	return render(request, 'accounts/settings.html', {'user_form': user_form, 'profile_form': profile_form})

def user(request, username):
	if User.objects.filter(username=username).exists():
		context = {
			'profilename': username
		}
		return render(request, 'accounts/user.html', context)
	else:
		raise Http404()