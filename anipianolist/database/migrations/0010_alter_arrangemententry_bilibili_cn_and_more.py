# Generated by Django 4.1.4 on 2023-02-11 01:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_arrangemententry_last_modified_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrangemententry',
            name='bilibili_cn',
            field=models.SlugField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator('BV[0-9A-Za-z]+$', 'Bilibili.com video IDs must be alphanumeric and start with BV ( ´△｀)'), django.core.validators.MinLengthValidator(12, 'This video ID must be 12 characters long!')]),
        ),
        migrations.AlterField(
            model_name='arrangemententry',
            name='bilibili_tv',
            field=models.SlugField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('[0-9]+$', 'Bilibili.tv video IDs must be numeric ( ´△｀)')]),
        ),
        migrations.AlterField(
            model_name='arrangemententry',
            name='creator_id',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\.\\-\\_]*$', 'A creator ID can only contain letters, numbers, periods, hyphens or underscores, baka!')]),
        ),
        migrations.AlterField(
            model_name='arrangemententry',
            name='sheet_music_url',
            field=models.CharField(blank=True, max_length=420, validators=[django.core.validators.URLValidator("That isn't a valid URL!")]),
        ),
        migrations.AlterField(
            model_name='arrangemententry',
            name='youtube_id',
            field=models.SlugField(blank=True, max_length=11, validators=[django.core.validators.MinLengthValidator(11, 'This video ID must be 11 characters long!')]),
        ),
    ]
