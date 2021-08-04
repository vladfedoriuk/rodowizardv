from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            User.objects.get(username=settings.DEFAULT_ADMIN.get("username"))
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username=settings.DEFAULT_ADMIN.get("username"),
                password=settings.DEFAULT_ADMIN.get("password"),
                email=settings.DEFAULT_FROM_EMAIL,
            )
            user.is_active = True
            user.is_admin = True
            user.is_staff = True
            user.save()
