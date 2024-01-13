from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, validators=[RegexValidator(r'^[A-Za-z0-9\s]*$')])

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, validators=[RegexValidator(r'^[A-Za-z0-9\s]*$')])
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return f"{self.title} by {self.author}, {self.date}, ({[str(tag) for tag in self.tags.all()]})"
