
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField("ProfileTickets", blank=True)
    verified = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProfileTickets(models.Model):
    tour = models.ForeignKey("TourInstance", blank=True, on_delete=models.DO_NOTHING)
    count = models.IntegerField(null=True)


class Tour(models.Model):
    title = models.CharField(max_length=200, help_text="Название тура")
    type = models.ForeignKey("Type", on_delete=models.DO_NOTHING, help_text="Тип тура")
    description = models.TextField(max_length=1000, help_text="Краткое описание тура")
    owner = models.ForeignKey("Owner", null=False, on_delete=models.DO_NOTHING)
    image = models.ImageField(height_field=None, width_field=None, max_length=100)
    country = models.ForeignKey("Country", null=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Type(models.Model):
    name = models.CharField(max_length=200, help_text="Тип тура")

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200, help_text="Страна")

    def __str__(self):
        return self.name


class TourInstance(models.Model):
    id = models.UUIDField(primary_key=True)
    tour = models.ForeignKey("Tour", on_delete=models.SET_NULL, null=True)
    date_of_departure = models.DateField(null=False, blank=True)
    date_of_arrival = models.DateField(null=False, blank=True)
    number_of_seats = models.IntegerField(null=False)
    cost = models.IntegerField(null=False)

    class Meta:
        ordering = ["date_of_departure"]


class Owner(models.Model):
    name = models.CharField(max_length=100)
    date_of_opening = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    email_reply_capt = models.CharField('Заголовок ответа на e-mail', blank=True, max_length=500)
    email_reply_text = models.TextField('Текст ответа на e-mail', null=True, blank=True)
    email_reply_date = models.DateTimeField("Время отправки", null=True, blank=True)
    email_reply_adress = models.ManyToManyField("Profile", null=True, blank=True)



