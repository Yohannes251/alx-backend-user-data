#!/usr/bin/env python3
"""
    This module implements authorization
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Encrypts passwod using bcrypt module"""
    pwd = bytes(password, 'utf-8')
    return hashpw(pwd, gensalt())
