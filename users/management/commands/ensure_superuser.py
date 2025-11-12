from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Ensure a superuser exists (creates one if none exists, using environment variables)"

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists. Skipping creation.')
            )
            return

        # Get superuser details from environment variables
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD')

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    'No ADMIN_PASSWORD environment variable set. '
                    'Skipping superuser creation. '
                    'Set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD to create a superuser automatically.'
                )
            )
            return

        # Check if username already exists (but not as superuser)
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'User "{username}" already exists but is not a superuser. '
                    'Skipping creation. Please create superuser manually or use a different username.'
                )
            )
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with email "{email}"'
                )
            )
            self.stdout.write(
                f'You can now log in to Django admin at /admin/'
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )

