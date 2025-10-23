from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from note_app.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfiles for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created user profiles'))