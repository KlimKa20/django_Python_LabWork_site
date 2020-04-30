import hashlib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from firstapp.models import TourInstance, Tour, ProfileTickets, Profile
from untitled2.settings import EMAIL_HOST_USER


def page_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.data["username"]
        password_value = form.data["password"]
        user = authenticate(username=username, password=password_value)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            context = {'form': form,
                       'error': 'The username and password combination is incorrect'}
            return render(request, 'registration/login.html', context)
    else:
        return render(request, 'registration/login.html', {'form': form})


def page_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def page_change_password(request):
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        old_value = form.data["old_password"]
        password_value = form.data["password"]
        if check_password(old_value, request.user.password):
            if form.correct_password():
                user = request.user
                user.set_password(password_value)
                user.save()
                return HttpResponseRedirect("/")
            else:
                context = {'form': form,
                           'error': "The new passwords aren't same"}
        else:
            context = {'form': form,
                       'error': 'The old password is incorrect'}
        return render(request, 'registration/changepage.html', context)
    else:
        return render(request, 'registration/changepage.html', {'form': form})


def page_tours(request, name):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user.profile
            tour = Tour.objects.get(title=request.POST.get('counter'))
            if TourInstance.objects.get(tour=tour).number_of_seats > 0:
                instance = TourInstance.objects.get(tour=tour)
                instance.number_of_seats -= int(request.POST.get("number"))
                if user.tickets.filter(tour=instance).exists():
                    temper_ticket = user.tickets.get(tour=instance)
                    temper_ticket.count += int(request.POST.get("number"))
                    temper_ticket.save()
                else:
                    new_tour = ProfileTickets(tour=instance, count=int(request.POST.get("number")))
                    new_tour.save()
                    user.tickets.add(new_tour)
                instance.save()
                user.save()
            return HttpResponseRedirect("/")
        else:
            form = LoginForm(request.POST or None)
            return render(request, 'registration/login.html', {'form': form})
    else:
        tours = Tour.objects.get(title=name)
        instance = TourInstance.objects.get(tour=tours)
        data = {"tours": instance}
        return render(request, 'firstapp/tourpage.html', context=data)


def page_tour_instance(request):
    if request.method == "POST":
        tours = TourInstance.objects.get(id=request.POST.get('counter')).tour.title
        return HttpResponseRedirect(reverse('tourpage', args=(tours,)))
    else:
        all_object = TourInstance.objects.all()
        context = list()
        temper = list()
        for object in all_object:
            temper.append(object)
            if len(temper) == 3:
                context.append(temper)
                temper = list()
        if len(temper) != 0:
            context.append(temper)
        return render(request, 'firstapp/tourInstance_list.html', {"object_lis": context})


def page_user(request):
    if request.method == "POST":
        object_id = None
        num = 1
        while object_id != "Отказаться":
            object_id = request.POST.get(str(num), None)
            num += 1
        tickets = request.user.profile.tickets.all()
        ticket = tickets[num - 2]
        instance = TourInstance.objects.get(tour=ticket.tour.tour)
        instance.number_of_seats += ticket.count
        request.user.profile.tickets.remove(ticket)
        profile = ProfileTickets.objects.get(id=ticket.id)
        profile.delete()
        instance.save()
        return HttpResponseRedirect("/")
    else:
        if request.user.is_authenticated:
            tickets = request.user.profile.tickets.all()
            if len(tickets) == 0:
                data = {"tickets": "None"}
            else:
                data = {"tickets": tickets}
            return render(request, 'firstapp/user.html', context=data)
        else:
            return HttpResponseRedirect("/")


def page_registration(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        context = {'form': form}
        value = form.error_value()
        if not value:
            user = form.user_return()
            login(request, user)
            sha = hashlib.md5(request.user.username.encode())
            send_mail('Подтверждение почты', 'http://127.0.0.1:8000/confirmation/' + sha.hexdigest(), EMAIL_HOST_USER,
                      [request.user.email], )
            return HttpResponseRedirect("/")
        else:
            context[value[0]] = value[1]
            return render(request, 'registration/registration.html', context)
    else:
        return render(request, 'registration/registration.html', {'form': form})


def page_about_us(request):
    return render(request, 'firstapp/aboutus.html')


def page_confirmation(request, name):
    users = Profile.objects.all()
    context = {"information": "Активация прошла успешно"}
    for user in users:
        sha = hashlib.md5(user.user.username.encode())
        if sha.hexdigest() == name:
            user.verified = True
            context["information"] = "Активация прошла успешно"
            user.save()
            break
    return render(request, 'firstapp/confirmation.html', context)