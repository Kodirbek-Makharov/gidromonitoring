# Generated by Django 4.2.11 on 2024-04-16 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0002_dalolatnoma_amal_qilish_muddati_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dalolatnoma',
            name='korsatma_raqam',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
