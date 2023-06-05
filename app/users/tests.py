from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import User
from .forms import UserLoginForm


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            'first_name': 'Peka',
            'last_name': 'LastPeka',
            'username': 'peka',
            'email': 'peka@mail.ru',
            'password1': 'pass8worD',
            'password2': 'pass8worD',
        }
        self.path = reverse('users:registration')

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self._common_tests(response=response)

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)


class UserLoginViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
        )
        self.login_url = reverse('users:login')

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_successful(self):
        _data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, _data)

        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        _data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, _data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
