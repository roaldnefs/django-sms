"""
SMS backend for sending text messages using MessageBird.
"""
import json

from typing import Dict, List, Any, Optional, Union

from django.conf import settings  # type: ignore

from sms.backends.base import BaseSmsBackend
from sms.message import Message
from sms._http_client import HttpClient


ENDPOINT = 'https://rest.messagebird.com/'
MESSAGEBIRD_ACCESS_TOKEN = getattr(settings, 'MESSAGEBIRD_ACCESS_TOKEN', '')


class Client:
    def __init__(self, access_key: str, http_client: Optional[HttpClient] = None) -> None:
        self.access_key = access_key
        self.http_client = http_client

    def _get_http_client(self) -> HttpClient:
        if self.http_client:
            return self.http_client

        headers = {
            'Accept': 'application/json',
            'Authorization': 'AccessKey ' + self.access_key,
            'Content-Type': 'application/json'
        }
        return HttpClient(ENDPOINT, headers)

    def request(
        self,
        path: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        response_text = self._get_http_client().request(path, method, params)
        if not response_text:
            return response_text

        response_json = json.loads(response_text)

        # TODO(roaldnefs): Check for errors in the response
        if 'errors' in response_json:
            pass

        return response_json

    def message_create(
        self, originator: str,
        recipients: Union[str, List[str]],
        body: str,
        params: Optional[Dict[str, Any]]=None
    ) -> Any:
        """Create a new text message."""
        if params is None:
            params = {}
        if type(recipients) == list:
            recipients = ','.join(recipients)

        params.update({
            'originator': originator,
            'body': body,
            'recipients': recipients
        })
        return self.request('messages', 'POST', json.dumps(params).encode('utf-8')) 


class SmsBackend(BaseSmsBackend):
    def send_messages(self, messages: List[Message]) -> int:
        client = Client(MESSAGEBIRD_ACCESS_TOKEN)

        msg_count: int = 0
        for message in messages:
            res = client.message_create(
                message.originator,
                message.recipients,
                message.body
            )
            msg_count += 1
        return msg_count
