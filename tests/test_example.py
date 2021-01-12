from django.test import SimpleTestCase  # type: ignore

import sms
from sms.backends import dummy
from sms.message import Message


class ExampleTests(SimpleTestCase):

    def test_dummy_backend(self) -> None:
        """
        Make sure that dummy backends return correct number of sent text
        messages.
        """
        connection = dummy.SmsBackend()
        message = Message()
        self.assertEqual(
            connection.send_messages([message, message, message]),
            3
        )

    def test_backend_arg(self) -> None:
        """Test backend argument of mail.get_connection()."""
        self.assertIsInstance(
            sms.get_connection('sms.backends.dummy.SmsBackend'),
            dummy.SmsBackend
        )
