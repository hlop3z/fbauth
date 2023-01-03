# -*- coding: utf-8 -*-
""" [Permission]
    Check GraphQL Context for a { User } or { Anonymous-User }.
"""

import json
import typing
from pathlib import Path

import fastberry as fb
from strawberry.types import Info


def write_public_perms(path_to_file: str):
    """Writing to Public-API (JSON)"""
    path = Path(path_to_file)
    if not path.is_file():
        with open(path_to_file, "w", encoding="utf-8") as outfile:
            data = {"perms": []}
            json_object = json.dumps(data, indent=4)
            outfile.write(json_object)


def read_public_perms():
    """Read Public-API (JSON) Permissions"""
    path_to_file = fb.base_dir / "config" / "public-perms.json"
    write_public_perms(path_to_file)
    json_dict = {"perms": []}
    with open(path_to_file, "r", encoding="utf-8") as outfile:
        data = outfile.read()
        perms = None
        if data:
            json_dict = json.loads(data)
            perms = json_dict.get("perms")
        if not isinstance(perms, list):
            json_dict = {"perms": []}
    return json_dict["perms"]


PUBLIC_PERMS = read_public_perms()


class IsAuthorized(fb.BasePermission):
    """Check If User Is Authorized"""

    message = "User is not authorized"  # Unauthorized

    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        """Check GraphQL's Info Context"""

        operation = info.field_name  # info.python_name
        user = info.context.get("user")

        # Disable & Enable User
        if operation == "UserDisable" and user.is_disabled:
            pass
        elif user.is_disabled:
            return False
        if user.is_super_user:
            return True
        if user.role and not user.is_super_user:
            user_perms = user.role.perms or []
            user_perms.extend(PUBLIC_PERMS)
            return operation in user_perms
        return operation in PUBLIC_PERMS
