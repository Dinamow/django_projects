# Generated by Django 5.0.2 on 2024-04-12 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_users_activated'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='activation_token',
            field=models.CharField(default='<function uuid4 at 0x7f645a7f2020>', max_length=50),
        ),
    ]