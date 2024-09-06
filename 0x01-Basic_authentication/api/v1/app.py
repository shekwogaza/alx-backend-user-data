#!/usr/bin/env python3
"""Route module for the API

This module sets up a Flask application with CORS support and defines
error handlers for 404, 401, and 403 errors. It also registers the app_views
blueprint and starts the Flask development server if run as the main script.

The module adheres to the following standards:
- Interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- Uses pycodestyle style (version 2.5)
- All functions and the module itself are documented
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error):
    """
    Not found handler

    This function handles 404 Not Found errors and returns a JSON response.

    Args:
        error: The 404 error object.

    Returns:
        tuple: A tuple containing a JSON response and the HTTP status code 404.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error):
    """
    Handle 401 Unauthorized errors

    This function handles 401 Unauthorized errors and returns a JSON response.

    Args:
        error: The 401 error object.

    Returns:
        tuple: A tuple containing a JSON response and the HTTP status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error):
    """
    Handle 403 Forbidden errors

    This function handles 403 Forbidden errors and returns a JSON response.

    Args:
        error: The 403 error object.

    Returns:
        tuple: A tuple containing a JSON response and the HTTP status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
