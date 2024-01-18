from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.
class VideoGame(models.Model):
    title = models.CharField(max_length=100)
    developer = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])