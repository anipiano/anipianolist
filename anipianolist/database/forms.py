from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import ArrangementEntry

from .language_choices import LANGUAGE_CHOICES

class CreateEntryForm(forms.ModelForm):
	required_css_class = 'required'
	alphanumeric = RegexValidator(r'^[0-9a-zA-Z\.\-\_]*$', 'A creator ID can only contain letters, numbers, periods, hyphens or underscores, baka!')

	title = forms.CharField(max_length=100, required=True, label="Video title", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g  [Animenz arr.] Domestic Girlfriend OP - Kawaki wo Ameku (Crying for Rain) | 200 Subs Special'}))
	youtube_id = forms.CharField(max_length=11, required=False, label="YouTube video ID (11 alphanumeric digits)", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g 5wBN1WeK9Gc'})) # todo: custom validator
	bilibili_cn = forms.CharField(max_length=12, required=False, label="Bilibili.com video ID (12 alphanumeric digits)", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g BV1oq4y197XM'}))
	bilibili_tv = forms.CharField(max_length=10, required=False, label="Bilibili.tv video ID (10 numeric digits)", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g 2004101838'}))
	creator_id = forms.CharField(max_length=100, required=True, label="Creator ID", label_suffix='', validators=[alphanumeric], widget=forms.TextInput(attrs={'placeholder': 'e.g WikiBidoz'}))
	instruments = forms.CharField(max_length=200, initial="Piano", required=True, label="Instrument(s)", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g Piano, Bass Guitar'}))

	# Optional fields
	language = forms.ChoiceField(required=True, label="Track language", choices=LANGUAGE_CHOICES, label_suffix='')
	track_name_en = forms.CharField(max_length=100, required=False, label="Track name - English", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g Crying for Rain'}))
	track_name_rom = forms.CharField(max_length=100, required=False, label="Track name - Romanisation", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g Kawaki wo Ameku'}))
	track_name_cjk = forms.CharField(max_length=100, required=False, label="Track name - CJK script", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g カワキヲアメク'}))
	series_name = forms.CharField(max_length=100, required=False, label="Series name", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g Domestic Girlfriend'}))
	arranger = forms.CharField(max_length=100, required=False, label="Arranger", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g Animenz Piano Sheets'}))
	original_artist = forms.CharField(max_length=100, required=False, label="Original artist", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g Minami'}))
	upload_date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Upload date (UTC)", label_suffix='')
	sheet_music_url = forms.CharField(max_length=420, required=False, label="Sheet music URL", label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'e.g https://www.mymusicsheet.com/animenzzz/47276'}))
	internal_notes = forms.CharField(max_length=420, required=False, widget=forms.Textarea, label="Internal notes (viewable only to Maintainers)", label_suffix='')
	public_notes = forms.CharField(max_length=420, required=False, widget=forms.Textarea, label="Public notes")

	class Meta: # it is safer to define fields https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/#selecting-the-fields-to-use
		model = ArrangementEntry
		fields = ['title', 'youtube_id', 'bilibili_cn', 'bilibili_tv', 'creator_id', 'language', 'track_name_en',
					'track_name_rom', 'track_name_cjk', 'series_name', 'arranger', 'original_artist', 
					'instruments', 'upload_date', 'sheet_music_url', 'internal_notes', 'public_notes']
		exclude = ["created_by", "last_modified_by"]