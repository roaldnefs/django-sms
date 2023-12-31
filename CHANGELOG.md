# Changelog
All notable changes in **django-sms** are documented below.

## [Unreleased]

## [0.7.0]
### Changed
- Add support for Django 4.2 and 5.0.
- Add support for Python 3.12.

### Deprecated
- Drop support for Django 2.2, 3.1 and 4.0.
- Drop support for Python 3.6 and 3.7.

## [0.6.0]
### Changed
- Add support for Django 3.2, 4.0 and 4.1.
- Add support for Python 3.11.

### Deprecated
- Drop support for Django 3.0.

## [0.5.0]
### Added
- The **sms.backends.twilio.SmsBackend** to send text messages using [Twilio](https://twilio.com/) ([#7](https://github.com/roaldnefs/django-sms/issues/7)).

## [0.4.0]
### Added
- The **sms.backends.messagebird.SmsBackend** to send text messages using [MessageBird](https://messagebird.com/) ([#6](https://github.com/roaldnefs/django-sms/issues/6)).

### Changed
- Simplified the attributes of the **sms.signals.post_send** signal to include the instance of the originating **Message** instead of all attributes ([#11](https://github.com/roaldnefs/django-sms/pull/11)).

## [0.3.0] (2021-01-30)
### Added
- The **sms.signals.post_send** signal to let user code get notified by Django itself after **send()** is called on a **Message** instance.

## [0.2.0] (2021-01-21)
### Added
- The file backend that writes text messages to a file ([#1](https://github.com/roaldnefs/django-sms/pull/1)).

## [0.1.0] (2021-01-15)
### Added
- This `CHANGELOG.md` file to be able to list all notable changes for each version of **django-sms**.

[Unreleased]: https://github.com/roaldnefs/django-sms/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/roaldnefs/django-sms/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/roaldnefs/django-sms/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/roaldnefs/django-sms/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/roaldnefs/django-sms/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/roaldnefs/django-sms/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/roaldnefs/django-sms/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/roaldnefs/django-sms/releases/tag/v0.1.0
