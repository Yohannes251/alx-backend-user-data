#!/usr/bin/env python3
"""
    This module implements authorization
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Encrypts passwod using bcrypt module"""
    pwd = bytes(password, 'utf-8')
    return hashpw(pwd, gensalt())


class Auth:
    """Implements authentication of users"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Handles user registration"""

        try:
            check_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks recieved user credentials"""

        try:
            user = self._db.find_user_by(email=email)
            if checkpw(bytes(password, 'utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False
