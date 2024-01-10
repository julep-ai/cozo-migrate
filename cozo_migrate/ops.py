#!/usr/bin/env python3

import time
from typing import Optional

from pycozo.client import Client

from .schema import MANAGER_TABLE_NAME
from .types import MigrationModule
from .utils.console import fail, info, warn
from .utils.fn import paired


def add_migration(
    client: Client, id: Optional[str], previous_id: Optional[str], created_at: float
) -> None:
    """Add a migration to the migrations manager table."""

    time.sleep(0.01)  # Ensure that the migrated_at is unique
    client.insert(
        MANAGER_TABLE_NAME,
        {
            "created_at": created_at,
            "previous_id": previous_id,
            "id": id,
        },
    )


def apply(
    client: Client,
    migration1: MigrationModule,
    migration2: MigrationModule,
    down: bool = False,
) -> str:
    """Apply a migration and return the operation name."""
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

    op(client)

    add_migration(
        client,
        created_at=created_at,
        id=id,
        previous_id=previous_id,
    )

    return op_name


def apply_migrations(
    client: Client,
    migrations: list[MigrationModule],
    down: bool = False,
    _rolling_back: bool = False,
    verbose: bool = False,
    from_cli: bool = True,
) -> tuple[bool, Optional[Exception]]:
    currently_applied = []
    need_to_roll_back = False
    migration_error = None

    for from_, to in paired(migrations):
        try:
            op_name = apply(client, from_, to, down=down)
            from_cli and verbose and info(f"Executed `{op_name}`.")
            currently_applied.append(from_)
        except Exception as e:
            if _rolling_back:
                # We're already rolling back, so we can't roll back again
                # Just fail
                from_cli and fail(f"Rollback failed: {e}")
                raise e

            migration_error = e
            need_to_roll_back = True
            break

    if need_to_roll_back:
        from_cli and migration_error and warn(f"Error: {migration_error}")

        # Roll back the migrations that were applied
        # in reverse order
        from_cli and warn("Migration failed. Reverting...")

        apply_migrations(
            client,
            currently_applied[::-1],
            down=(not down),
            _rolling_back=True,
            verbose=True,
            from_cli=from_cli,
        )

        return (False, migration_error)

    return (True, None)
