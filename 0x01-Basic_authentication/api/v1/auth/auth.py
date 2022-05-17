#!/usr/bin/env python3
"""
    This module contains Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Implements authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if path is in excluded paths"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] == "/":
            path = path[:-1]
        for pat in excluded_paths:
            if path in pat:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks if Authorization key is in request header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns user"""
        return None
