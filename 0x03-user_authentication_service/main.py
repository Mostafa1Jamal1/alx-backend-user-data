#!/usr/bin/env python3
"""
Main file
End-to-end integration test
"""
import requests
# test for local app: http://0.0.0.0:5000/


def register_user(email: str, password: str) -> None:
    """To test register_user
    """
    r = requests.post('http://0.0.0.0:5000/users',
                      data={'email': email, 'password': password})
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """To test login with wrong password
    """
    r = requests.post('http://0.0.0.0:5000/sessions',
                      data={'email': email, 'password': password})
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """To test login
    """
    r = requests.post('http://0.0.0.0:5000/sessions',
                      data={'email': email, 'password': password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """To test profile with unlogged user
    """
    r = requests.get('http://0.0.0.0:5000/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """To test profile with logged user
    """
    r = requests.get('http://0.0.0.0:5000/profile',
                     cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.json().get('email') is not None


def log_out(session_id: str) -> None:
    """To test logout
    """
    r = requests.delete('http://0.0.0.0:5000/sessions',
                        cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.url == 'http://0.0.0.0:5000/'
    assert r.history[0].status_code == 302


def reset_password_token(email: str) -> str:
    """To test reset password token
    """
    r = requests.post('http://0.0.0.0:5000/reset_password',
                      data={'email': email})
    assert r.status_code == 200
    r_json = r.json()
    assert r_json.get('email') == email
    assert r_json.get('reset_token') is not None
    return r_json.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """To test update password
    """
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put('http://0.0.0.0:5000/reset_password', data=data)
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
