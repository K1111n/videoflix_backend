from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def build_activation_url(user):
    """Build the account activation URL containing uid and token."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"


def send_activation_email(user_id):
    """Fetch the user by id and send an HTML activation email."""
    user = User.objects.get(pk=user_id)
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


def set_auth_cookies(response, user):
    """Attach JWT access and refresh token cookies to the response."""
    refresh = RefreshToken.for_user(user)
    jwt_settings = settings.SIMPLE_JWT
    response.set_cookie(
        key='access_token',
        value=str(refresh.access_token),
        httponly=jwt_settings['AUTH_COOKIE_HTTPONLY'],
        samesite=jwt_settings['AUTH_COOKIE_SAMESITE'],
        max_age=int(jwt_settings['ACCESS_TOKEN_LIFETIME'].total_seconds()),
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=jwt_settings['AUTH_COOKIE_HTTPONLY'],
        samesite=jwt_settings['AUTH_COOKIE_SAMESITE'],
        max_age=int(jwt_settings['REFRESH_TOKEN_LIFETIME'].total_seconds()),
    )


def build_password_reset_url(user):
    """Build the password reset URL containing uid and token."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uid}&token={token}"


def send_password_reset_email(user_id):
    """Fetch the user by id and send an HTML password reset email."""
    user = User.objects.get(pk=user_id)
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
