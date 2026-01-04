from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_AUTHOR = 'author'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_AUTHOR, 'Author'),
        (ROLE_ADMIN, 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
            self.is_staff = True
        else:
            self.is_staff = False

        super().save(*args, **kwargs)

    @property
    def is_author(self):
        return self.role == self.ROLE_AUTHOR

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN