#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""


import bcrypt


def hash_password(password: str) -> bytes:
    """Generate a salt

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password

    Args:
        hashed_password (bytes): _description_
        password (str): _description_

    Returns:
        bool: _description_
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
