#!/usr/bin/env python
"""
Generate a Django secret key without requiring Django to be installed.
This uses Python's built-in secrets module.
"""
import secrets
import string

# Django secret key uses these characters
chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(chars) for _ in range(50))

print(secret_key)

