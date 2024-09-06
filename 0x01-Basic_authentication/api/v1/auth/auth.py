#!/usr/bin/env python3
"""Authentication module for the API.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't
            require authentication.

        Returns:
            bool: False for now.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: None for now.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the request.

        Args:
            request: Flask request object.

        Returns:
            TypeVar('User'): None for now.
        """
        return None
