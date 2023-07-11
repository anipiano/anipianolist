from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

class Command(BaseCommand):
    help = "Custom command for anipianolist to automatically generate groups for moderation roles as defined in .env"

    def handle(self, *args, **options):
        Group.objects.get_or_create(name=env('MAINTAINER_GROUP'))
        Group.objects.get_or_create(name=env('MODERATOR_GROUP'))
        Group.objects.get_or_create(name=env('ADMIN_GROUP'))
        self.stdout.write(self.style.SUCCESS("Groups set up!"))