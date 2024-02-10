from django.contrib.auth.views import LoginView
from django.urls import path
from django.http import JsonResponse
from users.tasks import sending_email
from users.views import RegisterView, SettingsView, ProfileLoginView


def sending_email_view(request, email):
    sending_email.delay(email)
    return JsonResponse({'success': True})


urlpatterns = [
    path('sent/<email>/', sending_email_view, name='sending'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='apps/login.html', next_page='product_list'), name='login'),
    path('settings/', ProfileLoginView.as_view(), name='profile'),
]

