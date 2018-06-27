# Generated by Django 2.0.4 on 2018-05-25 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_auto_20180521_1523'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyDataDay',
        ),
        migrations.RemoveField(
            model_name='channeldataday',
            name='proxy_id',
        ),
        migrations.RemoveField(
            model_name='channeldataday',
            name='proxy_type',
        ),
        migrations.AlterUniqueTogether(
            name='channeldataday',
            unique_together={('report_date', 'platform', 'channel_id')},
        ),
    ]
