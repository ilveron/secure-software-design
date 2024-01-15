# Generated by Django 5.0.1 on 2024-01-15 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_book_delete_superhero'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
