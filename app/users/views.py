from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User
from .user_services import is_check_verification


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'Registration'
    success_message = 'You are successfully registered!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class UserProfileUpdateView(TitleMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Store - Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Email confirmation'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(
            user=user,
            code=kwargs.get('code'),
        )

        if is_check_verification(email_verification=email_verifications, user=user):
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('index'))
