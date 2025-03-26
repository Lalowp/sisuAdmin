from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from sisuInvitaciones.sisu.models import Event
from sisuInvitaciones.sisu.models import Guest

class Command(BaseCommand):
    help = 'Create admin groups and assign permissions'

    def handle(self, *args, **options):
        #Create groups
        superadmin_group, created = Group.objects.get_or_create(name='SuperAdmin')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        #Assign permissions to groups
        # SuperAdmin group gets all permissions
        superadmin_group.permissions.set(Permission.objects.all())

        # Admin group gets specific permissions (excluding user-related permissions)
        user_content_type = ContentType.objects.get(app_label='auth', model='user')
        admin_permissions = Permission.objects.exclude(content_type=user_content_type)
        admin_group.permissions.set(admin_permissions)

        # Create a superuser and assign to SuperAdmin group (if not already created)
        if not User.objects.filter(username='galab').exists():
            superuser = User.objects.create_superuser('galab', 'galabconsulting@gmail.com', 'Galab2025$')
            superuser.groups.add(superadmin_group)

        # Create a superuser and assign to admin group (if not already created)
        if not User.objects.filter(username='sisuAraAdmin').exists():
            admin1 = User.objects.create_user('sisuAraAdmin','sisuAraAdmin@superrito.com','sisuAraAdmin2025$')
            admin1.is_staff = True
            admin1.save()
            self.stdout.write(self.style.SUCCESS('Successfully created admin1'))

        if not User.objects.filter(username='sisuRicAdmin').exists():
            admin2 = User.objects.create_user('sisuRicAdmin','sisuRicAdmin@superrito.com','sisuRicAdmin2025$')
            admin2.is_staff = True
            admin2.save()
            self.stdout.write(self.style.SUCCESS('Successfully created admin2'))

        #Assigning admin users to admin group
        event_content_type = ContentType.objects.get_for_model(Event)
        guest_content_type = ContentType.objects.get_for_model(Guest)
        event_permissions = Permission.objects.filter(content_type=event_content_type)
        guest_permissions = Permission.objects.filter(content_type=guest_content_type)

        admin1.user_permissions.set(event_permissions)
        admin1.user_permissions.set(guest_permissions)

        admin2.user_permissions.set(event_permissions)
        admin2.user_permissions.set(guest_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))