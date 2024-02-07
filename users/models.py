from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    first_name = models.CharField(max_length=35, verbose_name='First Name')
    last_name = models.CharField(max_length=35, verbose_name='Last Name', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Phone', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
