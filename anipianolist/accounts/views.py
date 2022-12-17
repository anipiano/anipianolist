from django.shortcuts import render

# Create your views here.

def generic_render(request, pagename):
	context = {}
	return render(request, 'accounts/' + pagename + '.html', context)

def profile(request):
	return generic_render(request, 'profile')

def login(request):
	return generic_render(request, 'login')