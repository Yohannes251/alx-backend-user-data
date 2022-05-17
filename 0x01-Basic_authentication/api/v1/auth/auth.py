#!/usr/bin/python3
"""
    This module contains Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Implements authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns a boolean"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns a string"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns user"""
        return None
