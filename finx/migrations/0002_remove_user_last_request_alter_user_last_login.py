# Generated by Django 4.0.2 on 2022-02-05 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finx', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_request',
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
