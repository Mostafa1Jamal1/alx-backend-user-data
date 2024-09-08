#!/usr/bin/env python3
"""all routes for the Session authentication.
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route(
    '/auth_session/login', methods=['Post'], strict_slashes=False)
def login() -> str:
    """Post /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            respond = jsonify(user.to_json())
            respond.set_cookie(getenv('SESSION_NAME'), session_id)
            return respond
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    'auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """DELETE /api/v1/auth_session/logout
    """
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
