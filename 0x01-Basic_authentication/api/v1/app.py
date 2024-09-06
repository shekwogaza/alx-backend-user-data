#!/usr/bin/env python3
"""Route module for the API

This module sets up a Flask application with CORS support and defines
error handlers for 404 and 401 errors. It also registers the app_views
blueprint and starts the Flask development server if run as the main script.

Returns:
    Flask: The configured Flask application instance.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from typing import Literal
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler

    This function handles 404 Not Found errors and returns a JSON response.

    Args:
        error (werkzeug.exceptions.NotFound): The 404 error object.

    Returns:
        tuple: A tuple containing a JSON response and the HTTP status code 404.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """Handle 401 Unauthorized errors

    This function handles 401 Unauthorized errors and returns a JSON response.

    Args:
        error (werkzeug.exceptions.Unauthorized): The 401 error object.

    Returns:
        tuple: A tuple containing a JSON response and the HTTP status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    # Run the Flask development server
    app.run(host=host, port=port)
