#!/usr/bin/env python3

from pycozo.client import Client

from .utils.fn import doesnt_throw

MANAGER_TABLE_NAME: str = "cozo_migrate_manager"

check_schema_query = f"""
?[id] := *{MANAGER_TABLE_NAME} {{ id }}
:limit 1
"""

create_schema_query = f"""
:create {MANAGER_TABLE_NAME} {{
    migrated_at_ms: Validity default [floor(now() * 1000), true] =>
    id: String?,
    previous_id: String?,
    created_at: Float?,
}}"""


@doesnt_throw
def schema_exists(client: Client) -> bool:
    # Ensure the migrate schema exists
    client.run(check_schema_query)
    return True


def create_schema(client: Client) -> None:
    client.run(create_schema_query)
