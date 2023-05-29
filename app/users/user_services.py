import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_verification_email(user, link):
    send_mail(
        subject='Registration confirmation',
        message=_create_email_massage(user_name=user.username, link=f'{settings.DOMAIN_NAME}{link}'),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
    logger.debug(f'Send mail for {user=}')


def _create_email_massage(user_name, link):
    return (
        f'Hello {user_name}, thank you for registering!\n'
        f'To complete the registration process,'
        f'please confirm your email within 48 hours at the link\n{link}'
    )


def is_check_verification(email_verification, user):
    if email_verification.exists() and not email_verification.first().is_expired():
        _verify_user(user=user)
        logger.debug(f'{user=}')
        return True
    return False


def _verify_user(user):
    user.is_verified_email = True
    user.save()
