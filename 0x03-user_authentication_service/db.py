#!/usr/bin/env python3
""" database module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """

        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add a user instance to the session DB
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user instance in the DB """
        fields, values = [], []
        for k, v in kwargs.items():
            if hasattr(User, k):
                fields.append(getattr(User, k))
                values.append(v)
            else:
                raise InvalidRequestError()
            result = self._session.query(User).filter(tuple(*fields).in_([tuple(v)])).first()
            if result is None:
                raise NoResultFound()
            return result
        
    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update a user instance in the DB
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for k, v in kwargs.items():
            if hasattr(user, k):
                update_source[getattr(User, k)] = v
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(update_source, syncronize_session=False, )
        self._session.commit()
