#!/usr/bin/env python3
"""
    This module contains BasicAuth class that inherits from Auth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """This class implements Basic Authorization system"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header or None"""
        auth_head = authorization_header
        if auth_head is None or type(auth_head) != str:
            return None
        splited_header = list(auth_head.split())
        if splited_header[0] != 'Basic':
            return None
        return splited_header[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Returns the decoded value of a Base64 string"""
        data = base64_authorization_header
        if data is None or type(data) != str:
            return None
        try:
            return base64.b64decode(data, validate=True).decode('UTF8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Returns user e-mail and password from the decoded Base64 string"""
        decoded = decoded_base64_authorization_header

        if decoded is None or type(decoded) != str or ':' not in decoded:
            return None, None
        output = decoded.split(':')
        return output[0], output[1]

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """Returns User instance based on email and password"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        users = User()
        user = users.search(attributes={"email": user_email})
        if user:
            if user[0].is_valid_password(user_pwd):
                return user[0]
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrives the User instance for a request"""
        auth_header = self.authorization_header(request)
        encoded = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(encoded)
        user_credentials = self.extract_user_credentials(decoded)
        user_name, user_pwd = user_credentials[0], user_credentials[1]
        return self.user_object_from_credentials(user_name, user_pwd)
