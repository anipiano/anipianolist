from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied

def cockpit_render(request, pagename, group):
	if request.user.groups.filter(name=group).exists():
		return cockpit_render(request, pagename)
	else:
		raise PermissionDenied()

@login_required
def dbms(request):
	return cockpit_render(request, 'dbms', settings.MAINTAINER_GROUP)

@login_required
def log(request):
	return cockpit_render(request, 'log', settings.MODERATOR_GROUP)

@login_required
def iam(request):
	return cockpit_render(request, 'iam', settings.ADMIN_GROUP)