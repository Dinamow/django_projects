# Generated by Django 5.0.2 on 2024-04-12 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='reset_token',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='users',
            name='session_token',
            field=models.CharField(default=0, max_length=50),
        ),
    ]