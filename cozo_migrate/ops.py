#!/usr/bin/env python3

import time
from typing import Optional

from pycozo.client import Client
from rich.progress import track

from .types import MigrationModule
from .utils.console import fail, info, warn
from .utils.fn import paired


def add_migration(
    client: Client, id: Optional[str], previous_id: Optional[str], created_at: float
) -> None:
    """Add a migration to the migrations_manager table."""

    client.insert(
        "migrations_manager",
        {
            "created_at": created_at,
            "previous_id": previous_id,
            "id": id,
        },
    )

    time.sleep(0.1)


def apply(
    client: Client,
    migration1: MigrationModule,
    migration2: MigrationModule,
    down: bool = False,
    verbose: bool = False,
) -> None:
    # Up: migration1 -> migration2 (run migration2.up)
    # Down: migration1 -> migration2 (run migration1.down)
    op = migration1.down if down else migration2.up

    op_name = (
        f"{migration1.MIGRATION_ID}::down" if down else f"{migration2.MIGRATION_ID}::up"
    )

    previous_id = migration1.MIGRATION_ID
    id = migration2.MIGRATION_ID
    created_at = migration2.CREATED_AT
    assert id or previous_id, "Can't migrate from None to None"

    verbose and info(f"Running `{op_name}`...")
    op(client)

    add_migration(
        client,
        created_at=created_at,
        id=id,
        previous_id=previous_id,
    )


def apply_migrations(
    client: Client,
    migrations: list[MigrationModule],
    down: bool = False,
    _rolling_back: bool = False,
    verbose: bool = False,
) -> bool:
    currently_applied = []
    need_to_roll_back = False
    migration_error = None

    for from_, to in track(paired(migrations), description="Migrating"):
        try:
            apply(client, from_, to, down=down, verbose=verbose)
            currently_applied.append(from_)
        except Exception as e:
            if _rolling_back:
                # We're already rolling back, so we can't roll back again
                # Just fail
                fail(f"Rollback failed: {e}")

            migration_error = e
            need_to_roll_back = True
            break

    if need_to_roll_back:
        migration_error and warn(f"Error: {migration_error}")

        # Roll back the migrations that were applied
        # in reverse order
        warn("Migration failed. Reverting...")

        apply_migrations(
            client,
            currently_applied[::-1],
            down=(not down),
            _rolling_back=True,
            verbose=verbose,
        )

        return False

    return True
