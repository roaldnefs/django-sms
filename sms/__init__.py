"""
Tools for sending text messages.
"""
from typing import Type

from django.conf import settings  # type: ignore
from django.utils.module_loading import import_string  # type: ignore

from sms.backends.base import BaseSmsBackend
from sms.message import Message


__all__ = [
    'Message', 'get_connection'
]


def get_connection(
    backend: str = None,
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
