# Generated by Django 4.0.4 on 2022-06-04 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineschool', '0007_remove_courserequest_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='reviews',
        ),
    ]
