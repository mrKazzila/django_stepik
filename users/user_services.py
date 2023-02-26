from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user, link):
    send_mail(
        subject='Подтверждение регистрации',
        message=_create_email_massage(user_name=user.username, link=f'{settings.DOMAIN_NAME}{link}'),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )


def _create_email_massage(user_name, link):
    return (f'{user_name}, благодарим вас за регистрацию!\n'
            f'Для завершения процедуры регистрации,'
            f'пожалуйста, подтвердите ваш email по ссылке {link} в течении 48 часов.')


def is_check_verification(email_verification, user):
    if email_verification.exists() and not email_verification.first().is_expired():
        user.is_verified_email = True
        user.save()
        return True
    return False
