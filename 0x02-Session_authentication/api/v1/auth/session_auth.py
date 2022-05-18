#!/usr/bin/env python3
"""
    This module contains SessionAuth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Implements Session authentication system"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session_id for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
