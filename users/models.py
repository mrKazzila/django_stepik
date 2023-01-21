from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'{self.__class__.__name__} for {self.user}'

    def send_verification_email(self):
        link = reverse(
            'users:email_verification',
            kwargs={
                'email': self.user.email,
                'code': self.code
            }
        )
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = 'Подтверждение регистрации'
        massage = (f'{self.user.username}, благодарим вас за регистрацию!\n'
                   f'Для завершения процедуры регистрации,'
                   f'пожалуйста, подтвердите ваш email по ссылке {verification_link} в течении 48 часов.')

        send_mail(
            subject=subject,
            message=massage,
            from_email=settings.EMAIL_HOST_USER,  # settings.EMAIL_HOST_USER
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
