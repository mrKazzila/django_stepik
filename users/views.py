# Create your views here.
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:profile')  # куда пользователя перенаправят
    title = 'Registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.title
        return context


class UserProfileUpdateView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.title
        context["baskets"] = Basket.objects.filter(user=self.object)
        return context
