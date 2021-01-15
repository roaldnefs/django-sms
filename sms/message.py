from typing import Type, Optional, List, TYPE_CHECKING

from django.conf import settings  # type: ignore


if TYPE_CHECKING:
    from sms.backends.base import BaseSmsBackend


class Message:
    """A container for text message information."""
    def __init__(
        self,
        body: str = '',
        from_phone: Optional[str] = None,
        to: Optional[List[str]] = None,
        connection: Optional[Type['BaseSmsBackend']] = None
    ) -> None:
        """
        Initialize a single text message (which can be sent to multiple
        recipients).
        """
        if to:
            if isinstance(to, str):
                raise TypeError('"to" argument must be a list or tuple')
            self.to = list(to)
        else:
            self.to = []
        self.from_phone = from_phone or getattr(
            settings, 'DEFAULT_FROM_SMS', ''
        )
        self.body = body or ''
        self.connection = connection

    def get_connection(
        self,
        fail_silently: bool = False
    ) -> Type['BaseSmsBackend']:
        from sms import get_connection
        if not self.connection:
            self.connection = get_connection(fail_silently=fail_silently)
        return self.connection

    def send(self, fail_silently: bool = False) -> int:
        """
        Send the text messages return and the number of messages sent.
        """
        if not self.to:
            # Don't brother creating the network connection if there's nobody
            # to send the text message to
            return 0
        connection: Type['BaseSmsBackend'] = self.get_connection(fail_silently)
        return connection.send_messages([self])  # type: ignore
