# Generated by Django 4.0.1 on 2022-02-03 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='world',
            index=models.Index(fields=['created_at'], name='rest_world_created_4b4a55_idx'),
        ),
    ]
