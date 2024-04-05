#!/usr/bin/env python3

from typing import Optional

import pandas as pd
from pycozo.client import Client

from .schema import MANAGER_TABLE_NAME
from .types import Migration

get_first_query = f"""
?[
    migrated_at,
    id,
    previous_id,
    created_at,
] := *{MANAGER_TABLE_NAME} {{
        migrated_at_ms: validity,
        id,
        created_at,
        previous_id,
    }},
    migrated_at = to_int(validity) / 1000,
    previous_id = null
"""

get_latest_query = f"""
?[
    migrated_at,
    id,
    previous_id,
    created_at,
] := *{MANAGER_TABLE_NAME} {{
        migrated_at_ms: validity,
        id,
        created_at,
        previous_id,
        @ "NOW"
    }}, migrated_at = to_int(validity) / 1000
"""

get_history_query = f"""
?[
    migrated_at,
    id,
    previous_id,
    created_at,
] := *{MANAGER_TABLE_NAME} {{
        migrated_at_ms: validity,
        id,
        created_at,
        previous_id,
    }}, migrated_at = to_int(validity) / 1000

:sort migrated_at
"""

get_migration_path_query = f"""
edges[
    previous_id,
    id,
] := *{MANAGER_TABLE_NAME} {{
        id,
        previous_id,
    }}

starting[id] <- [[null]]
latest[id] := *{MANAGER_TABLE_NAME} {{ id @ "NOW" }}

?[start, goal, path] <~ ShortestPathBFS(
    edges[from, to],
    starting[start_idx],
    latest[goal_idx],
)
"""


def get_history(client: Client) -> pd.DataFrame:
    results = client.run(get_history_query)
    return results


def get_migration_path(client: Client) -> list[str]:
    results = client.run(get_migration_path_query)
    assert len(results) <= 1, "More than one path returned"

    if len(results) == 0:
        return []

    path = results["path"][0]
    return path


def get_latest_migration(client: Client) -> Optional[Migration]:
    migration = Migration.get_first(client.run(get_latest_query))
    return migration


def get_first_migration(client: Client) -> Optional[Migration]:
    migration = Migration.get_first(client.run(get_first_query))
    return migration


def get_current_schema(client: Client) -> pd.DataFrame:
    all_relations = client.run("::relations")
    normal_relations = all_relations[all_relations["access_level"] != "index"][
        ["name", "description"]
    ]

    relation_wise_columns = {
        relation: client.run(f"::columns {relation}").drop("index", axis=1)
        for relation in normal_relations["name"]
        if relation != MANAGER_TABLE_NAME
    }

    return relation_wise_columns
