# -*- coding: utf-8 -*-
"""
    { Controller } for the Database(s)
"""

import fastberry as fb

from .. import types


# Create your <managers> here.
@fb.manager
class Role:
    """Product Manager"""

    model = types.Role

    @classmethod
    async def create(cls, form):
        """Create Role"""
        # Errors
        errors_messages = []

        # Good Input
        if form.is_valid:
            results = await cls.objects.create(form.data.__dict__)
            if not results.error:
                item = results.data.__dict__
                return cls.model(**item)
            if "UNIQUE" in results.error_message:
                if "name" in results.error_message:
                    errors_messages.append(
                        fb.error(
                            field="name",
                            type="unique",
                            text="name already exists!",
                        )
                    )
        # Bad Input
        if len(errors_messages) < 1:
            errors_messages.append(fb.error(type="input", text="Something Went Wrong!"))
        return fb.errors(messages=errors_messages)

    @classmethod
    async def update(cls, form):
        """Update Role"""
        # Errors
        errors_messages = []

        # Good Input
        if form.is_valid:
            data = {}
            if form.data.name:
                data["name"] = form.data.name
            if form.data.perms:
                data["perms"] = form.data.perms
            results = await cls.objects.update(form.data.id, data)
            if not results.error:
                item = results.data.__dict__
                return cls.model(**item)
        # Bad Input
        if len(errors_messages) < 1:
            errors_messages.append(fb.error(type="input", text="Something Went Wrong!"))
        return fb.errors(messages=errors_messages)

    @classmethod
    async def delete(cls, unique_id):
        """Delete Role"""
        # Good Input
        results = await cls.objects.delete(unique_id)
        if not results.error:
            return True
        # Bad Input
        return False

    @classmethod
    async def all(cls):
        """All Roles"""
        results = await cls.objects.all()
        items = [
            cls.model(id=item.id, name=item.name, perms=item.perms)
            for item in results.data
        ]
        return items
