from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = {
        "ELE": "Electronics",
        "FSH": "Fashion",
        "HOM": "Home",
        "BTY": "Beauty",
        "SPO": "Sports",
        "BKS": "Books",
    }

    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-z0-9\s]*$')])
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    price_in_cents = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000_00)])
    quantity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    def __str__(self):
        return f"{self.name}, priced: {self.price_in_cents//100}.{self.price_in_cents%100:02} (qty. {self.quantity}) - {self.category}"
