from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {"form": form}
    return render(request=request, template_name='users/login.html', context=context)


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


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
