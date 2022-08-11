# -*- coding: utf-8 -*-
"""
    API - CRUD
"""

# Fastberry
from fastberry import GQL, Fastberry, to_camel_case

SETTINGS = Fastberry()

""" All-Operations
query operations {
  query: operationQuery
  mutation: operationMutation
}
"""

# Create your API (GraphQL) here.
class Operations(GQL):
    """Operations Api"""

    class Query:
        """Query"""

        async def queries(info) -> list[str]:
            """## List of All GraphQL Queries"""
            # print(info)
            ops = SETTINGS.apps.operations.query
            query_names = [to_camel_case(x) for x in ops]
            return query_names

        async def mutations(info) -> list[str]:
            """## List of All GraphQL Mutations"""
            ops = SETTINGS.apps.operations.mutation
            mutation_names = [to_camel_case(x) for x in ops]
            return mutation_names
