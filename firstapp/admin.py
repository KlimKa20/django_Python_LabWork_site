import datetime
import time
from multiprocessing.dummy import Manager
from multiprocessing.pool import Pool

from django.contrib import admin
from django.core.mail import send_mail, BadHeaderError

from untitled2.settings import EMAIL_HOST_USER
from .models import Owner, Tour, TourInstance, Type, Profile, Country, ProfileTickets, Feedback


class EmailReply(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.email_reply_text:
            return

        recipients = [
            x.user.email for x in Profile.objects.all() if x.verified
        ]

        def send(email):
            send_mail(obj.email_reply_capt, datetime.datetime.now().strftime("%H:%M:%S"), EMAIL_HOST_USER, [email])
            time.sleep(10)

        pool = Manager().Pool(4)  # process per core
        pool.map(send, recipients)

        # сбрасываем поля, чтобы при следующем сохранении модели случайно не отправить письмо ещё раз
        # поле адреса электронной почты я не сбрасываю. Вдруг пригодится ещё
        obj.email_reply_capt = ''
        obj.email_reply_text = None
        super().save_model(request, obj, form, change)


admin.site.register(Feedback, EmailReply)
admin.site.register(Owner)
admin.site.register(Tour)
admin.site.register(TourInstance)
admin.site.register(Type)
admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(ProfileTickets)
