#!/usr/bin/env python3
"""Auth module
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path
        """
        if path is not None and excluded_paths is not None:
            if path[-1] != '/':
                path = path + '/'
            if path in excluded_paths:
                return False
            for ex_path in excluded_paths:
                if ex_path[-1] == '*':
                    p_path = path[:(len(ex_path)-1)]
                    if ex_path[:-1] == p_path:
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None
        """
        if (request is not None and
                request.headers.get('Authorization') is not None):
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
