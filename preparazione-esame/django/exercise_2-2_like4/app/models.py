from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50, validators=[RegexValidator(r'^[A-Za-z]+$')])

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    CATEGORY_CHOICES = {
        "APPETIZER": "Appetizer",
        "FIRST COURSE": "First Course",
        "SECOND COURSE": "Second Course",
        "SIDE DISH": "Side Dish",
        "DESSERT": "Dessert",
        "BEVERAGE": "Beverage"
    }
    author = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z][A-Za-z ]*$')])
    title = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z0-9][A-Za-z0-9 ]*$')])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return f"{self.title} by {self.author} ({self.category}). Ingredients: ({self.__get_ingredients_str__()})"

    def __get_ingredients_str__(self):
        to_return = ""
        for i in self.ingredients.all():
            to_return += f"{str(i)}, "

        return to_return[:-2]
