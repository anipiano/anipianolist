# Generated by Django 4.1.4 on 2023-02-09 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_arrangemententry_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrangemententry',
            name='staff_member',
        ),
    ]
