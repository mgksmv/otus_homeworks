# Generated by Django 4.0.4 on 2022-06-03 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineschool', '0005_courserequest_email_registrationrequest_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineschool.course', verbose_name='Курс'),
        ),
    ]