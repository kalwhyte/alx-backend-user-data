#!/usr/bin/env python3
"""Session authentication module.
"""
from api.v1.auth.auth import Auth
from flask import request
from flask_cors import (CORS, cross_origin)
import os


class SessionAuth(Auth):
    """ SessionAuth class to manage API authentication."""
    pass
