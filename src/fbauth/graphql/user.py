# -*- coding: utf-8 -*-
"""
    API - GraphQL
"""

# Fastberry
import fastberry as fb

# Type(s) Tools
from .. import forms, manager, security, types


# Create your API (GraphQL) here.
@fb.gql
class User:
    """User GraphQL"""

    class Meta:
        """Meta-Data"""

        app = False
        model = "User"

    class Query:
        """Query"""

        '''
        async def search(
            username: str | None = None,
            email: str | None = None,
            role: fb.ID | None = None,
            is_disabled: bool | None = None,
            is_staff: bool | None = None,
            is_super_user: bool | None = None,
            is_authenticated: bool | None = None,
            is_anonymous: bool | None = None,
        ) -> fb.edges(types.User):
            """(Search-Account) Read the Docs"""
            print(username)
            print(email)
            print(role)
            print(is_disabled)
            print(is_staff)
            print(is_super_user)
            print(is_authenticated)
            print(is_anonymous)
            table = types.User.objects
            query = table.where("username", "contains", "jane")
            query |= table.where("username", "contains", "john")
            print(query)
            results = await table.find(query, page=1, limit=100, sort_by="-id")
            print(results)
            return fb.page(edges=[], length=0, pages=0)
        '''

        async def detail(id: fb.ID) -> fb.query(types.User):
            """Get Account by ID"""
            user_db = await types.User.objects.detail(id)
            user = user_db.__dict__
            role = await types.Role.objects.get_by(id=user["role_id"])
            del user["role_id"]
            user["role"] = types.Role(**role.__dict__)
            user["password"] = None
            if user_db.id:
                return types.User(
                    **user,
                    is_authenticated=False,
                    is_anonymous=False,
                )
            return False

        async def me(info) -> fb.query(types.User):
            """Get Current Account (Me)"""
            user = info.context.get("user")
            # Get Anonymous Token
            anonymous_token = info.context["request"].cookies.get("Anonymous")
            # Inject Anonymous Token
            if not anonymous_token and user.is_anonymous:
                info.context["response"].set_cookie(
                    key="Anonymous", value=user.id, httponly=True, secure=True
                )
            if user.is_anonymous:
                info.context["response"].delete_cookie(key="Authorization")
            if not user.is_anonymous:
                info.context["response"].delete_cookie(key="Anonymous")
            return user

    class Mutation:
        """Mutation"""

        async def create(form: forms.CreateUser) -> fb.mutation(types.User):
            """Create an Account"""
            return await manager.User.create(form.input)

        async def login(
            info,
            username: str | None = None,
            email: str | None = None,
            password: str = None,
        ) -> fb.mutation(types.AccessToken):
            """Authenticate Credentials"""
            account = await manager.User.authenticate(
                username=username, email=email, password=password
            )
            # Error
            if not account.is_valid:
                return account.error
            # Success
            info.context["response"].set_cookie(
                key="Authorization",
                value=account.token.token,
                httponly=True,
                secure=True,
            )
            return account.token

        async def update(
            info, form: forms.UpdateUser
        ) -> fb.mutation(types.User) | None:
            """Update Current Account (Me)
            - Any field left as blank ex: `email: null` **will not be updated**.
            - Only fields with an actual value other than `null` will be processed.
            """
            user = info.context.get("user")
            if not user.is_anonymous:
                return await manager.User.update(
                    user.id,
                    form.input,
                )
            return fb.errors(
                messages=[fb.error(text="user is not authorized", type="unauthorized")]
            )

        async def disable(info, state: bool) -> bool:
            """**Disable/Enable** Current Account (Me)
            Returns:
                - `True` if it was **updated**.
                - `False` if there was an **error**.
            """
            user = info.context.get("user")
            return await manager.User.disable(user.id, state)

        async def refresh_token(
            info, token: str | None = None
        ) -> fb.query(types.AccessToken):
            """Refresh Credentials Token"""
            if not token:
                request = info.context.get("request")
                token = request.headers.get("authorization", "").replace("Bearer ", "")
            if token:
                new_token = security.AccessToken.refresh(token)
                if new_token:
                    # Success
                    info.context["response"].set_cookie(
                        key="Authorization",
                        value=new_token,
                        httponly=True,
                        secure=True,
                    )
                    return types.AccessToken(token=new_token)
            return None
