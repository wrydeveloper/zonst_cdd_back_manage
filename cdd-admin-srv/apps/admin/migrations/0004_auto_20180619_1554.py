# Generated by Django 2.0.4 on 2018-06-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_auto_20180618_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolepermission',
            name='permission',
            field=models.CharField(default='', max_length=500),
        ),
    ]