from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MagicAuthConfig(AppConfig):
    name = 'magic_auth'
    verbose_name = _('Магический доступ')
