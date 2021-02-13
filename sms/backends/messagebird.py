"""
SMS backend for sending text messages using MessageBird.
"""
from typing import List, Optional

from django.conf import settings  # type: ignore
from django.core.exceptions import ImproperlyConfigured  # type: ignore

from sms.backends.base import BaseSmsBackend
from sms.message import Message

try:
    import messagebird  # type: ignore
    HAS_MESSAGEBIRD = True
except ImportError:
    HAS_MESSAGEBIRD = False


class SmsBackend(BaseSmsBackend):
    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)

        if not HAS_MESSAGEBIRD and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.messagebird.SmsBackend' without having "
                "'messagebird' installed. Install 'messagebird' or use "
                "another SMS backend."
            )

        access_key: Optional[str] = getattr(settings, 'MESSAGEBIRD_ACCESS_KEY')
        if not access_key and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.messagebird.SmsBackend' without having the "
                "setting 'MESSAGEBIRD_ACCESS_KEY' set."
            )

        self.client = None
        if HAS_MESSAGEBIRD:
            self.client = messagebird.Client(access_key)

    def send_messages(self, messages: List[Message]) -> int:
        if not self.client:
            return 0

        msg_count: int = 0
        for message in messages:
            try:
                self.client.message_create(
                    message.originator,
                    message.recipients,
                    message.body
                )
            except Exception as exc:
                if not self.fail_silently:
                    raise exc
            msg_count += 1
        return msg_count
