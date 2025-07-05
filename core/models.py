from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.contrib.auth.models import BaseUserManager


class Screen(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Screen, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusuário precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Liberar obrigatoriedade
    email = models.EmailField(unique=True)  # Obrigatório e usado como login

    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='users/photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'         # Login via email
    REQUIRED_FIELDS = []             # Nenhum campo adicional obrigatório no createsuperuser

    objects = CustomUserManager()

    def has_permission(self, screen_name):
        if self.is_superuser or self.is_admin:
            return True
        if self.group:
            return self.group.permissions.filter(name=screen_name).exists()
        return False

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Força espelhamento
        super().save(*args, **kwargs)