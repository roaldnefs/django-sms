# Django SMS

[![PyPI](https://img.shields.io/pypi/v/django-sms?color=156741&logo=python&logoColor=ffffff&style=for-the-badge)](https://pypi.org/project/django-sms/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/roaldnefs/django-sms/tests?color=156741&label=CI&logo=github&style=for-the-badge)](https://github.com/roaldnefs/django-sms/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-sms?color=156741&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/django-sms/)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-sms?color=156741&logo=django&logoColor=ffffff&style=for-the-badge)](https://pypi.org/project/django-sms/)

**django-sms** is a Django app for sending SMS with interchangeable backends. The module is heavily based upon and structured the same way as the `django.core.mail` module.

- [Sending SMS](#sending-sms)
    - [Quick example](#quick-example)
    - [send_sms()](#send_sms)
    - [Examples](#examples)
    - [The **Message** class](#the-message-class)
        - [Message Objects](#message-objects)
    - [SMS backends](#sms-backends)
        - [Obtaining an instance of an SMS backend](#obtaining-an-instance-of-an-sms-backend)
            - [Console backend](#console-backend)
            - [File backend](#file-backend)
            - [In-memory backend](#in-memory-backend)
            - [Dummy backend](#dummy-backend)
        - [Defining a custom SMS backend](#defining-a-custom-sms-backend)
- [Acknowledgement](#acknowledgement)

## Sending SMS

These wrappers are provided to make sending SMS extra quick, to help test SMS sending during development, and to provide additional SMS gateways.

### Quick example

In two lines:

```python
from sms import send_sms

send_sms(
    'Here is the message',
    '+12065550100',
    ['+441134960000'],
    fail_silently=False
)
```

The text messages are sent using one of the configured [SMS backends](#sms-backends).

### send_sms()

**send_sms(_body, from_phone, to, fail_silently=False, connection=None_)**

In most cases, you can send text messages using **sms.send_sms()**.

The **message**, **from_phone** and **to** parameters are required.

- **message**: A string.
- **from_phone**: A string. If **None**, django-sms will use the **DEFAULT_FROM_SMS** setting.
- **to**: A list of strings, each an phone number.
- **fail_silently**: A boolean. When it's **False**, **send_sms()** will raise an exception if an error occurs. See the [SMS backends](#sms-backends) documentation for a list of possible exceptions.
- **connection**: The optional SMS backend to use to send the text message. If unspecified, an instance of the default backend will be used. See the documentation of [SMS backends](#sms-backends) for more details.

The return value will be the number of successfully delivered text messages.

## Examples

This sends a text message to _+44 113 496 0000_ and _+44 113 496 0999_:

```python
send_sms(
    'Here is the message',
    '+12065550100',
    ['+441134960000', '+441134960999']
)
```

### The **Message** class

django-sms' **send_sms()** function is  actually a thin wrapper that makes use of the **Message** class.

Not all features of the **Message** class will be available though the **send_sms()** and related wrapper functions. If you wish to use advanced features, you'll need to create **Message** instances directly.

**Note**: This is a design feature. **send_sms()** was originally the only interfaces django-sms provided.

**Message** is responsible for creating the text message itself. The SMS backend is then responsible for sending the SMS.

For convenience, *Message** provides a **send()** method for sending a single text message. If you need to send multiple text messages, the SMS backend API provides alternatives.

#### Message Objects

**_class_ Message**

The **Message** class is initialized with the following parameters (in the given order, if positional arguments are used). All parameters are optional and can be set at any time prior to calling the **send()** method.

- **body**: The body text. This should be a plain text message.
- **from_phone**:
- **to**: A list or tuple of recipient phone numbers.
- **connection**: An SMS backend instance. Use this parameter if you want to use the same connection for multiple text messages. If omitted, a new connection is created when **send()** is called.

For example:

```python
from sms import Message

message = Message(
    'Here is the message',
    '+12065550100',
    ['+441134960000']
)
```

The class has the following methods:

- **send(fail_silently=False)** sends the text message. If a connection was specified when the text message was constructed, that connection will be used. Otherwise, an instance of the default backend will be instantiated and used. If the keyword argument **fail_silently** is **True**, exceptions raised while sending the text messages will be quashed. An empty list of recipients will not raise an exception.

### SMS backends

The actual sending of an SMS is handled by the SMS backend.

The SMS backend class has the following methods:

- **open()** instantiates a long-lived SMS-sending connection.
- **close()** closes the current SMS-sending connection.

It can also be used as a context manager, which will automatically call **open()** and **close()** as needed:

```python
import sms

with sms.get_connection() as connection:
    sms.Message(
        'Here is the message', '+12065550100', ['+441134960000'],
        connection=connection
    ).send()
    sms.Message(
        'Here is the message', '+12065550100', ['+441134960000'],
        connection=connection
    ).send()
```

### Obtaining an instance of an SMS backend

The **sms.get_connection()** function in **sms** returns an instance of the SMS backend that you can use.

**get_connection(_backend=None, fail_silently=False, *args, **kwargs_)**

By default, a call to **get_connection()** will return an instance of the SMS backend specified in **SMS_BACKEND**. If you specify the **backend** argument, an instance of that backend will be instantiated.

The **fail_silently** argument controls how the backend should handle errors. If **fail_silently** is True, exceptions during the SMS sending process will be silently ignored.

All other arguments are passed directly to the constructor of the SMS backend.

django-sms ships with several SMS sending backends. Some of these backends are only useful during testing and development. If you have special SMS sending requirements, you can [write your own SMS backend](#defining-a-custom-sms-backend).

#### Console backend

Instead of sending out real text messages the console backend just writes the text messages that would be sent to the standard output. By default, the console backend writes to **stdout**. You can use a different stream-like object by providing the **stream** keyword argument when constructing the connection.

```python
SMS_BACKEND = 'sms.backends.console.SmsBackend'
```

This backend is not intended for use in production - it is provided as a convenience that can be used during development.

#### File backend

The file backend writes text messages to a file. A new file is created for each session that is opened on this backend. The directory to which the files are written is either taken from the **SMS_FILE_PATH** setting or file the **file_path** keyword when creating a connection with **get_connection()**.

To specify this backend, put the following in your settings:

```python
SMS_BACKEND = 'sms.backends.filebased.SmsBackend'
SMS_FILE_PATH = '/tmp/app-messages' # change this to a proper location
```

This backend is not intended for use in production - it is provided as a convenience that can be used during development.

#### In-memory backend

The **'locmen'** backend stores text messages in a special attribute of the **sms** module. The **outbox** attribute is created when the first message is sent. It's a list with an **Message** instance of each text message that would be sent.

To specify this backend, put the following in your settings:

```python
SMS_BACKEND = 'sms.backends.locmem.SmsBackend'
```

This backend is not intended for use in production - it is provided as a convenience that can be used during development.

#### Dummy backend

As the name suggests the dummy backend does nothing with your text messages. To specify this backend, put the following in your settings:

```python
SMS_BACKEND = 'sms.backends.dummy.SmsBackend'
```

This backend is not intended for use in production - it is provided as a convenience that can be used during development.

### Defining a custom SMS backend

If you need to change how text messages are sent you can write your own SMS backend. The **SMS_BACKEND** setting in your settings file is then the Python import path for you backend class.

Custom SMS backends should subclass **BaseSmsBackend** that is located in the **sms.backends.base** module. A custom SMS backend must implement the **send_messages(messages)** method. This methods receives a list of **Message** instances and returns the number of successfully delivered messages. If your backend has any concept of a persistent session or connection, you should also implement **open()** and **close()** methods. Refer to one of the existing SMS backends for a reference implementation.

## Acknowledgement

This project is heavily based upon the **django.core.mail** module, with the modified work by [Roald Nefs](https://github.com/roaldnefs). The [Django license](https://raw.githubusercontent.com/roaldnefs/django-sms/main/LICENSE.django) is included with **django-sms**.
