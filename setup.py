#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def long_description() -> str:
    """
    Returns the long description containing both the README.md and CHANGELOG.md
    files.
    """
    with open('README.md') as readme_file:
        readme = readme_file.read()

    with open('CHANGELOG.md') as changelog_file:
        changelog = changelog_file.read()
    
    return readme + changelog


setup(
    name='django-sms',
    version='0.2.0',
    url="https://github.com/django-enterprise/django-sms",
    description='A Django app for sending SMS with interchangeable backends.',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Roald Nefs',
    author_email='info@roaldnefs.com',
    license='BSD-3-Clause',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    test_suite='tests.runtests.main',
    install_requires=['Django>=2.2']
)
