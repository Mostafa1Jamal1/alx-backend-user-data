#!/usr/bin/env python3
"""SessionExpAuth module
"""

from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    def __init__(self):
        """initialization
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        """
        if (session_id is None or
                session_id not in self.user_id_by_session_id):
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        session_duration = timedelta(seconds=self.session_duration)
        if (created_at is not None and
                created_at + session_duration > datetime.now()):
            return session_dict.get('user_id')
        return None
