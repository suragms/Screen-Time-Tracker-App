from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile for users that do not have one'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            UserProfile.objects.get_or_create(user=user)
            self.stdout.write(f'Created profile for user {user.username}') 