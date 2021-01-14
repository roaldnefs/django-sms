"""A custom backend for testing."""

from typing import List

from sms.backends.base import BaseSmsBackend
from sms.message import Message


class SmsBackend(BaseSmsBackend):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.test_outbox: List[Message] = []

    def send_messages(self, messages: List[Message]) -> int:
        # Messages are stored in an instance variable for testing
        self.test_outbox.extend(messages)
        return len(messages)
