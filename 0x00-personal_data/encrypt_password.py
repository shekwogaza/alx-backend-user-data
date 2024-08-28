#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""


import bcrypt


def hash_password(password: str) -> bytes:
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
