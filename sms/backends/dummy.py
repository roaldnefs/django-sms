"""
Dummy SMS backend that does nothing.
"""
from typing import List

from sms.backends.base import BaseSmsBackend
from sms.message import Message


class SmsBackend(BaseSmsBackend):
    def send_messages(self, messages: List[Message]) -> int:
        return len(list(messages))
