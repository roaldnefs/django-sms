import urllib

from typing import Optional, Any, Dict


# TODO(roaldnefs): Add user agent for django-sms
USER_AGENT = ''


class HttpClient:
    def __init__(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> None:
        self.endpoint = endpoint
        self.headers = headers
        self.user_agent = USER_AGENT

    def request(
        self,
        path: str,
        method: str = 'GET',
        data: Optional[bytes] = None
    ) -> str:
        url = urllib.parse.urljoin(self.endpoint, path)

        headers = {'User-Agent': self.user_agent}
        if self.headers:
            headers.update(self.headers)

        request = urllib.request.Request(url, data=data, method=method)
        for key, value in headers.items():
            request.add_header(key, value)

        response = urllib.request.urlopen(request)
        response_text = response.read()

        return response_text
