import sms


class SMSTestCaseMixin:
    """A TestCase mixin that sets up the fake sms backend like Django sets
    up the fake email backend
    """
    def _pre_setup(self):
        super()._pre_setup()
        sms.outbox = []
