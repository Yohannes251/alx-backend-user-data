#!/usr/bin/env python3
"""
    This module implements authorization
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Encrypts passwod using bcrypt module"""
    pwd = bytes(password, 'utf-8')
    return hashpw(pwd, gensalt())


def _generate_uuid() -> str:
    """Returns a uuid value"""

    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """Returns a string format of session id"""

        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)

            return sess_id
        except Exception:
            return None
