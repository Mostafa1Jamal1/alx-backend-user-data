#!/usr/bin/env python3
"""BasicAuth module
"""

from .auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        """
        if (authorization_header is not None and
                type(authorization_header) == str and
                authorization_header[:6] == 'Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode value of a Base64 string base64_authorization_header
        """
        if (base64_authorization_header is not None and
                type(base64_authorization_header) == str):
            try:
                binary_like = base64_authorization_header.encode('utf-8')
                decoded64 = b64decode(binary_like)
                return decoded64.decode('utf-8')
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value.
        """
        if (decoded_base64_authorization_header is not None and
                type(decoded_base64_authorization_header) == str and
                ':' in decoded_base64_authorization_header):
            splited = decoded_base64_authorization_header.split(':')
            return (splited[0], splited[1])
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password.
        """
        if (
            user_email is not None and
            user_pwd is not None and
            type(user_email) == str and
            type(user_pwd) == str and
            len(User.search({'email': user_email})) > 0
        ):
            user = User.search({'email': user_email})[0]
            return user if user.is_valid_password(user_pwd) else None
        return None
