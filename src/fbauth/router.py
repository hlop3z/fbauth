# -*- coding: utf-8 -*-
"""
    [Router]
"""

from typing import Any, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastberry import Router
from fastberry.tools import to_camel_case

# Type(s) Tools
from . import manager, security

ACCESS_TOKEN_URL = security.config.ACCESS_TOKEN_URL

router = Router(tags=["Users"])

ACCESS_OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=ACCESS_TOKEN_URL)


async def get_current_user(
    token: Optional[str] = Depends(ACCESS_OAUTH2_SCHEME),
):
    """FastAPI Dependency -> Get Current-User"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await manager.User.me(token)
    if not user.is_authenticated:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Optional[Any] = Depends(get_current_user),
):
    """FastAPI Dependency -> Check if Current-User is Disabled"""

    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Create <Router> here.
@router.post(f"/{ACCESS_TOKEN_URL}")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    # Login
    """

    access = await manager.User.authenticate(
        username=form_data.username, password=form_data.password
    )

    # Invalid User
    if not access.is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Add Cookie
    access_token = access.token
    response.set_cookie(
        key="Authorization", value=access_token.token, httponly=True, secure=True
    )

    return {"access_token": access_token.token, "token_type": "bearer"}


@router.get("/logout")
async def logout_current_user(
    current_user: Any = Depends(get_current_active_user),
):
    """
    # Logout
    """

    response = JSONResponse({"logout": True})
    response.delete_cookie(key="Authorization")
    return response


@router.get("/user-me")
async def read_user_me(current_user: Any = Depends(get_current_active_user)):
    """
    # Get Current User
    """

    user_me = {to_camel_case(k): v for k, v in current_user.__dict__.items()}

    del user_me["Id"]
    if user_me.get("role", {}):
        user_me["role"] = user_me["role"].__dict__
        if user_me["role"].get("_id"):
            del user_me["role"]["_id"]
        user_me["role"] = {to_camel_case(k): v for k, v in user_me["role"].items()}
    return user_me
