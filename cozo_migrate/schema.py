#!/usr/bin/env python3

from pycozo.client import Client

from .utils.fn import doesnt_throw

check_schema_query = """
?[id] := *migrations_manager { id }
:limit 1
"""

create_schema_query = """
:create migrations_manager {
    migrated_at: Validity default [floor(now()), true] =>
    id: String?,
    previous_id: String?,
    created_at: Float?,
}"""


@doesnt_throw
def schema_exists(client: Client) -> bool:
    # Ensure the migrate schema exists
    client.run(check_schema_query)
    return True


def create_schema(client: Client) -> None:
    client.run(create_schema_query)
