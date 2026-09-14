import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Crea o actualiza el usuario administrador de producción"

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "No se configuraron las variables del administrador."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email or ""},
        )

        if email:
            user.email = email

        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrador '{username}' creado correctamente."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrador '{username}' actualizado correctamente."
                )
            )