# Generated by Django 4.2.11 on 2024-06-06 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0004_alter_dalolatnoma_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dalolatnoma',
            name='bartaraf_etilganligi_hujjati_sana',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dalolatnoma',
            name='bartaraf_etilganligi_sana',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
