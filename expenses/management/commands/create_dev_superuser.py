from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a non-interactive superuser for development purposes.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin' # WARNING: Use a strong password in production!

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password, role='admin')
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser: {username} already exists.'))
