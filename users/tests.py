# Create your tests here.
from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


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

    def __common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.__common_tests(response=response)

    def test_user_registration_post_success(self):
        username = self.data['username']

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
