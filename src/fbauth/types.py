# -*- coding: utf-8 -*-
"""
    { Types } for GraphQL
"""

from typing import Optional

import fastberry as fb


# Create your <types> here.
@fb.sql.model(
    required=["name"],
    unique=["name"],
)
class Role:
    """User's Account Role"""

    name: str
    perms: fb.json


@fb.sql.model(
    required=["username", "email"],
    index=["username"],
    unique=["username", "email"],
    ignore=["is_authenticated", "is_anonymous"],
)
class User:
    """User's Account"""

    username: str
    password: str
    email: str
    role: Optional["Role"] = None
    is_disabled: bool = False
    is_staff: bool = False
    is_super_user: bool = False
    created_on: fb.datetime = fb.field(fb.Date.datetime)
    is_authenticated: bool = False
    is_anonymous: bool = True


@fb.type
class AccessToken:
    """Account Acces Token"""

    token: str
    token_type: str = "bearer"
