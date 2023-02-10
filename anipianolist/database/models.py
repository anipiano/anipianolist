from django.db import models
from django_hashids import HashidsField

from django.contrib.auth.models import User
from django.conf import settings
from .language_choices import LANGUAGE_CHOICES

# Create your models here.

class ArrangementEntry(models.Model):

	entry_id = HashidsField(real_field_name="id", editable=False, salt=settings.DJANGO_HASHIDS_SALT, min_length=8) # hash+salted proxy to default `id` AutoField
	title = models.CharField(max_length=100, blank=False)
	youtube_id = models.CharField(max_length=11, blank=True) # todo: custom validator
	bilibili_cn = models.CharField(max_length=12, blank=True)
	bilibili_tv = models.CharField(max_length=10, blank=True)
	creator_id = models.CharField(max_length=100, blank=False)
	instruments = models.CharField(max_length=200, blank=True)

	# Optional fields
	language = models.CharField(max_length=100, blank=True, choices=LANGUAGE_CHOICES)
	track_name_en = models.CharField(max_length=100, blank=True)
	track_name_rom = models.CharField(max_length=100, blank=True)
	track_name_cjk = models.CharField(max_length=100, blank=True)
	track_name = models.CharField(max_length=100, blank=True)
	series_name = models.CharField(max_length=100, blank=True)
	arranger = models.CharField(max_length=100, blank=True)
	original_artist = models.CharField(max_length=100, blank=True)
	upload_date = models.DateTimeField(blank=False)
	sheet_music_url = models.CharField(max_length=420, blank=True)
	internal_notes = models.CharField(max_length=420, blank=True)
	public_notes = models.CharField(max_length=420, blank=True)

	# Tracking
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_modified = models.DateTimeField(auto_now=True, null=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="creator")
	last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="last_editor")
