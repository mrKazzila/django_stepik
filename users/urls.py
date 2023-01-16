from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import login, UserRegistrationCreateView, UserProfileUpdateView, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path("registration/", UserRegistrationCreateView.as_view(), name='registration'),
    path("profile/<int:pk>", login_required(UserProfileUpdateView.as_view()), name='profile'),
    path("logout/", logout, name='logout'),

]
