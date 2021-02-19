"""
SMS backend for sending text messages using Twilio.
"""
from typing import List, Optional

from django.conf import settings  # type: ignore
from django.core.exceptions import ImproperlyConfigured  # type: ignore

from sms.backends.base import BaseSmsBackend
from sms.message import Message

try:
    from twilio.rest import Client  # type: ignore
    HAS_TWILIO = True
except ImportError:
    HAS_TWILIO = False


class SmsBackend(BaseSmsBackend):
    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)

        if not HAS_TWILIO and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.twilio.SmsBackend' without having "
                "'twilio' installed. Install 'twilio' or use "
                "another SMS backend."
            )

        account_sid: Optional[str] = getattr(settings, 'TWILIO_ACCOUNT_SID')
        if not account_sid and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.twilio.SmsBackend' without having the "
                "setting 'TWILIO_ACCOUNT_SID' set."
            )

        auth_token: Optional[str] = getattr(settings, 'TWILIO_AUTH_TOKEN')
        if not auth_token and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.twilio.SmsBackend' without having the "
                "setting 'TWILIO_AUTH_TOKEN' set."
            )

        self.client = None
        if HAS_TWILIO:
            self.client = Client(account_sid, auth_token)

    def send_messages(self, messages: List[Message]) -> int:
        if not self.client:
            return 0

        msg_count: int = 0
        for message in messages:
            for recipient in message.recipients:
                try:
                    self.client.messages.create(
                        to=recipient,
                        from_=message.originator,
                        body=message.body
                    )
                except Exception as exc:
                    if not self.fail_silently:
                        raise exc
                msg_count += 1
        return msg_count
