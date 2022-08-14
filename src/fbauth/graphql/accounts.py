# -*- coding: utf-8 -*-
"""
    API - CRUD
"""

import functools

# Fastberry
import strawberry
from fastberry import GQL
from fastberry.graphql.inputs import Pagination
from fastberry.graphql.types import (
    Edges,
    Error,
    ErrorMessage,
    Mutation,
    Query,
    Response,
)

from .. import types
from ..actions.users import User
from ..database import SQL

sql_manager = SQL(types.User)


# Create your API (GraphQL) here.
class Accounts(GQL):
    """Demo Api"""

    schema = types.User

    class Query:
        """Query"""

        async def all() -> list[types.User]:
            """## Get All Users"""
            items = await sql_manager.all()
            if items.data:
                return [types.User(**item.__dict__) for item in items.data]
            return []

        async def detail(info, id: str) -> Query(types.User):
            """## Get User by ID"""
            results = await User.users.detail(id)
            if results:
                item = results.__dict__
                item["password"] = None
                return types.User(**item)
            return None

    class Mutation:
        """Mutation"""

        async def create(
            username: str, password: str, email: str
        ) -> Mutation(types.User):
            """## Create Account"""
            message = "Something went wrong!"
            results = await User.create(
                username=username, password=password, email=email, role_id=1
            )
            if not results.error:
                item = results.data.__dict__
                item["password"] = None
                return types.User(**item)
            if (
                "UNIQUE" in results.error_message
                and "username" in results.error_message
            ):
                message = "Username is taken."
            elif "UNIQUE" in results.error_message and "email" in results.error_message:
                message = "Email is already registered."
            return Error([ErrorMessage(type="input", message=message)])
