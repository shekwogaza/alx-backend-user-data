#!/usr/bin/env python3
"""E2E integration tests for user authentication system"""
from requests import get, put, post, delete

BASE_URL = "http://0.0.0.0:5000"

def register_user(email: str, password: str) -> None:
    """Test user registration"""
    r = post(f"{BASE_URL}/users", data={'email': email, "password": password})
    assert r.json() == {"email": email, "message": "user created"}
    assert r.status_code == 200

    r = post(f"{BASE_URL}/users", data={'email': email, "password": password})
    assert r.json() == {"message": "email already registered"}
    assert r.status_code == 400

def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect password"""
    r = post(f"{BASE_URL}/sessions", data={'email': email, "password": password})
    assert r.status_code == 401
    assert r.cookies.get("session_id") is None

def log_in(email: str, password: str) -> str:
    """Test successful login and return session_id"""
    r = post(f"{BASE_URL}/sessions", data={'email': email, "password": password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    session_id = r.cookies.get("session_id")
    assert session_id is not None
    return session_id

def profile_unlogged() -> None:
    """Test profile access for logged out user"""
    r = get(f"{BASE_URL}/profile")
    assert r.status_code == 403

def profile_logged(session_id: str) -> None:
    """Test profile access for logged in user"""
    r = get(f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL}

def log_out(session_id: str) -> None:
    """Test logout"""
    r = delete(f"{BASE_URL}/sessions", cookies={"session_id": session_id},
               allow_redirects=True)
    assert r.status_code == 200
    assert len(r.history) == 1
    assert r.history[0].status_code == 302
    assert r.json() == {"message": "Bienvenue"}

def reset_password_token(email: str) -> str:
    """Test password reset token generation"""
    r = post(f"{BASE_URL}/reset_password", data={"email": email})
    assert r.status_code == 200
    reset_token = r.json().get("reset_token")
    assert isinstance(reset_token, str)
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test password update"""
    data = {"email": email, "new_password": new_password, "reset_token": reset_token}
    r = put(f"{BASE_URL}/reset_password", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
