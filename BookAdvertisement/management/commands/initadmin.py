from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.stdout.write("here\n")
