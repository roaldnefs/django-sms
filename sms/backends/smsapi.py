"""
SMS backend for sending text messages using service SMSAPI.pl

Requires:
 - https://github.com/smsapi/smsapi-python-client
 - SMSAPI_TOKEN to be set
"""
from typing import List, Optional

from django.conf import settings  # type: ignore
from django.core.exceptions import ImproperlyConfigured  # type: ignore
from sms.backends.base import BaseSmsBackend
from sms.message import Message

try:
    from smsapi.client import SmsApiPlClient  # type: ignore
    HAS_SMSAPI = True
except ImportError:
    HAS_SMSAPI = False


class SmsBackend(BaseSmsBackend):
    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)

        if not HAS_SMSAPI and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.smsapi.SmsBackend' without having "
                "'smsapi-client' installed. Install 'smsapi-client' or use "
                "another SMS backend."
            )

        access_key: Optional[str] = getattr(settings, 'SMSAPI_TOKEN')
        if not access_key and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.smsapi.SmsBackend' without having the "
                "setting 'SMSAPI_TOKEN' set."
            )

        self.client = None
        if HAS_SMSAPI:
            self.client = SmsApiPlClient(access_token=access_key)

    def send_messages(self, messages: List[Message]) -> int:
        if not self.client:
            return 0

        msg_count: int = 0
        for message in messages:
            for recipient in message.recipients:
                try:
                    message.send_results = self.client.sms.send(
                        to=recipient,
                        message=message.body
                    )
                except Exception as exc:
                    if not self.fail_silently:
                        raise exc
                msg_count += 1
        return msg_count
