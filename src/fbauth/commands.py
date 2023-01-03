# -*- coding: utf-8 -*-
"""
    Custom - Command-Line-Group
"""
from types import SimpleNamespace

import click
import fastberry as fb

# Type(s) Tools
# from . import forms, manager, types
from . import types
from .security import Password

# from fastberry.handlers.cmd.action import introspection_info


def shell_print(text: str, color: str = None, bold: bool = False):
    """(CLI) Print"""
    click.echo(click.style(text, fg=color, bold=bold))


def get_ops():
    """Get GraphQL Operations"""

    # GraphQL (Schema)
    app = fb.App()
    schema = app.graphql.schema()
    introspection_query = """
    query {
        query: __schema {
            ops: queryType {
                names: fields {
                    name
                }
            }
        }
        mutation: __schema {
            ops: mutationType {
                names: fields {
                    name
                }
            }
        }
    }
    """
    result = schema.execute_sync(introspection_query)
    graphql_query = [x["name"] for x in result.data["query"]["ops"]["names"]]
    graphql_mutation = [x["name"] for x in result.data["mutation"]["ops"]["names"]]

    return SimpleNamespace(
        query=graphql_query,
        mutation=graphql_mutation,
        all=[*graphql_query, *graphql_mutation],
    )


def get_perms(perms):
    """Get GraphQL Operations"""
    role_perms = []

    # GraphQL (Operations)
    if perms:
        graphql = get_ops()
        for item in perms.split(","):
            operation = item.strip()
            if operation in graphql.all:
                role_perms.append(operation)

    return role_perms or None


# Init Group
@fb.cli
def cli():
    """Click (CLI) Group"""


# Create <Commands> here.
@cli.command()
@click.option(
    "-u",
    "--username",
    help="Account's Username.",
    type=str,
    default=None,
    required=True,
)
@click.option(
    "-p",
    "--password",
    help="Account's Password.",
    type=str,
    default=None,
    required=True,
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
)
@click.option(
    "-e", "--email", help="Account's Email.", type=str, default=None, required=True
)
@click.option(
    "-s",
    "--super",
    is_flag=True,
    show_default=True,
    default=False,
    help="Create a Super User Account.",
)
@fb.coro
async def create_user(username, password, email, super):
    """Create an Account"""
    # Example:
    # create-user --super -u admin -p secret -e admin@example.com

    # Account Dict
    account = {}
    account["username"] = username
    account["password"] = Password.hash(password)
    account["email"] = email

    # Create Account
    schema = types.User(**account).__dict__
    for field in ["_id", "id", "is_authenticated", "is_anonymous", "role"]:
        del schema[field]

    # Is Super-User?
    if super:
        schema["is_super_user"] = True

    # Database Hit
    database = await types.User.objects.create(schema)
    if not database.error:
        user = database.data
        shell_print("\nSuccessfully Created Account:", bold=True)
        shell_print(f"* {user.username}", color="bright_green", bold=True)
    else:
        shell_print("\nDatabase Error:", bold=True)
        shell_print(f"* {database.error_message}", color="bright_red", bold=True)
