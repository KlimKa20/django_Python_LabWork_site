import datetime

from django.contrib.auth import authenticate
from django.test import TestCase, Client

from firstapp.forms import RegistrationForm, ChangePasswordForm

from firstapp.models import *


class TestModel(TestCase):

    def test_save(self):
        type = Type.objects.create(name="Активный Отдых")
        country = Country.objects.create(name="Франция")
        owner = Owner.objects.create(name="БелТур")
        tour = Tour.objects.create(title="Чехия всегда", country=country, type=type, owner=owner,
                                   image="media/7e79b151a97cc442418bac02086d8499.jpg")

        assert type.name == "Активный Отдых"
        assert type.__str__() == "Активный Отдых"
        assert country.__str__() == "Франция"
        assert owner.__str__() == "БелТур"
        assert tour.__str__() == "Чехия всегда"

    def test_save_user(self):
        User.objects.create_user(username="default", email="default@gmail.com", password="default")
        user = authenticate(username="default", password="default")
        assert user.email == "default@gmail.com"


class TestForm(TestCase):

    def test_registration(self):
        form_data = {'mail': 'Default@gmail.com', 'username': 'Default', 'password': 'Default',
                     'password_repeat': 'Default'}
        form = RegistrationForm(data=form_data)
        assert form.user_return()
        assert form.correct_password()
        form_data = {'mail': 'Default@gmail.com', 'username': 'Default', 'password': 'Default',
                     'password_repeat': 'Default'}
        form = RegistrationForm(data=form_data)
        assert form.error_value()[1] == "Данная почта уже сужествует"
        form_data = {'mail': 'NoneDefault@gmail.com', 'username': 'Default', 'password': 'Default',
                     'password_repeat': 'Default'}
        form = RegistrationForm(data=form_data)
        assert form.error_value()[1] == "Данное имя уже сужествует"
        form_data = {'mail': 'NoneDefault@gmail.com', 'username': 'NoneDefault', 'password': 'NoneDefault',
                     'password_repeat': 'Default'}
        form = RegistrationForm(data=form_data)
        assert form.error_value()[1] == "Пароли не совпадают"

    def test_changepassword(self):
        form_data = {'old_password': 'Default', 'password': 'Default',
                     'password_repeat': 'Default'}
        form = ChangePasswordForm(data=form_data)
        assert form.is_valid()
        assert form.correct_password()
        form_data = {'old_password': 'Default', 'password': 'Default',
                     'password_repeat': 'рefault'}
        form = ChangePasswordForm(data=form_data)
        assert not form.correct_password()


