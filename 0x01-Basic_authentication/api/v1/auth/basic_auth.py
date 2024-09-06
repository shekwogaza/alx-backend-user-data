#!/usr/bin/env python3
"""Basic authentication module for the API.
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class to manage API basic authentication."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header
            from the request.

        Returns:
            str: The Base64 part of the header or
            None if conditions are not met.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """
        Decodes the Base64 string to its UTF-8 value.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string, or
            None if decoding fails or conditions are not met.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 string.

        Args:
            decoded_base64_authorization_header (str): Decoded Base64
            string in the format "email:password".

        Returns:
            (str, str): Tuple of user email and password, or
            (None, None) if any conditions are not met.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The User instance if credentials are valid,
            or None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        users = User.search({"email": user_email})
        if not users:
            return None

        # Assuming that email is unique and there's only one result
        user = users[0]

        # Verify the password
        if not user.is_valid_password(user_pwd):
            return None

        return user
