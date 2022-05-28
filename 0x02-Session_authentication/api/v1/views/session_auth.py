#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ GET /api/v1/auth_session/login
    Return:
      - the status of the API
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user_list = User.search({"email": email})
    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_list[0]
    if user.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response
