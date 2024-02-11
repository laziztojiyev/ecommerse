from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView

from apps.forms import UserRegistrationForm
from users.models import CustomUser
from users.tasks import sending_email


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        sending_email.delay([form.data.get('email')])
        return super().form_valid(form)


class ProfileLoginView(TemplateView, LoginRequiredMixin):
    template_name = 'auth/user_settings.html'


class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'phone_number', 'about_me', 'email', 'password']
    template_name = 'auth/user_settings.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.get_success_url())  # Redirect to success URL

