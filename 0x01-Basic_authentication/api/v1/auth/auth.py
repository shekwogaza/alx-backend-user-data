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
            excluded_paths (List[str]): List of paths that don't require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Handle wildcard paths
                pattern = excluded_path.rstrip('*')
                if path.startswith(pattern):
                    return False
            elif path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the request.

        Args:
            request: Flask request object.

        Returns:
            TypeVar('User'): None for now.
        """
        return None
