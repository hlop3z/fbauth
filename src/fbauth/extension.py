# -*- coding: utf-8 -*-
""" [Extension]
    Inject { User } or { Anonymous-User } to GraphQL Context.
"""

from fastberry import BaseExtension

from .manager import User

# from .security import AccessToken


async def get_request_user(request):
    """Get User from Request the Header or Cookie"""
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    user = await User.me(token)
    if user.is_anonymous:
        anonymous_id = request.cookies.get("Anonymous", None)
        if anonymous_id:
            user.id = anonymous_id
    return user


class InjectUser(BaseExtension):
    """Inject User Extension"""

    async def on_executing_start(self):
        """GrapQL Execution"""
        request = self.execution_context.context.get("request")
        user = await get_request_user(request)
        # Set-User (Context)
        self.execution_context.context["user"] = user
