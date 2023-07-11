from django.db import models
from django_hashids import HashidsField

from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator, URLValidator

from .language_choices import LANGUAGE_CHOICES

# Create your models here.

class ArrangementEntry(models.Model):

	alphanumeric = RegexValidator(r'^[0-9a-zA-Z\.\-\_]*$', 'A YouTube handle can only contain letters, numbers, periods, hyphens or underscores, baka!')
	bilibili_cn_validator = RegexValidator(r'BV[0-9A-Za-z]+$', 'Bilibili.com video IDs must be alphanumeric and start with BV ( ´△｀)')
	bilibili_tv_validator = RegexValidator(r'[0-9]+$', 'Bilibili.tv video IDs must be numeric ( ´△｀)')
	validate_url = URLValidator('That isn\'t a valid URL! ʕ•́ᴥ•̀ʔっ♡')

	def length_validator(n):
		return MinLengthValidator(n, 'This video ID must be ' + str(n) + ' characters long!')

	entry_id = HashidsField(real_field_name="id", editable=False, salt=settings.DJANGO_HASHIDS_SALT, min_length=8) # hash+salted proxy to default `id` AutoField
	title = models.CharField(max_length=100, blank=False)
	youtube_id = models.SlugField(max_length=11, validators=[length_validator(11)], blank=True, unique=True)
	bilibili_cn = models.CharField(max_length=12, validators=[bilibili_cn_validator, length_validator(12)], blank=True)
	bilibili_tv = models.CharField(max_length=10, validators=[bilibili_tv_validator], blank=True)
	creator_id = models.CharField(max_length=100, validators=[alphanumeric], blank=False)
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
	sheet_music_url = models.CharField(max_length=420, validators=[validate_url], blank=True)
	internal_notes = models.CharField(max_length=420, blank=True)
	public_notes = models.CharField(max_length=420, blank=True)

	# Tracking
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_modified = models.DateTimeField(auto_now=True, null=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="creator")
	last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="last_editor")