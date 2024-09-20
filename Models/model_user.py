from datetime import datetime, timedelta, timezone
import os
from typing import List

from dotenv import load_dotenv
import jwt
from jwt.exceptions import ExpiredSignatureError
from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM', "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))


class User(Base):
    """Users who will use the app """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), nullable=False)

    role: Mapped["Group"] = relationship(back_populates="users")

    customers: Mapped[List["Customer"]] = relationship(
        back_populates="sales_representative")
    events: Mapped[List["Event"]] = relationship(back_populates="support")

    def set_password(self, password):
        """encrypt the password given to it

        Keyword arguments:
        password -- a password to encrypt
        """
        ph = PasswordHasher()
        self.password = ph.hash(password)

    def check_password(self, password):
        """verify if the password given is the same that the one in DB

        Keyword arguments:
        password -- a password to check
        return -- true/false response
        """

        ph = PasswordHasher()
        return ph.verify(self.password, password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        """Create a token with the data given and give it a expire date

        Keyword arguments:
        data -- the data to put in the token
        expire_delta -- the duration of the token if given
        Return: the encoded token
        """

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta

        else:
            expire = datetime.now(timezone.utc)
            expire += timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str):
        """will get data from the token given

        Keyword arguments:
        token -- a token previously encoded
        Return: return the decoded data if token still valid, an error if not
        """

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload

        except ExpiredSignatureError:
            return "expired"

        except jwt.PyJWTError:
            return None
