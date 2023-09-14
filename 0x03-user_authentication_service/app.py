#!/usr/bin/env python3
""" set up a basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth
from typing import TypeVar


app = Flask(__name__)
AUTH = Auth()
T = TypeVar('T')


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ GET / welcome message
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")