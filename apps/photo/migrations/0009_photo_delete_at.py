# Generated by Django 4.2.5 on 2023-11-21 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0008_photo_latitude_photo_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='delete_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]