#!/usr/bin/env python3
"""basic Flask app.
"""

from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect,
    url_for
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['Get'])
def hello():
    """home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """the end-point to register a user
    """
    try:
        AUTH.register_user(
            email=request.form['email'],
            password=request.form['password'])
        return jsonify(
            {"email": request.form['email'], "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """create a new session for the user,
    store it the session ID as a cookie with key "session_id" on the response
    """
    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email=email, password=password):
        new_id = AUTH.create_session(email=email)
        respond = jsonify({"email": email, "message": "logged in"})
        respond.set_cookie('session_id', new_id)
        return respond
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """If the user exists destroy the session and redirect the user to GET /
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
