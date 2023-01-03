# -*- coding: utf-8 -*-
"""
    [Security]
"""

from datetime import datetime, timedelta

import fastberry as fb
from jose import JWTError, jwt

from . import config

# Config
SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

SECRET_KEY_ERROR = f"""
----------------------------------------------------
The Environment: "config/.env/{fb.mode}.toml"
----------------------------------------------------

Requires a "SECRET_KEY" value.

----------------------------------------------------
For example:
----------------------------------------------------
[env]
SECRET_KEY = "fastapi-insecure-09d25e094faa6ca2556c"
"""

if not SECRET_KEY:
    raise Exception(SECRET_KEY_ERROR)


class AccessToken:
    """User Access Tokens"""

    @staticmethod
    def encode(data: dict, expires_delta: timedelta | None = None):
        """Create Access Token

        Args:
            data (dict): User's Information.
            expires_delta (timedelta | None, optional) <Defaults to None>: Time for the expiration.

        Returns:
            str: JSON Web Token
        """

        to_encode = data.copy()

        # Expiration
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES,
                hours=config.ACCESS_TOKEN_EXPIRE_HOURS,
                weeks=config.ACCESS_TOKEN_EXPIRE_WEEKS,
            )

        # Encoding
        to_encode.update({"exp": expire})

        # Token
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode(token: str):
        """Decode Access Token

        Args:
            token (str): JSON Web Token

        Returns:
            dict: User's Information.
        """
        if token:
            try:
                return_value = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            except JWTError:
                return_value = {}
        else:
            return_value = {}
        return return_value

    @classmethod
    def refresh(cls, token: str):
        """Refresh Access Token

        Args:
            token (str): JSON Web Token

        Returns:
            token (str): JSON Web Token
        """

        return cls.encode(cls.decode(token))
