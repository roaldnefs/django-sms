"""
SMS backend for sending text messages using sms77.
"""
from typing import List, Optional

from django.conf import settings  # type: ignore
from django.core.exceptions import ImproperlyConfigured  # type: ignore

from sms.backends.base import BaseSmsBackend
from sms.message import Message

try:
    from sms77api.Sms77api import Sms77api  # type: ignore
    HAS_SMS77 = True
except ImportError:
    HAS_SMS77 = False


class SmsBackend(BaseSmsBackend):
    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)

        if not HAS_SMS77 and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.sms77.SmsBackend' without having "
                "'sms77' installed. Install 'sms77' or use "
                "another SMS backend."
            )

        api_key: Optional[str] = getattr(settings, 'SMS77_API_KEY')
        if not api_key and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.sms77.SmsBackend' without having the "
                "setting 'SMS77_API_KEY' set."
            )

        self.client = None
        if HAS_SMS77:
            self.client = Sms77api(api_key, 'Django-SMS')

    def send_messages(self, messages: List[Message]) -> int:
        if not self.client:
            return 0

        msg_count: int = 0
        for message in messages:
            try:
                self.client.sms(
                    message.recipients,
                    message.body,
                    {'from': message.originator}
                )
            except Exception as exc:
                if not self.fail_silently:
                    raise exc
            msg_count += 1
        return msg_count
