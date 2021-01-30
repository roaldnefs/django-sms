"""
SMS backend that writes text messages to console instead of sending them.
"""
import sys
import threading

from typing import List

from sms.backends.base import BaseSmsBackend
from sms.message import Message


class SmsBackend(BaseSmsBackend):
    def __init__(self, *args, **kwargs) -> None:
        self.stream = kwargs.pop('stream', sys.stdout)
        self._lock = threading.RLock()
        super().__init__(*args, **kwargs)

    def write_message(self, message: Message) -> int:
        msg_count = 0
        for recipient in message.recipients:
            msg_data = (
                f"from: {message.originator}\n"
                f"to: {recipient}\n"
                f"{message.body}"
            )
            self.stream.write(f'{msg_data}\n')
            self.stream.write('-' * 79)
            self.stream.write('\n')
            msg_count += 1
        return msg_count

    def send_messages(self, messages: List[Message]) -> int:
        """Write all text messages to the stream in a thread-safe way."""
        msg_count: int = 0
        if not messages:
            return msg_count
        with self._lock:
            try:
                stream_created = self.open()
                for message in messages:
                    count = self.write_message(message)
                    self.stream.flush()  # flush after each message
                    msg_count += count
                if stream_created:
                    self.close()
            except Exception:
                if not self.fail_silently:
                    raise
        return msg_count
