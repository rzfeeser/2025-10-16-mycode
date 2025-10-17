#!/usr/bin/env python3
"""
app.py - basic Flask application with comments

Usage:
    pip install flask
    python app.py
This app is container-friendly (binds to 0.0.0.0) and is suitable for quick local testing.
"""

# Import Flask pieces: Flask to create the app, request to read input, jsonify to return JSON.
from flask import Flask, request, jsonify

# Create the Flask application instance
app = Flask(__name__)

# Root route: returns a plain text greeting
@app.route("/")
def index():
    """index function"""
    # Returning a simple string results in a text/html response by default
    return "Hello, World!"


# JSON example route: returns a JSON object with a message
@app.route("/json")
def hello_json():
    """returns string in json format - rzfeeser"""
    # jsonify serializes the given kwargs into a JSON response with appropriate headers
    return jsonify(message="Hello, JSON!")


# Echo endpoint: supports GET (query params) and POST (JSON body)
@app.route("/echo", methods=["GET", "POST"])
def echo():
    """
    Echoes back input from the client:
    - If a JSON body is provided (e.g., Content-Type: application/json), that JSON is echoed.
    - Otherwise, query parameters from the URL are echoed as a dict.
    """
    # get_json(silent=True) tries to parse JSON and returns None instead of raising if parsing fails
    data = request.get_json(silent=True)

    if data:
        # Return the parsed JSON under the "echo" key
        return jsonify(echo=data)

    # If no JSON was provided, echo query parameters (request.args is an ImmutableMultiDict)
    return jsonify(echo=request.args.to_dict())


# Health check route: useful for container orchestration/readiness probes
@app.route("/health")
def health():
    """returns json OK"""
    # Return a minimal JSON health status
    return jsonify(status="ok")


# When executed directly, run the development server.
# For production, use a WSGI server (gunicorn, uWSGI, etc.).
if __name__ == "__main__":
    # Bind to all interfaces (0.0.0.0) so the app is reachable from other containers/hosts.
    # debug=True enables the debugger and auto-reload; disable in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
