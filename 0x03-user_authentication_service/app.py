#!/usr/bin/env python3
"""basic Flask app.
"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
