# Generated by Django 4.1.1 on 2022-09-18 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nss', '0003_user_is_email_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_email_verified',
        ),
    ]
