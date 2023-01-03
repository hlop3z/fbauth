# -*- coding: utf-8 -*-
"""
    API - GraphQL
"""

# Fastberry
import fastberry as fb

# Type(s) Tools
from .. import forms, manager, types


# Create your API (GraphQL) here.
@fb.gql
class Role:
    """Role GraphQL"""

    class Meta:
        """Meta-Data"""

        app = False
        model = "Role"

    class Query:
        """Query"""

        async def all(info) -> list[types.Role | None]:
            """Get ALL Roles"""
            return await manager.Role.all()

    class Mutation:
        """Mutation"""

        # @fb.doc("Create Role for Accounts")
        async def create(form: forms.CreateRole) -> fb.mutation(types.Role):
            """Create Role for Account(s)"""
            return await manager.Role.create(form.input)

        async def update(form: forms.UpdateRole) -> fb.mutation(types.Role):
            """Update Role by ID"""
            return await manager.Role.update(form.input)

        async def delete(id: fb.ID) -> bool:
            """Delete Role by ID"""
            return await manager.Role.delete(id)
