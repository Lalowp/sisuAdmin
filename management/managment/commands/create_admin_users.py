from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create admin users'

    def handle(self, *args, **options):
        # Create superadmin user
        if not User.objects.filter(username='galab').exists():
            superadmin = User.objects.create_superuser('galab', 'galabconsulting@gmail.com', 'Galab2025$')
            self.stdout.write(self.style.SUCCESS('Successfully created superadmin'))

        # Create 1st admin user
        if not User.objects.filter(username='sisuAraAdmin').exists():
            admin1 = User.objects.create_superuser('sisuAraAdmin','sisuAraAdmin@superrito.com','sisuAraAdmin2025$')
            self.stdout.write(self.style.SUCCESS('Successfully created admin1'))

        # Create 2nd admin user
        if not User.objects.filter(username='sisuRicAdmin').exists():
            admin2 = User.objects.create_superuser('sisuRicAdmin','sisuRicAdmin@superrito.com','sisuRicAdmin2025$')
            self.stdout.write(self.style.SUCCESS('Successfully created admin2'))
