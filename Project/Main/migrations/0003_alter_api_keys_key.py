# Generated by Django 5.1.4 on 2025-01-04 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_api_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api_keys',
            name='key',
            field=models.TextField(unique=True, verbose_name='Ключ'),
        ),
    ]
