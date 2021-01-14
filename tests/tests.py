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

    def test_custom_backend(self) -> None:
        """Test cutoms backend defined in this suite."""
        connection = sms.get_connection('tests.custombackend.SmsBackend')
        self.assertTrue(hasattr(connection, 'test_outbox'))
        message = Message('Content', '0600000000', '0600000000')
        connection.send_messages([message])  # type: ignore
        self.assertEqual(len(connection.test_outbox), 1)  # type: ignore
