# Generated by Django 4.0.2 on 2023-08-30 18:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_us',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
