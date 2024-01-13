from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.
class SuperHero(models.Model):
    epic_name = models.CharField(max_length=50)
    secret_identity = models.CharField(max_length=50)
    city = models.CharField(max_length=50)