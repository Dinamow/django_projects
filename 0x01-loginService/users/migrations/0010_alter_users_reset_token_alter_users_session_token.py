# Generated by Django 5.0.2 on 2024-04-15 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_users_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='reset_token',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='session_token',
            field=models.CharField(max_length=50),
        ),
    ]