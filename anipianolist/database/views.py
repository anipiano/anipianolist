from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied, BadRequest
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.timezone import make_aware

from .models import ArrangementEntry
from .forms import CreateEntryForm, ChannelBatchForm

from datetime import datetime
import requests
import json
import re

apikey = settings.GOOGLE_API_KEY

def generic_render(request, pagename, context):
	return render(request, 'cockpit/' + pagename + '.html', context)

def permissions_check(request, group):
	# Admins have access to all pages
	if request.user.groups.filter(name=settings.ADMIN_GROUP).exists():
		return True

	# Moderators and Admins can access Moderator-level pages
	# Admins would have already been caught by the above statement
	if (group == settings.MODERATOR_GROUP) and request.user.groups.filter(name=settings.MODERATOR_GROUP).exists():
		return True

	# Maintainers, Moderators and Admins can access Maintainer-level pages
	if (group == settings.MAINTAINER_GROUP) and request.user.groups.filter(name=(settings.MODERATOR_GROUP or settings.MAINTAINER_GROUP)).exists():
		return True
		
	else:
		return False

	# purewater you are not allowed to bully this code

def cockpit_render(request, pagename, group, context):
	if permissions_check(request, group) == True:
		return generic_render(request, pagename, context)
	else:
		raise PermissionDenied()

@login_required
def arrangements(request):
	arrangement_list = ArrangementEntry.objects.order_by('-date_modified')
	return cockpit_render(request, 'arrangements', settings.MAINTAINER_GROUP, {'arrangement_list': arrangement_list})

@login_required
def channel_check(request):

	# Early pre-emptive error catching to avoid passes through redundant logic (keep it clean!)
	# This looks like a bunch of spaghetti, but essentially we're stepping through a series of tests and requests
	# To help make it easier to explore, comment headings have been added to each stage of the execution process

	### REQUEST NATURE CHECKS ###

	if permissions_check(request, settings.MAINTAINER_GROUP) == False:
		raise PermissionDenied()

	if request.method != 'POST':
		raise BadRequest()

	### FORM VALIDITY CHECK ###

	batch_check_form = ChannelBatchForm(request.POST)

	if not batch_check_form.is_valid():
		messages.error(request, "Oh no! Something went wrong — please correct the issues below :(")
		return redirect('dbms')

	### OPERATIONAL API REQUEST ###

	try:
		params = {
			'part':'about',
			'handle': '@' + batch_check_form.cleaned_data.get('channel_handle'),
			}

		r = requests.get((settings.YOUTUBE_API_INSTANCE + 'channels'), params=params)
		data = r.json()
	except:
		messages.error(request, "We couldn't find that account! Make sure you're typing in the YouTube @handle, not the username.")
		return redirect('dbms')

	### OPERATIONAL API RESPONSE CHECK ###
	
	if not data:
		messages.error(request, "Sorry, but that user could not be found. Please try again with a different username!")
		return redirect('dbms')

	### DATA ASSIGNMENT ###

	youtube_channel_id = data['items'][0]['id']
	youtube_title = data['items'][0]['about']['title']
	youtube_desc = data['items'][0]['about']['description']
	youtube_handle = data['items'][0]['about']['handle']

	### OFFICIAL API REQUEST (for thumbnail) ###

	try:
		# Because the people at Google don't know how to make a damn half-functioning API, we use a self-hosted unofficial API from
		# yt.lemnoslife.com to do things that the YouTube Data v3 API simply can't. Except, we need to use the official API
		# to get thumbnail, so yea we're making two requests LMAO. This API is literally more mid than DENJI DENJI DENJI DENJI DENJI

		pfp_params = {
			'part':'snippet',
			'fields':'items/snippet/thumbnails/medium/url',
			'id':youtube_channel_id,
			'key':apikey
			}

		pfp_r = requests.get('https://www.googleapis.com/youtube/v3/channels', params=pfp_params)
		pfp_data = pfp_r.json()
		youtube_pfp = pfp_data['items'][0]['snippet']['thumbnails']['medium']['url']

	except:
		messages.error(request, "Oh no! Something went wrong during the standard API request and/or JSON decoding. Please contact support for help.")

	return cockpit_render(request, 'channel_check', settings.MAINTAINER_GROUP, {'youtube_channel_id': youtube_channel_id, 'youtube_title': youtube_title, 'youtube_desc': youtube_desc, 'youtube_handle': youtube_handle, 'youtube_pfp': youtube_pfp})

