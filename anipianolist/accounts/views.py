from django.shortcuts import render, redirect

# Create your views here.

def generic_render(request, pagename):
	context = {}
	return render(request, 'accounts/' + pagename + '.html', context)

def profile(request):
	return generic_render(request, 'profile')

def login(request):
	if request.user.is_authenticated:
		return redirect(profile)
	else:
		return generic_render(request, 'login')