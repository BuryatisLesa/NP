# Generated by Django 5.1 on 2024-10-28 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsportal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
