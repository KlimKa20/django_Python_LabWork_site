from django import forms
from django.contrib.auth.models import User


class UserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "myfield"}), label="LogIn")
    age = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label="Password")


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "myfield"}), label="LogIn")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label="Password")


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "myfield"}), label="LogIn")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label="Password")
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label="Password repeat")
    mail = forms.CharField(widget=forms.EmailInput(attrs={"class": "myfield"}), label="Mail")

    def correct_password(self):
        password_value = self.data["password"]
        password_repeat = self.data["password_repeat"]
        if password_repeat == password_value:
            return True
        return False

    def error_value(self):
        user_value = self.data["username"]
        mail = self.data["mail"]
        if User.objects.filter(email__iexact=mail).exists():
            return "error_mail", "Данная почта уже сужествует"
        if User.objects.filter(username__iexact=user_value).exists():
            return "error_name", "Данное имя уже сужествует"
        if not self.correct_password():
            return "error_password", "Пароли не совпадают"

    def user_return(self):
        return User.objects.create_user(username=self.data["username"], email=self.data["mail"],
                                        password=self.data["password"])


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label="Old Password")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label="New Password")
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}),
                                      label="New Password repeat")

    def correct_password(self):
        password_value = self.data["password"]
        password_repeat_value = self.data["password_repeat"]
        if password_value == password_repeat_value:
            return True
        return False

