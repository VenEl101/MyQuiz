from django.contrib.auth.models import AbstractUser
from django.db import models
from common import BaseModel


class UserRoleChoices(models.TextChoices):
    USER = "user", "User"
    ADMIN = "admin", "Admin"


class User(AbstractUser, BaseModel):
    username =  models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.CharField(blank=True, null=True, max_length=150)
    password = models.CharField(null=True, blank=True)
    is_temporary_password = models.BooleanField(default=True)
    first_name = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)

    is_verified = models.BooleanField(default=False)
    is_subscriber = models.BooleanField(default=False)

    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices,
        default=UserRoleChoices.USER
    )
    phone = models.CharField(max_length=15, db_index=True, unique=True, null=True, blank=True)
    chat_id = models.BigIntegerField(unique=True, db_index=True, null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username or f"User {self.id}"

