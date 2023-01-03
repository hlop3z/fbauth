# -*- coding: utf-8 -*-
"""
    { Forms } for GraphQL
"""
import fastberry as fb

# Create Group "Form"
form = fb.input("form")

# Create your <forms> here.
@form
class CreateUser:
    """Form for Creating an Account"""

    username = fb.value(
        str,
        default=None,
        required=True,
        regex={
            r"^[a-zA-Z0-9-_]+$": "username must contain only: letters, numbers, dashes(-) and underscores(_)"
        },
        rules=[],
        filters=fb.filters(
            rules=[(lambda v: v.lower())],
            regex=[],
        ),
    )
    password = fb.value(
        str,
        default=None,
        required=True,
        rules=[
            (lambda v: len(v) >= 8 or "password must be at least 8 characters long")
        ],
    )
    email = fb.value(
        str,
        default=None,
        required=True,
        regex={r"[\w\.-]+@[\w\.-]+": "invalid email address"},
        rules=[],
        filters=fb.filters(
            regex=[],
            rules=[(lambda v: v.lower())],
        ),
    )


@form
class UpdateUser:
    """Form for Creating an Account"""

    username = fb.value(
        str,
        default=None,
        required=False,
        regex={
            r"^[a-zA-Z0-9-_]+$": "username must contain only: letters, numbers, dashes(-) and underscores(_)"
        },
        rules=[],
        filters=fb.filters(
            rules=[(lambda v: v.lower())],
            regex=[],
        ),
    )
    password = fb.value(
        str,
        default=None,
        required=False,
        rules=[
            (lambda v: len(v) >= 8 or "password must be at least 8 characters long")
        ],
    )
    email = fb.value(
        str,
        default=None,
        required=False,
        regex={r"[\w\.-]+@[\w\.-]+": "invalid email address"},
        rules=[],
        filters=fb.filters(
            regex=[],
            rules=[(lambda v: v.lower())],
        ),
    )


@form
class CreateRole:
    """Form for Creating an Role"""

    name = fb.value(
        str,
        default=None,
        required=True,
        regex={
            r"^[a-zA-Z0-9_]+$": "name must contain only: letters, numbers and underscores(_)"
        },
        filters=fb.filters(
            rules=[(lambda v: v.lower())],
            regex=[],
        ),
    )
    perms = fb.value(
        list[str],
        default=None,
        required=False,
        rules=[],
    )


@form
class UpdateRole:
    """Form for Creating an Role"""

    id = fb.value(fb.ID, required=True)

    name = fb.value(
        str,
        default=None,
        required=False,
        regex={
            r"^[a-zA-Z0-9_]+$": "name must contain only: letters, numbers and underscores(_)"
        },
        filters=fb.filters(
            rules=[(lambda v: v.lower())],
            regex=[],
        ),
    )
    perms = fb.value(
        list[str],
        default=None,
        required=False,
        rules=[],
    )
