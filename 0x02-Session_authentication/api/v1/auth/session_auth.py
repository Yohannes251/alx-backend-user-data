#!/usr/bin/env python3
"""
    This module contains SessionAuth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """Implements Session authentication system"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session_id for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user_id based on session_id"""
        if session_id is None or type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
       """Returns the current user object"""

       session_id = self.session_cookie(request)
       user_id = self.user_id_for_session_id(session_id)
       print(user_id)
       user = User.get(user_id)
       return user
