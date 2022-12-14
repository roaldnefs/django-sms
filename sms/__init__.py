"""
Tools for sending text messages.
"""
from typing import List, Optional, Type, Union

from django.conf import settings  # type: ignore
from django.utils.module_loading import import_string  # type: ignore

from sms.backends.base import BaseSmsBackend
from sms.message import Message

__all__ = [
    'Message', 'get_connection', 'send_sms'
]


def get_connection(
    backend: Optional[str] = None,
    fail_silently: bool = False,
    **kwargs
) -> Type[BaseSmsBackend]:
    """Load a SMS backend and return an instance of it.

    If backend is None (default), use settings.SMS_BACKEND.

    Both fail_silently and other keyword arguments are used in the constructor
    of the backend.
    """
    klass = import_string(backend or settings.SMS_BACKEND)
    return klass(fail_silently=fail_silently, **kwargs)


def send_sms(
    body: str = '',
    originator: Optional[str] = None,
    recipients: Union[Optional[str], Optional[List[str]]] = None,
    fail_silently: bool = False,
    connection: Optional[Type['BaseSmsBackend']] = None
) -> int:
    """
    Easy wrapper for sending a single message to a recipient list.

    Allow to to be a string, to remain compatibility with older
    django-sms<=0.0.4.

    If originator is None, use DEFAULT_FROM_SMS setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should the the Message class directly.
    """
    if isinstance(recipients, str):
        recipients = [recipients]
    msg = Message(body, originator, recipients, connection=connection)
    return msg.send(fail_silently=fail_silently)
