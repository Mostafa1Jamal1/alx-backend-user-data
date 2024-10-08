#!/usr/bin/env python3
"""SessionAuth module
"""

from .auth import Auth
from uuid import uuid4
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id
        """
        if user_id is not None and type(user_id) == str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        """
        if session_id is not None and type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a User instance based on a cookie value
        """
        cooky = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cooky)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """deletes the user session / logout
        """
        if request is not None:
            session_id = self.session_cookie(request)
            if (session_id is not None and
                    self.user_id_for_session_id(session_id) is not None):
                self.user_id_by_session_id.pop(session_id)
                return True
        return False
