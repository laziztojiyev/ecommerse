from django.contrib.auth.views import LoginView
from django.urls import path
from django.http import JsonResponse
from users.tasks import sending_email
from users.views import RegisterView, ProfileLoginView, UserUpdateView


def sending_email_view(request, email):
    sending_email.delay(email)
    return JsonResponse({'success': True})


urlpatterns = [
    path('sent/<email>/', sending_email_view, name='sending'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='auth/login.html', next_page='product_list'), name='login'),
    path('settings/', ProfileLoginView.as_view(), name='profile'),
    path('settings/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]

