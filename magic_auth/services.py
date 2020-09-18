import logging

from django.core.mail import send_mail
from django.template import loader

from .exceptions import (UserNotFoundException,
                         UserInactiveException,
                         MagicLinkException,
                         TokenAllocationException,
                         InvalidKeyException)
from .models import MagicLinkCredential
from .settings import api_settings
from .utils import (get_user_for_email,
                    get_magic_link,
                    inject_template_context,
                    check_hashed_key,
                    check_credential_expiry,
                    authenticate_user)

logger = logging.getLogger(__name__)


def email_link(user,
               request_source,
               go_next=None,
               email_subject=api_settings.MAGIC_LINKS_EMAIL_SUBJECT,
               email_plaintext=api_settings.MAGIC_LINKS_EMAIL_PLAINTEXT_MESSAGE,
               email_html=api_settings.MAGIC_LINKS_EMAIL_HTML_TEMPLATE_NAME,
               **kwargs
               ):
    link = get_magic_link(user=user, request_source=request_source, go_next=go_next)

    if link:
        try:
            if api_settings.MAGIC_LINKS_EMAIL_FROM_ADDRESS:
                context = inject_template_context({'link': link})
                html_message = loader.render_to_string(email_html, context, )

                send_mail(
                    email_subject,
                    email_plaintext.format(link=link),
                    api_settings.MAGIC_LINKS_EMAIL_FROM_ADDRESS,
                    [getattr(user, api_settings.MAGIC_LINKS_USER_EMAIL_FIELD_NAME)],
                    fail_silently=False,
                    html_message=html_message,
                )

            else:
                logger.debug("Nothing specified for MAGIC_LINKS_EMAIL_FROM_ADDRESS.")
                return False
            return True

        except Exception as e:
            logger.debug(e)
            return False

        return success

    return logger.debug("Could not generate link.")


def send_magic_link(email, request_source='default', go_next=None):
    user = get_user_for_email(email)

    if not user:
        raise UserNotFoundException

    if not user.is_active:
        raise UserInactiveException

    success = email_link(user, request_source, go_next=go_next)

    email_link(user, request_source, go_next=go_next)

    if not success:
        raise MagicLinkException

    return True


def validate_credential(email, callback_token):
    try:
        credential = MagicLinkCredential.objects.get(user__email=email, is_active=True)


        if check_credential_expiry(credential):
            import q
            q('truuuuuu')
            valid = check_hashed_key(str(credential.key), callback_token)
            if valid:
                import q
                q("sdsdsd")
                credential.is_active = False
                credential.save()
                return credential
            return None
        else:
            import q
            q('error')
            return None

    except MagicLinkCredential.DoesNotExist:
        return None


def get_user_from_callback_token(email, callback_token):
    credential = validate_credential(email, callback_token)

    if not credential:
        raise InvalidKeyException

    user = credential.user

    if not user.is_active:
        raise UserInactiveException

    return user


def authenticate_token(email, callback_token):
    user = get_user_from_callback_token(email, callback_token)
    token = authenticate_user(user)

    if not token:
        raise TokenAllocationException

    return token
