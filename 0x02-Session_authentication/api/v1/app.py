#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
env_auth = getenv("AUTH_TYPE")

if env_auth == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif env_auth == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif env_auth == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def filter_request():
    """Filters request"""

    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/',
            '/api/v1/auth_session/login/']

    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        return None
        abort(401)
    if auth is None or not auth.require_auth(request.path, paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    elif auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
