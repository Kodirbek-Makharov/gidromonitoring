# Generated by Django 4.2.11 on 2024-11-24 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0005_dalolatnoma_bartaraf_etilganligi_hujjati_sana_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dalolatnoma',
            name='maqsadi',
            field=models.CharField(blank=True, choices=[("Xo'jalik-ichimlik", "Xo'jalik-ichimlik"), ('Ishlab chiqarish-texnik', 'Ishlab chiqarish-texnik'), ("Sug'orish", "Sug'orish"), ('Davolash-balneologik', 'Davolash-balneologik'), ('Drenaj', 'Drenaj')], max_length=255, null=True, verbose_name='Suvdan foydalanish maqsadi'),
        ),
        migrations.AddField(
            model_name='dalolatnoma',
            name='miqdori',
            field=models.FloatField(blank=True, null=True, verbose_name='Suv olish miqdori'),
        ),
    ]
