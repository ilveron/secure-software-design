from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.
class Song(models.Model):
    GENRE_CHOICES = {
        'ROCK': 'Rock',
        'RAP': 'Rap',
        'TRAP': 'Trap',
        'COUNTRY': 'Country',
        'PUNK': 'Punk',
        'HOUSE': 'House',
        'DANCE': 'Dance',
    }
    author = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z0-9 ]*$')])
    title = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z0-9 ]*$')])
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES)
    duration_in_seconds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3600)])

    def __str__(self):
        return f'{self.author} - {self.title} [{self.genre}] ({self.duration_in_seconds // 60}:{self.duration_in_seconds % 60:02})'
