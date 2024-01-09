#!/usr/bin/env python3

from typing import Optional

import pandas as pd
from pycozo.client import Client

from .types import Migration

get_first_query = """
?[
    migrated_at,
    id,
    previous_id,
    created_at,
] := *migrations_manager {
        migrated_at_ms: validity,
        id,
        created_at,
        previous_id,
    },
    migrated_at = to_int(validity) / 1000,
    previous_id = null
"""

get_latest_query = """
?[
    migrated_at,
    id,
    previous_id,
    created_at,
] := *migrations_manager {
        migrated_at_ms: validity,
        id,
        created_at,
        previous_id,
        @ "NOW"
    }, migrated_at = to_int(validity) / 1000
"""

get_history_query = """
?[
    migrated_at,
    id,
    previous_id,
    created_at,
] := *migrations_manager {
        migrated_at_ms: validity,
        id,
        created_at,
        previous_id,
    }, migrated_at = to_int(validity) / 1000

:sort migrated_at
"""

get_migration_path_query = """
edges[
    previous_id,
    id,
] := *migrations_manager {
        id,
        previous_id,
    }

starting[id] <- [[null]]
latest[id] := *migrations_manager { id @ "NOW" }

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
