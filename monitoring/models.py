from typing import Iterable
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from PIL import Image
from datetime import date
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class Viloyat(models.Model):
    nomi = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"

    def __str__(self):
        return self.nomi

class Tuman(models.Model):
    nomi = models.CharField(max_length=100)
    viloyat = models.ForeignKey(Viloyat, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"

    def __str__(self):
        return self.nomi

class Noqonuniy_holat_turi(models.Model):
    nomi = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Noqonuniy holat turi"
        verbose_name_plural = "Noqonuniy holat turi"

    def __str__(self):
        return self.nomi

class Stansiya(models.Model):
    nomi = models.CharField(max_length=200)
    seriya = models.CharField(max_length=20, null=True, blank=True)
    status = models.BooleanField(default=True)
    soni = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Stansiya"
        verbose_name_plural = "Stansiyalar"

    def __str__(self):
        return self.nomi


class Dalolatnoma(models.Model):

    def kr_qogoz(instance, filename):
        ext = filename.split(".")[-1].lower()
        if ext not in ["jpg", "png", "gif", "jpeg"]:
            raise ValidationError(f"invalid image extension: {filename}")
        filename = f"{instance.pk}-qogoz.{ext}"
        _now = datetime.now()
        return f"korsatma/{_now.strftime('%Y')}/{_now.strftime('%m')}/{filename}"

    def kr_odam(instance, filename):
        ext = filename.split(".")[-1].lower()
        if ext not in ["jpg", "png", "gif", "jpeg"]:
            raise ValidationError(f"invalid image extension: {filename}")
        filename = f"{instance.id}-odam.{ext}"
        _now = datetime.now()
        return f"korsatma/{_now.strftime('%Y')}/{_now.strftime('%m')}/{filename}"

    def brt_hujjat(instance, filename):
        ext = filename.split(".")[-1].lower()
        if ext not in ["jpg", "png", "pdf", "docx"]:
            raise ValidationError(f"invalid image extension: {filename}")
        filename = f"{instance.id}-bartaraf-hujjat.{ext}"
        _now = datetime.now()
        return f"korsatma/{_now.strftime('%Y')}/{_now.strftime('%m')}/{filename}"

    noqonuniy_holat_turi = models.ForeignKey(Noqonuniy_holat_turi, on_delete=models.CASCADE)
    maqsadi = models.CharField("Suvdan foydalanish maqsadi", max_length=255, null=True, blank=True, choices=[("Xo'jalik-ichimlik","Xo'jalik-ichimlik"), ("Ishlab chiqarish-texnik", "Ishlab chiqarish-texnik"), ("Sug'orish", "Sug'orish"), ("Davolash-balneologik", "Davolash-balneologik"), ("Drenaj", "Drenaj")])
    miqdori = models.FloatField("Suv olish miqdori", null=True, blank=True)
    huquqbuzar_turi = models.CharField(max_length=25, choices=[('jismoniy', "Jismoniy shaxs"),('yuridik', "Yuridik shaxs")])
    huquqbuzar_nomi = models.CharField(max_length=255)
    huquqbuzar_stir = models.CharField(max_length=100)
    tuman = models.ForeignKey(Tuman, on_delete=models.CASCADE)
    orientir = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    lng = models.DecimalField(max_digits=11, decimal_places=8)
    stansiya = models.ForeignKey(Stansiya, on_delete=models.CASCADE)
    inspektor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    korsatma_raqam = models.CharField(max_length=100, unique = True)
    korsatma_sana = models.DateTimeField()
    korsatma_rasm_qogoz = models.ImageField(upload_to=kr_qogoz)
    korsatma_rasm_odam = models.ImageField(upload_to=kr_odam)

    amal_qilish_muddati = models.DateField(default=datetime.today)
    bartaraf_etilganligi = models.BooleanField(null=True, blank=True, default=False)
    bartaraf_etilganligi_sana = models.DateTimeField(null=True, blank=True)
    bartaraf_etilganligi_hujjati = models.FileField(null=True, blank=True, upload_to=brt_hujjat)
    bartaraf_etilganligi_hujjati_sana = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


    @property
    def bartaraf_etilmagan(self):
        return (not self.bartaraf_etilganligi) and (date.today() > self.amal_qilish_muddati)

    class Meta:
        verbose_name = "Dalolatnoma"
        verbose_name_plural = "Dalolatnomalar"

    def __str__(self):
        return self.korsatma_raqam


_UNSAVED_FILEFIELD_q = 'kqogoz'
_UNSAVED_FILEFIELD_o = 'kodam'

@receiver(pre_save, sender=Dalolatnoma)
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not hasattr(instance, _UNSAVED_FILEFIELD_q):
        setattr(instance, _UNSAVED_FILEFIELD_q, instance.korsatma_rasm_qogoz)
        instance.korsatma_rasm_qogoz = "temp"
    if not instance.pk and not hasattr(instance, _UNSAVED_FILEFIELD_o):
        setattr(instance, _UNSAVED_FILEFIELD_o, instance.korsatma_rasm_odam)
        instance.korsatma_rasm_odam = "temp"

@receiver(post_save, sender=Dalolatnoma)
def save_file(sender, instance, created, **kwargs):
    print("SAVE", created, instance)
    if created and hasattr(instance, _UNSAVED_FILEFIELD_q):
        instance.korsatma_rasm_qogoz = getattr(instance, _UNSAVED_FILEFIELD_q)
        instance.save()
        kq = Image.open(instance.korsatma_rasm_qogoz.path)
        kq.thumbnail((2000,2000),Image.LANCZOS)
        # kq.resize((1000,1000), Image.LANCZOS)
        kq.save(instance.korsatma_rasm_qogoz.path)
    if created and hasattr(instance, _UNSAVED_FILEFIELD_o):
        instance.korsatma_rasm_odam = getattr(instance, _UNSAVED_FILEFIELD_o)
        instance.save()        
        ko = Image.open(instance.korsatma_rasm_odam.path)
        ko.thumbnail((2000,2000),Image.LANCZOS)
        # ko.resize((1000,1000), Image.LANCZOS)
        ko.save(instance.korsatma_rasm_odam.path)
    if instance.bartaraf_etilganligi_hujjati:
        br = Image.open(instance.bartaraf_etilganligi_hujjati.path)
        br.thumbnail((2000,2000),Image.LANCZOS)
        br.save(instance.bartaraf_etilganligi_hujjati.path)
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "message": [instance.korsatma_raqam, instance.inspektor.username, instance.id],
            }
        )


class DalolatnomaRasm(models.Model):

    def photo_location(instance, filename):
        pk = instance.dalolatnoma.pk
        _now = datetime.now()
        return f"photos/{_now.strftime('%Y')}/{_now.strftime('%m')}/{pk}-{filename}"  

    dalolatnoma = models.ForeignKey(Dalolatnoma, on_delete=models.CASCADE)
    rasm = models.ImageField(upload_to=photo_location)

@receiver(post_save, sender=DalolatnomaRasm)
def save_file(sender, instance, created, **kwargs):
    if created:
        ko = Image.open(instance.rasm.path)
        w,h=ko.size
        ko.thumbnail((2000,2000),Image.LANCZOS)
        # ko=ko.resize((1000,1000), Image.LANCZOS)
        ko.save(instance.rasm.path)
