"""
SMS backend that writes messages to a file.
"""
import datetime
import os

from typing import Optional

from django.conf import settings  # type: ignore
from django.core.exceptions import ImproperlyConfigured  # type: ignore

from sms.backends.console import SmsBackend as BaseSmsBackend
from sms.message import Message


class SmsBackend(BaseSmsBackend):
    def __init__(
        self,
        *args,
        file_path: Optional[str] = None,
        **kwargs
    ) -> None:
        self._fname: Optional[str] = None
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = getattr(settings, 'SMS_FILE_PATH', None)
        self.file_path = os.path.abspath(self.file_path)
        try:
            os.makedirs(self.file_path, exist_ok=True)
        except FileExistsError:
            raise ImproperlyConfigured((
                'Path for saving text messages exists, but is not a '
                f'directory: {self.file_path}'
            ))
        except OSError as exc:
            raise ImproperlyConfigured((
                'Could not create directory for saving text messages: '
                f'{self.file_path} ({exc})'
            ))
        # Make sure that self.file_path is writable.
        if not os.access(self.file_path, os.W_OK):
            raise ImproperlyConfigured(
                f'Could not write to directory: {self.file_path}'
            )
        # Finally, call super().
        # Since we're using the console-based backend as a base,
        # force the stream to be None, so we don't default to stdout
        kwargs['stream'] = None
        super().__init__(*args, **kwargs)

    def write_message(self, message: Message) -> int:
        msg_count = 0
        for to in message.to:
            msg_data = (
                f"from: {message.from_phone}\n"
                f"to: {to}\n"
                f"{message.body}"
            )
            self.stream.write(f'{msg_data}\n'.encode())
            self.stream.write(b'-' * 79)
            self.stream.write(b'\n')
            msg_count += 1
        return msg_count

    def _get_filename(self) -> str:
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fname = "%s-%s.log" % (timestamp, abs(id(self)))
            self._fname = os.path.join(self.file_path, fname)
        return self._fname

    def open(self) -> bool:
        if self.stream is None:
            self.stream = open(self._get_filename(), 'ab')
            return True
        return False

    def close(self) -> None:
        try:
            if self.stream is not None:
                self.stream.close()
        finally:
            self.stream = None
