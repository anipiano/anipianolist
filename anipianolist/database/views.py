from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext

from .models import ArrangementEntry
from .forms import CreateEntryForm

def generic_render(request, pagename, context):
	return render(request, 'cockpit/' + pagename + '.html', context)

def cockpit_render(request, pagename, group, context):
	# Admins have access to all pages
	if request.user.groups.filter(name=settings.ADMIN_GROUP).exists():
		return generic_render(request, pagename, context)

	# Moderators and Admins can access Moderator-level pages
	# Admins would have already been caught by the above statement
	if (group == settings.MODERATOR_GROUP) and request.user.groups.filter(name=settings.MODERATOR_GROUP).exists():
		return generic_render(request, pagename, context)

	# Maintainers, Moderators and Admins can access Maintainer-level pages
	if (group == settings.MAINTAINER_GROUP) and request.user.groups.filter(name=(settings.MODERATOR_GROUP or settings.MAINTAINER_GROUP)).exists():
		return generic_render(request, pagename, context)
	else:
		raise PermissionDenied()

	# purewater you are not allowed to bully this code

@login_required
def dbms(request):
	arrangement_list = ArrangementEntry.objects.order_by('-date_modified')[:10]

	if request.method == 'POST':
		entry_form = CreateEntryForm(request.POST)

		if entry_form.is_valid():
			stage_entry = entry_form.save(commit=False)
			stage_entry.created_by = request.user
			stage_entry.save()
			messages.success(request, "Naisu~! Operation completed!!")
			return redirect('dbms')
		else:
			messages.error(request, "Oh no! Something went wrong  — please correct the issues below :(")

	else:
		entry_form = CreateEntryForm(instance=request.user)

	return cockpit_render(request, 'dbms', settings.MAINTAINER_GROUP, {'entry_form': entry_form, 'arrangement_list': arrangement_list})

@login_required
def modify(request, entry_id):
	try:
		ArrangementEntry.objects.get(entry_id=entry_id)
	except:
		raise Http404()

	entry = ArrangementEntry.objects.get(entry_id=entry_id)

	if request.method == 'POST':
		entry_form = CreateEntryForm(request.POST, instance=entry)

		if entry_form.is_valid():
			stage_entry = entry_form.save(commit=False)
			stage_entry.last_modified_by = request.user
			messages.success(request, "Naisu~! Operation completed!!")
			stage_entry.save()
			return redirect('modify', entry_id)
		else:
			messages.error(request, "Oh no! Something went wrong  — please correct the issues below :(")
			
	else:
		entry_form = CreateEntryForm(instance=entry)

	return cockpit_render(request, 'modify', settings.MAINTAINER_GROUP, {'entry': entry, 'entry_form': entry_form, 'entry_id': entry_id})

@login_required
def delete(request, entry_id):
	try:
		ArrangementEntry.objects.get(entry_id=entry_id)
	except:
		raise Http404()

	entry = ArrangementEntry.objects.get(entry_id=entry_id)

	if request.method == 'POST':
		try:
			entry.delete()
			messages.success(request, "Entry has been deleted... bai bai (*￣Ｏ￣)ノ")
			return redirect('arrangements')
		except:
			messages.error(request, "Oh no! Something went wrong while trying to delete this entry. Please contact support >_<")

	raise Http404()


@login_required
def arrangements(request):
	arrangement_list = ArrangementEntry.objects.order_by('-date_modified')
	return cockpit_render(request, 'arrangements', settings.MAINTAINER_GROUP, {'arrangement_list': arrangement_list})

@login_required
def cockpit(request):
	return cockpit_render(request, 'cockpit', settings.MAINTAINER_GROUP, {})

@login_required
def log(request):
	return cockpit_render(request, 'log', settings.MODERATOR_GROUP, {})

@login_required
def iam(request):
	return cockpit_render(request, 'iam', settings.ADMIN_GROUP, {})