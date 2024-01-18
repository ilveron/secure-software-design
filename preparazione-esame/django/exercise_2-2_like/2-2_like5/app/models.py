import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


def date_time_is_in_the_future(value):
    if value < timezone.now():
        raise ValidationError('Date and time must be in the future.')


# Create your models here.
class TrainTicket(models.Model):
    departure = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z0-9 ]+$')])
    destination = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z0-9 ]+$')])
    date_time = models.DateTimeField(validators=[date_time_is_in_the_future])
    price_in_cents = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999_99)])

    def __str__(self):
        return f"{self.departure} -> {self.destination} leaves at {self.date_time.hour:02}:{self.date_time.minute:02} of {self.date_time.day:02}/{self.date_time.month:02}/{self.date_time.year:04}. Price: {self.price_in_cents//100}.{self.price_in_cents%100:02}"