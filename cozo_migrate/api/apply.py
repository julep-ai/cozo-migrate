from pathlib import Path
from typing import Optional

from pycozo.client import Client

from ..files import get_migration_files
from ..modules import get_adjacent_migrations
from ..ops import apply_migrations
from ..queries import get_latest_migration
from ..types import Migration, MigrationModule, MigrationModuleInfo


def apply(
    client: Client,
    migrations_dir: str | Path,
    steps: int = 1,
    all_: bool = False,
    down: bool = False,
):
    """
    Apply migrations to the database.
    You can specify the number of steps to apply and the direction.
    """

    # Get the current migration
    current_migration: Optional[Migration] = get_latest_migration(client)
    current_id: Optional[str] = current_migration.id if current_migration else None

    if down and current_id is None:
        raise ValueError("No migrations to rollback.")

    # Find migrations in migrations_dir
    migration_files: list[MigrationModuleInfo] = get_migration_files(migrations_dir)
    num_migrations_available = len(migration_files)
    assert num_migrations_available > 0, "No migrations found."

    # If all migrations are requested, set steps to the number of migrations available
    if all_:
        steps = num_migrations_available

    # Get the next steps migrations from starting_id (can be negative)
    migrations: list[MigrationModule] = get_adjacent_migrations(
        migration_files, current_id, steps, down
    )

    assert len(migrations) > 0, "No migrations to apply."

    applied_successfully, migration_error = apply_migrations(
        client, migrations, down=down, verbose=False, from_cli=False
    )

    if not applied_successfully:
        raise ValueError("Migration failed.") from migration_error