@login_required
def channel_multiadd(request):
	if permissions_check(request, settings.MAINTAINER_GROUP) == False:
		raise PermissionDenied()

	if request.method != 'POST':
		raise BadRequest()

	youtube_channel_id = request.POST.get("youtube_channel_id", "YouTube channel ID not supplied")
	youtube_handle = request.POST.get("youtube_handle", "YouTube handle not supplied")

	if bool(re.match(r"UC[-_0-9A-Za-z]{21}[AQgw]", youtube_channel_id)) == False:
		raise BadRequest()

	youtube_playlist_id = 'UU' + youtube_channel_id[2:]

	multiadd(request, youtube_playlist_id, youtube_handle)

	return redirect('dbms')

def multiadd(request, youtube_playlist_id, youtube_handle, next_page_token="", duplicates=0):

	params = {
		'part':'snippet',
		'playlistId':youtube_playlist_id
	}

	if next_page_token != "":
		params['pageToken'] = next_page_token

	try:
		r = requests.get((settings.YOUTUBE_API_INSTANCE + 'playlistItems'), params=params)
		data = r.json()
	except Exception as e:
		messages.error(request, "Oh no! Something went wrong in the request function >_<. The error was: ", e)
	else:	

		for i in data['items']:

			upload_date = make_aware(datetime.fromtimestamp(i['snippet']['publishedAt']))
			title = i['snippet']['title']
			video_id = i['snippet']['resourceId']['videoId']
			creator_id = youtube_handle[1:]
			created_by = request.user

			try:
				entry = ArrangementEntry(title=title, youtube_id=video_id, upload_date=upload_date, creator_id=creator_id, created_by=created_by)
				entry.save()

			except IntegrityError: # youtube_id is unique=True
				duplicates += 1;

		try:
			multiadd(request, youtube_playlist_id, youtube_handle, data['nextPageToken'], duplicates);
			# api won't return any nextPageToken if it's the last page :)
		except:	
			messages.success(request, "Nice stuff! Seems like everything went smoothly and " + youtube_handle + " has been added to the database. " + str(duplicates) + " entries with duplicate video IDs or errors weren't added (you can find more info about these in the Event Log).")

	# todo: 
	# - batch delete
	# https://yt.lemnoslife.com/playlistItems?part=snippet&playlistId=UUnXp_AxmNywJJlnIc46QWwg

@login_required
def cockpit(request):
	return cockpit_render(request, 'cockpit', settings.MAINTAINER_GROUP, {})

@login_required
def dbms(request):
	if permissions_check(request, settings.MAINTAINER_GROUP) == False:
		raise PermissionDenied()

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
			messages.error(request, "Oh no! Something went wrong — please correct the issues below :(")

	else:
		entry_form = CreateEntryForm(instance=request.user)

	channel_batch_form = ChannelBatchForm()

	return generic_render(request, 'dbms', {'entry_form': entry_form, 'arrangement_list': arrangement_list, 'apikey': apikey, 'channel_batch_form': channel_batch_form})

@login_required
def delete(request, entry_id):
	if permissions_check(request, settings.MAINTAINER_GROUP) == False:
		raise PermissionDenied()

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
def iam(request):
	return cockpit_render(request, 'iam', settings.ADMIN_GROUP, {})

@login_required
def log(request):
	return cockpit_render(request, 'log', settings.MODERATOR_GROUP, {})

@login_required
def modify(request, entry_id):
	if permissions_check(request, settings.MAINTAINER_GROUP) == False:
		raise PermissionDenied()

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

	return generic_render(request, 'modify', {'entry': entry, 'entry_form': entry_form, 'entry_id': entry_id})
