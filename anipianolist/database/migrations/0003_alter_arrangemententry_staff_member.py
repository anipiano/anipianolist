# Generated by Django 4.1.4 on 2023-02-08 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0002_arrangemententry_staff_member_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrangemententry',
            name='staff_member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
