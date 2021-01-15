"""
SMS backend for usage in a test environment.
"""
from typing import List

import sms
from sms.backends.base import BaseSmsBackend
from sms.message import Message


class SmsBackend(BaseSmsBackend):
    """
    An SMS backend for use during test session.

    The test connection stores text messages in a dummy outbox, rather than
    sending them out on the wire.

    The dummy outbox is accessible through the outbox instance attribute.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not hasattr(sms, 'outbox'):
            sms.outbox = []  # type: ignore

    def send_messages(self, messages: List[Message]) -> int:
        """Redirect messages to the dummy outbox."""
        msg_count: int = 0
        for message in messages:
            sms.outbox.append(message)  # type: ignore
            msg_count += 1
        return msg_count
