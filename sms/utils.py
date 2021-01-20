import re

from sms.message import Message


header_RE = re.compile('^(?:from|to): .*')
header_from_RE = re.compile('^from: (.*)$', re.MULTILINE)
header_to_RE = re.compile('^to: (.*)$', re.MULTILINE)


def message_from_binary_file(fp) -> Message:
    """Parse a binary file into a Message object model."""
    return message_from_bytes(fp.read())


def message_from_bytes(s: bytes) -> Message:
    """Parse a bytes string into a Message object model."""
    text = s.decode('ASCII', errors='surrogateescape')

    body = ''
    for line in text.splitlines():
        if not header_RE.match(line):
            if body is not None:
                body += '\n' + line
            else:
                body = line

    from_result = header_from_RE.search(text)
    if from_result:
        from_phone = from_result.group(1)
    else:
        raise ValueError

    to_result = header_to_RE.search(text)
    if to_result:
        to = [to_result.group(1)]
    else:
        raise ValueError

    return Message(body, from_phone, to)
