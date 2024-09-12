#!/usr/bin/env python3
"""auth module
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """salted hash of the input password, hashed with bcrypt.hashpw.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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
