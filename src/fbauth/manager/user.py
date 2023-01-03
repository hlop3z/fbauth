# -*- coding: utf-8 -*-
"""
    { User } Database
"""
import uuid
from types import SimpleNamespace

import fastberry as fb

from .. import types
from ..security import AccessToken, Password

DEFAULT_ROLE_ID = 1


def unique_constraint(results):
    """User's Unique Constraints Validator"""

    errors_messages = []

    # Bad Input
    if "UNIQUE" in results.error_message:
        if "username" in results.error_message:
            errors_messages.append(
                fb.error(
                    field="username",
                    type="unique",
                    text="username already exists!",
                )
            )
        if "email" in results.error_message:
            errors_messages.append(
                fb.error(
                    field="email",
                    type="unique",
                    text="email already exists!",
                )
            )

    return errors_messages


def user_object(current):
    """Transform: Database ORM to User Object"""

    return types.User(
        _id=current._id,
        id=current.id,
        role=current.role_id,
        username=current.username,
        email=current.email,
        password=None,
        is_disabled=current.is_disabled,
        is_staff=current.is_staff,
        is_super_user=current.is_super_user,
        is_authenticated=True,
        is_anonymous=False,
        created_on=current.created_on,
    )


# Create your <managers> here.
@fb.manager
class User:
    """User Manager"""

    model = types.User

    @classmethod
    async def create(cls, form):
        """Create Account"""

        # Errors
        errors_messages = []

        # Good Input
        if form.is_valid:
            the_input = cls.form(form)

            # Clean Dict
            the_input["password"] = Password.hash(the_input["password"])
            del the_input["role"]
            del the_input["is_authenticated"]
            del the_input["is_anonymous"]
            the_input["role_id"] = DEFAULT_ROLE_ID

            # Database Hit
            results = await cls.objects.create(the_input)

            # Success
            if not results.error:
                item = results.data.__dict__
                item["password"] = None
                del item["role_id"]
                return cls.model(**item)

            # Unique Constraint(s)
            errors_messages.extend(unique_constraint(results))

        # Bad Input
        for item in form.errors:
            errors_messages.append(
                fb.error(
                    field=item.get("field"),
                    type=item.get("type"),
                    text=item.get("text"),
                )
            )
        return fb.errors(messages=errors_messages)

    @classmethod
    async def authenticate(cls, **kwargs):
        """Authenticate Account"""

        # Errors
        errors_messages = []

        # Get User
        current = None
        if kwargs.get("email") and not kwargs.get("username"):
            current = await cls.objects.get_by(email=kwargs["email"])
            if not current:
                errors_messages.append(
                    fb.error(
                        field="email",
                        type="not found",
                        text="Email does not exists!",
                    )
                )
        elif kwargs.get("username"):
            current = await cls.objects.get_by(username=kwargs["username"])
            if not current:
                errors_messages.append(
                    fb.error(
                        field="username",
                        type="not found",
                        text="Username does not exists!",
                    )
                )

        # Verify
        response = SimpleNamespace(
            is_valid=False, token=None, user=None, error=fb.errors(messages=[])
        )
        if current:
            is_valid = Password.verify(kwargs.get("password", ""), current.password)
            if is_valid:

                # User Object
                user = user_object(current)
                response.user = user
                response.is_valid = True

                # Access Token
                access_token_data = {"sub": str(user._id)}
                access_token = AccessToken.encode(
                    data=access_token_data,
                    expires_delta=None,
                )
                response.token = types.AccessToken(token=access_token)
                return response
            errors_messages.append(
                fb.error(
                    field="password",
                    type="invalid",
                    text="password does not match!",
                )
            )
        response.error = fb.errors(messages=errors_messages)
        return response

    @classmethod
    async def me(cls, access_token: str):
        """Get Current User"""

        # Token Decoding
        token = AccessToken.decode(access_token)
        user_id = token.get("sub")

        # Authenticate
        if user_id:
            current = await cls.objects.get_by(id=user_id)
            if current:
                role = None
                if current.role_id:
                    db_role = await types.Role.objects.get_by(id=current.role_id)
                    role = types.Role(
                        _id=db_role._id,
                        id=db_role.id,
                        name=db_role.name,
                        perms=db_role.perms,
                    )
                user = user_object(current)
                user.role = role
                return user

        # Anonymous
        random_unique_id = uuid.uuid4()
        return types.User(
            id=str(random_unique_id),
            username=None,
            is_authenticated=False,
            is_anonymous=True,
        )

    @classmethod
    async def update(cls, unique_id, form):
        """Perform Update(s) to the Current User"""

        # Errors
        errors_messages = []
        if form.is_valid:
            data = {}
            if form.data.username:
                data["username"] = form.data.username
            if form.data.email:
                data["email"] = form.data.email
            if form.data.password:
                data["password"] = form.data.password
            if form.data.disabled is not None:
                data["is_disabled"] = form.data.disabled

            # Database Hit
            results = await cls.objects.update(unique_id, data)

            # Success
            if not results.error:
                item = results.data.__dict__
                item["password"] = None
                del item["role_id"]
                return cls.model(**item)

            # Unique Constraint(s)
            errors_messages.extend(unique_constraint(results))

        # Bad Input
        for item in form.errors:
            errors_messages.append(
                fb.error(
                    field=item.get("field"),
                    type=item.get("type"),
                    text=item.get("text"),
                )
            )
        return fb.errors(messages=errors_messages)

    @classmethod
    async def disable(cls, unique_id, state):
        """Disable/Enable Account"""

        data = {"is_disabled": state}

        # Database Hit
        results = await cls.objects.update(unique_id, data)

        # Success
        if not results.error:
            return True
        return False

    '''
    @classmethod
    async def detail(cls, unique_id):
        """Detail"""
        return None

    @classmethod
    async def delete(cls, form):
        """Delete"""
        return None

    @classmethod
    async def search(cls, form):
        """Search"""
        return None
    '''
