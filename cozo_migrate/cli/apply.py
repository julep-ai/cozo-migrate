from typing import Optional
from typing_extensions import Annotated

import typer

from ..files import get_migration_files
from ..history import get_latest_migration
from ..modules import get_adjacent_migrations
from ..ops import apply_migrations
from ..schema import schema_exists
from ..types import Migration, MigrationModule, MigrationModuleInfo
from ..utils.console import fail, success, info

from .main import app


# TODO: Add a flag to apply all migrations
@app.command()
def apply(
    ctx: typer.Context,
    steps: Annotated[int, typer.Argument()] = 1,
    down: Annotated[bool, typer.Option("--down")] = False,
):
    """
    Apply migrations to the database.
    You can specify the number of steps to apply and the direction.
    """

    client = ctx.obj.client
    migrations_dir = ctx.obj.migrations_dir
    verbose = ctx.obj.verbose

    if not schema_exists(client):
        fail("Schema does not exist. Run `init` first.")

    # Get the current migration
    current_migration: Optional[Migration] = get_latest_migration(client)
    current_id: Optional[str] = current_migration.id if current_migration else None

    if down and current_id is None:
        fail("No migrations to rollback.")

    # Find migrations in migrations_dir
    migration_files: list[MigrationModuleInfo] = get_migration_files(migrations_dir)
    if len(migration_files) == 0:
        fail("No migrations found.")

    # Get the next steps migrations from starting_id (can be negative)
    migrations: list[MigrationModule] = get_adjacent_migrations(
        migration_files, current_id, steps, down
    )

    if len(migrations) == 0:
        fail("No migrations to apply.")

    # Print the migration path
    joiner = "[yellow] → [/yellow]"
    migration_ids = [m.MIGRATION_ID or "[NONE]" for m in migrations]

    info(f"Migrate path: {joiner.join(migration_ids)}")

    # Confirm
    confirm = typer.confirm("Are you sure you want to apply these migrations?")
    if not confirm:
        raise typer.Abort()

    info("Migrating the database...")
    applied_successfully = apply_migrations(
        client, migrations, down=down, verbose=verbose
    )

    if applied_successfully:
        success("Database migrated.")
    else:
        fail("Migration failed.")
