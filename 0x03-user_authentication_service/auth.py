#!/usr/bin/env python3
"""auth module
"""

import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """salted hash of the input password, hashed with bcrypt.hashpw.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user to the database
        if a user already exist with the passed email, raise a ValueError
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(
                email=email, hashed_password=_hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """find the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user’s session_id, then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            user.session_id = uuid
            return uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """returns the corresponding User for session_id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None.
        """
        user = self.get_user_from_session_id(id=user_id)
        user.session_id = None
