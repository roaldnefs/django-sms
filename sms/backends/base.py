"""Base SMS backend class."""
from typing import Optional, Type, List
from types import TracebackType

from sms.message import Message


class BaseSmsBackend:
    """
    Base class for sms backend implementations.

    Subclasses must at least overwrite send_messages().

    open() and close() can be called indirectly by using a backend object as a
    context manager:

        with backend as connection:
            # do something with connection
            pass
    """
    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        self.fail_silently = fail_silently

    def open(self) -> bool:
        """
        Open a network connection.

        This method can be overwritten by backend implementations to open a
        network connection.

        It's up to the backend implementation to track the status of a network
        connection if it's needed by the backend.

        This method can be called by application to force a single network
        connection to be used when sending text messages.

        The default implementation does nothing.
        """
        return True

    def close(self) -> None:
        """Close a network connection."""
        pass

    def __enter__(self) -> 'BaseSmsBackend':
        try:
            self.open()
        except Exception:
            self.close()
            raise
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        self.close()

    def send_messages(
        self,
        messages: List[Message]
    ) -> int:
        """
        Send one or more Message objects and return the number of text messages
        sent.
        """
        raise NotImplementedError(
            'subclasses of BaseSmsBacked must override send_messages() method'
        )
