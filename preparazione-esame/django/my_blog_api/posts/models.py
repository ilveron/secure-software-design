from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from posts.validators import validate_title


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=50, validators=[validate_title])
    body = models.TextField(validators=[RegexValidator(r'^[\w\s.:;\'"]*$')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
