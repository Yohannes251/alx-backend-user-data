#!/usr/bin/env python3
"""
    This module is a basic flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index():
    """Index page get route"""

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Handles post request for users endpoint"""
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """Handles post request on sessions endpoint"""

    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """Handles DELETE request for /sessions endpoint"""

    session_id = session.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
