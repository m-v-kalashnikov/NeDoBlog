from django.urls import path
from .views import (
    RequestMagicLink,
    AuthenticateToken,
)


urlpatterns = [
    path('email/', RequestMagicLink.as_view(), name='magic_link_email'),
    path('token/', AuthenticateToken.as_view(), name='magic_link_token'),
]
