from typing import Type, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from sms.backends.base import BaseSmsBackend


class Message:
    """A container for text message information."""
    def __init__(
        self,
        body: str = '',
        from_: Optional[str] = None,
        to: Optional[str] = None,
        connection: Optional[Type['BaseSmsBackend']] = None
    ) -> None:
        """
        Initialize a single text message (which can be sent to multiple
        recipients).
        """
        self.connection = connection
        self.body = body
        self.from_ = from_
        self.to = to

    def get_connection(
        self,
        fail_silently: bool = False
    ) -> Type['BaseSmsBackend']:
        from sms import get_connection
        if not self.connection:
            self.connection = get_connection(fail_silently=fail_silently)
        return self.connection

    def send(self, fail_silently: bool = False):
        """Send the text message."""
        connection: Type['BaseSmsBackend'] = self.get_connection(fail_silently)
        return connection.send_messages([self])  # type: ignore
