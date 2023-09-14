#!/usr/bin/env python3
'''Define a hash_password function'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    '''Hash a password
    '''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''register a user
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError('User {} already exists'.format(email))
    
    def valid_login(self, email: str, password: str) -> bool:
        '''valid login
        '''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
        
    def _generate_uuid(self) -> str:
        '''generate uuid
        '''
        return str(uuid.uuid4())
    
    def create_session(self, email: str) -> str:
        '''create session
        '''
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None