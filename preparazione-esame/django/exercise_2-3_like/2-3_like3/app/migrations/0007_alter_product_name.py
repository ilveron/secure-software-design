# Generated by Django 5.0.1 on 2024-01-11 11:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9\\s]*$')]),
        ),
    ]