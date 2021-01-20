import os
import sys
import shutil
import tempfile

from typing import List, Type, Optional
from io import StringIO

from django.test import SimpleTestCase, override_settings  # type: ignore

import sms
from sms import send_sms
from sms.backends import dummy, locmem, filebased
from sms.backends.base import BaseSmsBackend
from sms.message import Message
from sms.utils import message_from_bytes, message_from_binary_file


class BaseSmsBackendTests:
    sms_backend: Optional[str] = None

    def setUp(self) -> None:
        self.settings_override = override_settings(
            SMS_BACKEND=self.sms_backend
        )
        self.settings_override.enable()

    def tearDown(self) -> None:
        self.settings_override.disable()


class SmsTests(SimpleTestCase):

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
        """Test backend argument of sms.get_connection()."""
        self.assertIsInstance(
            sms.get_connection('sms.backends.dummy.SmsBackend'),
            dummy.SmsBackend
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.assertIsInstance(
                sms.get_connection(
                    'sms.backends.filebased.SmsBackend',
                    file_path=tmp_dir
                ),
                filebased.SmsBackend
            )
        if sys.platform == 'win32':
            msg = ('_getfullpathname: path should be string, bytes or '
                   'os.PathLike, not object')
        else:
            msg = 'expected str, bytes or os.PathLike object, not object'
        with self.assertRaisesMessage(TypeError, msg):
            sms.get_connection(
                'sms.backends.filebased.SmsBackend',
                file_path=object()
            )
        self.assertIsInstance(sms.get_connection(), locmem.SmsBackend)

    def test_custom_backend(self) -> None:
        """Test cutoms backend defined in this suite."""
        connection = sms.get_connection('tests.custombackend.SmsBackend')
        self.assertTrue(hasattr(connection, 'test_outbox'))
        message = Message('Content', '0600000000', ['0600000000'])
        connection.send_messages([message])  # type: ignore
        self.assertEqual(len(connection.test_outbox), 1)  # type: ignore

    @override_settings(SMS_BACKEND='sms.backends.locmem.SmsBackend')
    def test_send_sms(self) -> None:
        """
        Test send_sms with the to specified as a string to remain compatibility
        with django-sms<=0.0.4.
        """
        send_sms('Content', '0600000000', '0600000000')
        self.assertEqual(len(sms.outbox), 1)  # type: ignore
        self.assertIsInstance(sms.outbox[0].to, list)  # type: ignore


class LocmemBackendTests(BaseSmsBackendTests, SimpleTestCase):
    sms_backend: str = 'sms.backends.locmem.SmsBackend'

    def flush_mailbox(self) -> None:
        sms.outbox = []  # type: ignore

    def tearDown(self) -> None:
        super().tearDown()
        self.flush_mailbox()

    def test_locmem_shared_messages(self) -> None:
        """
        Make sure that the locmem backend populates the outbox.
        """
        connections: List[Type[BaseSmsBackend]] = [
            locmem.SmsBackend(),  # type: ignore
            locmem.SmsBackend()  # type: ignore
        ]
        message = Message('Content', '0600000000', ['0600000000'])
        for connection in connections:
            connection.send_messages([message])  # type: ignore
        self.assertEqual(len(sms.outbox), 2)  # type: ignore


class ConsoleBackendTests(BaseSmsBackendTests, SimpleTestCase):
    sms_backend: str = 'sms.backends.console.SmsBackend'

    def test_console_stream_kwarg(self) -> None:
        """
        The console backend can be pointed at an arbitrary stream.
        """
        stream = StringIO()
        connection = sms.get_connection(
            'sms.backends.console.SmsBackend',
            stream=stream
        )
        message = Message('Content', '0600000000', ['0600000000'])
        connection.send_messages([message])  # type: ignore
        messages = stream.getvalue().split('\n' + ('-' * 79) + '\n')
        self.assertIn('from: ', messages[0])


class FileBasedBackendTests(BaseSmsBackendTests, SimpleTestCase):
    sms_backend = 'sms.backends.filebased.SmsBackend'

    def setUp(self) -> None:
        super().setUp()
        self.tmp_dir = self.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp_dir)
        self._settings_override = override_settings(SMS_FILE_PATH=self.tmp_dir)
        self._settings_override.enable()

    def tearDown(self) -> None:
        self._settings_override.disable()
        super().tearDown()

    def mkdtemp(self) -> str:
        return tempfile.mkdtemp()

    def flush_mailbox(self) -> None:
        for filename in os.listdir(self.tmp_dir):
            os.unlink(os.path.join(self.tmp_dir, filename))

    def get_mailbox_content(self) -> List[Message]:
        messages: List[Message] = []
        for filename in os.listdir(self.tmp_dir):
            with open(os.path.join(self.tmp_dir, filename), 'rb') as fp:
                session = fp.read().split(b'\n' + (b'-' * 79) + b'\n')
            messages.extend(message_from_bytes(m) for m in session if m)
        return messages

    def test_file_sessions(self) -> None:
        """Make sure opening a connection creates a new file"""
        message = Message(
            'Here is the message',
            '+12065550100',
            ['+441134960000']
        )
        connection = sms.get_connection()
        connection.send_messages([message])  # type: ignore

        self.assertEqual(len(os.listdir(self.tmp_dir)), 1)
        tmp_file = os.path.join(self.tmp_dir, os.listdir(self.tmp_dir)[0])
        with open(tmp_file, 'rb') as fp:
            message = message_from_binary_file(fp)
        self.assertEqual(message.from_phone, '+12065550100')
        self.assertEqual(message.to, ['+441134960000'])
