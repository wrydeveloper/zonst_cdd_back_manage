# Generated by Django 2.0.4 on 2018-06-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_auto_20180605_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='channel',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
    ]