from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from note_app.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfiles for all users'

    def handle(self, *args, **kwargs):
        created_count = 0
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'timezone': 'UTC'}
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Created {created_count} new user profiles')
        )