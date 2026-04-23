from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


def build_activation_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"


def send_activation_email(user):
    activation_url = build_activation_url(user)
    html_body = render_to_string('emails/activation_email.html', {'activation_url': activation_url})
    email = EmailMessage(
        subject='Videoflix – Account aktivieren',
        body=html_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


def build_password_reset_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uid}&token={token}"


def send_password_reset_email(user):
    reset_url = build_password_reset_url(user)
    html_body = render_to_string('emails/password_reset_email.html', {'reset_url': reset_url})
    email = EmailMessage(
        subject='Videoflix – Passwort zurücksetzen',
        body=html_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()
