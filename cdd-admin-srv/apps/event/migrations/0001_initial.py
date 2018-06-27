# Generated by Django 2.0.4 on 2018-05-28 09:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('point_id', models.IntegerField(default=1)),
                ('channel_id', models.IntegerField(default=100001)),
                ('user_id', models.IntegerField(default=0)),
                ('platform', models.IntegerField(default=1)),
                ('ip', models.CharField(max_length=50)),
                ('ua', models.CharField(max_length=500)),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'cdd_event_info',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'cdd_point_info',
                'ordering': ('-created_at',),
            },
        ),
    ]
