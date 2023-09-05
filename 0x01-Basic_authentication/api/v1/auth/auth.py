#!/usr/bin/env python3
""" Module of Index views
"""
from typing import List, TypeVar
from flask import jsonify, abort, request
from api.v1.views import app_views


class Auth:
    """Auth class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False - path and excluded_paths will not be used.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None - request will not be used.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None - request will not be used.
        """
        return None