class TestUrl(TestCase):

    def test_login(self):
        c = Client()
        response = c.post('/login/')
        assert response.status_code == 200
        response = c.post('/login/', {'username': 'default', 'password': 'default'})
        assert response.status_code == 200
        User.objects.create_user(username='default', email='default@gmail.com',
                                 password='default')
        response = c.post('/login/', {'username': 'default', 'password': 'default'})
        assert response.status_code == 302

    def test_logout(self):
        User.objects.create_user(username='default', email='default@gmail.com',
                                 password='default')
        c = Client()
        assert c.login(username='default', password='default')
        response = c.post('/logout/')
        assert response.status_code == 302

    def test_changepassword(self):
        User.objects.create_user(username='default', email='default@gmail.com',
                                 password='default')
        c = Client()
        assert c.login(username='default', password='default')
        response = c.post('/changepassword/')
        assert response.status_code == 200
        response = c.post('/changepassword/',
                          {'old_password': 'default', 'password': 'Default', 'password_repeat': 'Default'})
        assert response.status_code == 302
        assert c.login(username='default', password='Default')
        response = c.post('/changepassword/',
                          {'old_password': 'Default', 'password': 'Default', 'password_repeat': 'iefault'})
        assert response.status_code == 200
        response = c.post('/changepassword/',
                          {'old_password': 'iefault', 'password': 'Default', 'password_repeat': 'iefault'})
        assert response.status_code == 200

    def test_about(self):
        c = Client()
        response = c.post('/aboutus/')
        assert response.status_code == 200

    def test_registration(self):
        c = Client()
        response = c.post('/registration/')
        assert response.status_code == 200
        response = c.post('/registration/',
                          {'username': 'default', 'password': 'default', 'password_repeat': 'default',
                           'mail': 'default@gmail.com'})
        assert response.status_code == 302
        response = c.post('/registration/',
                          {'username': 'default', 'password': 'default', 'password_repeat': 'default',
                           'mail': 'default@gmail.com'})
        assert response.status_code == 200

    def test_tour(self):
        type = Type.objects.create(name="Активный Отдых")
        country = Country.objects.create(name="Франция")
        owner = Owner.objects.create(name="БелТур")
        tour = Tour.objects.create(title="Чехия всегда", country=country, type=type, owner=owner,
                                   image="media/7e79b151a97cc442418bac02086d8499.jpg")
        TourInstance.objects.create(id="123e4567-e89b-12d3-a456-426655440000", tour=tour,
                                    date_of_departure=datetime.date.today(),
                                    date_of_arrival=datetime.date.today() + datetime.timedelta(weeks=4),
                                    number_of_seats=60, cost=175)
        c = Client()
        response = c.get("")
        assert response.status_code == 200
        TourInstance.objects.create(id="123e4567-e89b-12d3-a456-426655440001", tour=tour,
                                    date_of_departure=datetime.date.today(),
                                    date_of_arrival=datetime.date.today() + datetime.timedelta(weeks=4),
                                    number_of_seats=60, cost=175)
        TourInstance.objects.create(id="123e4567-e89b-12d3-a456-426655440002", tour=tour,
                                    date_of_departure=datetime.date.today(),
                                    date_of_arrival=datetime.date.today() + datetime.timedelta(weeks=4),
                                    number_of_seats=60, cost=175)
        response = c.get("")
        assert response.status_code == 200
        response = c.post('', {'counter': '123e4567-e89b-12d3-a456-426655440000'})
        assert response.status_code == 302

    def test_userpage(self):
        User.objects.create_user(username='default', email='default@gmail.com', password='default')
        type = Type.objects.create(name="Активный Отдых")
        country = Country.objects.create(name="Франция")
        owner = Owner.objects.create(name="БелТур")
        tour = Tour.objects.create(title="Чехия всегда", country=country, type=type, owner=owner,
                                   image="media/7e79b151a97cc442418bac02086d8499.jpg")
        TourInstance.objects.create(id="123e4567-e89b-12d3-a456-426655440000", tour=tour,
                                    date_of_departure=datetime.date.today(),
                                    date_of_arrival=datetime.date.today() + datetime.timedelta(weeks=4),
                                    number_of_seats=60, cost=175)
        c = Client()
        response = c.get("/userpage/")
        assert response.status_code == 302
        assert c.login(username='default', password='default')
        response = c.get("/userpage/")
        assert response.status_code == 200
        response = c.post("/tourpage/Чехия%20всегда/",
                          {'counter': 'Чехия всегда', 'number': '1'})
        assert response.status_code == 302
        response = c.get("/userpage/")
        assert response.status_code == 200
        response = c.post("/userpage/", {'1': "Отказаться"})
        assert response.status_code == 302

    def test_tourpage(self):
        type = Type.objects.create(name="Активный Отдых")
        country = Country.objects.create(name="Франция")
        owner = Owner.objects.create(name="БелТур")
        tour = Tour.objects.create(title="Чехия всегда", country=country, type=type, owner=owner,
                                   image="media/7e79b151a97cc442418bac02086d8499.jpg")
        TourInstance.objects.update_or_create(id="123e4567-e89b-12d3-a456-426655440000", tour=tour,
                                              date_of_departure=datetime.date.today(),
                                              date_of_arrival=datetime.date.today() + datetime.timedelta(
                                                  weeks=4),
                                              number_of_seats=60, cost=175)

        c = Client()
        c.post('/registration/', {'username': 'default', 'password': 'default', 'password_repeat': 'default',
                                  'mail': 'default@gmail.com'})
        response = c.get("/tourpage/Чехия%20всегда/")
        assert response.status_code == 200
        response = c.post('/logout/')
        assert response.status_code == 302
        response = c.post("/tourpage/Чехия%20всегда/")
        assert response.status_code == 200
        assert c.login(username='default', password='default')
        response = c.post("/tourpage/Чехия%20всегда/",
                          {'counter': 'Чехия всегда', 'number': '1'})
        assert response.status_code == 302
        response = c.post("/tourpage/Чехия%20всегда/",
                          {'counter': 'Чехия всегда', 'number': '1'})
        assert response.status_code == 302
