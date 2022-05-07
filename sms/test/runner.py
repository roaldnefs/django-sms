import sms
from django.conf import settings
from django.test.runner import DiscoverRunner


class SMSTestRunner(DiscoverRunner):
    """A test runner that sets up the fake sms backend like Django sets
    up the fake email backend
    """
    def setup_test_environment(self, **kwargs):
        settings.SMS_BACKEND = "sms.backends.locmem.SmsBackend"
        sms.outbox = []
        super().setup_test_environment(**kwargs)
