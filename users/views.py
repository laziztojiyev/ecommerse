from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

from apps import forms
from apps.forms import UserRegistrationForm
from apps.models import Category, Product
from users.forms import UserSettingsForm
from users.models import CustomUser
from users.tasks import sending_email
from django.urls import reverse_lazy


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        sending_email.delay([form.data.get('email')])
        return super().form_valid(form)


class SettingsView(UpdateView):
    model = CustomUser
    form_class = UserSettingsForm
    template_name = 'auth/user_settings.html'


class ProfileLoginView(TemplateView, LoginRequiredMixin):
    template_name = 'auth/user_settings.html'
