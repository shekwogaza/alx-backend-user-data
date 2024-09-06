#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class to manage API basic authentication."""

    def extract_base64_authorization_header(self,
                                            authorization_header:
                                                str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header
            from the request.

        Returns:
            str: The Base64 part of the header or None if conditions
            are not met.
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
                                     user_email: str, user_pwd:
                                         str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The User instance if credentials are valid, or
            None otherwise.
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

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for the current request by
        performing Basic authentication.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The User instance if authentication
            succeeds, or None otherwise.
        """
        if request is None:
            return None

        # Retrieve the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract the Base64-encoded part from the Authorization header
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None

        # Decode the Base64 string
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_auth_header is None:
            return None

        # Extract user credentials (email and password) from the decoded string
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the User object based on the credentials
        return self.user_object_from_credentials(user_email, user_pwd)
