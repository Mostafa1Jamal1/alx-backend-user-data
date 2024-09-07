#!/usr/bin/env python3
"""BasicAuth module
"""

from .auth import Auth


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
