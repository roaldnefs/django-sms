from typing import List, Optional

from django.conf import settings  # type: ignore
from django.core.exceptions import ImproperlyConfigured  # type: ignore

from sms.backends.base import BaseSmsBackend

try:
    import boto3  # type: ignore
    from botocore.exceptions import ClientError  # type: ignore

    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


class SmsBackend(BaseSmsBackend):
    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)

        if not HAS_BOTO3 and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.aws.SmsBackend' without having "
                "'boto3' installed. Install 'boto3' or use "
                "another SMS backend."
            )

        region_name: Optional[str] = getattr(settings, 'AWS_SNS_REGION')
        if region_name is None and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.aws.SmsBackend' without having the "
                "setting 'AWS_SNS_REGION' set."
            )

        access_key_id: Optional[str] = getattr(settings, 'AWS_SNS_ACCESS_KEY_ID')
        if access_key_id is None and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.aws.SmsBackend' without having the "
                "setting 'AWS_SNS_ACCESS_KEY_ID' set."
            )

        access_key: Optional[str] = getattr(settings, 'AWS_SNS_SECRET_ACCESS_KEY')
        if access_key is None and not self.fail_silently:
            raise ImproperlyConfigured(
                "You're using the SMS backend "
                "'sms.backends.aws.SmsBackend' without having the "
                "setting 'AWS_SNS_SECRET_ACCESS_KEY' set."
            )

        self.sns_resource = None
        if HAS_BOTO3:
            self.sns_resource = boto3.resource(
                'sns',
                region_name=region_name,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_key,
            )

    def send_messages(self, messages: List[Message]) -> int:
        if self.sns_resource is None:
            return 0

        msg_count: int = 0
        for message in messages:
            for recipient in message.recipients:
                try:
                    self.sns_resource.meta.client.publish(
                        PhoneNumber=recipient,
                        Message=message.body,
                        MessageAttributes={
                            'AWS.SNS.SMS.SenderID': {
                                'DataType': 'String',
                                'StringValue': getattr(
                                    settings, 'AWS_SNS_SENDER_ID', 'django-sms'
                                ),
                            },
                            'AWS.SNS.SMS.SMSType': {
                                'DataType': 'String',
                                'StringValue': getattr(
                                    settings, 'AWS_SNS_SMS_TYPE', 'Promotional'
                                ),
                            },
                            'AWS.MM.SMS.OriginationNumber': {
                                'DataType': 'String',
                                'StringValue': message.originator,
                            },
                        },
                    )
                except (ClientError, AssertionError):
                    if not self.fail_silently:
                        raise
                msg_count += 1
        return msg_count
