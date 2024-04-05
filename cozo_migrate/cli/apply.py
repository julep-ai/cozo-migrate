from typing import Optional
from typing_extensions import Annotated

import typer

from ..files import get_migration_files
from ..modules import get_adjacent_migrations
from ..ops import apply_migrations
from ..queries import get_latest_migration
from ..types import Migration, MigrationModule, MigrationModuleInfo
from ..utils.console import fail, success, info

from .main import app


@app.command()
def apply(
    ctx: typer.Context,
    steps: Annotated[int, typer.Argument()] = 1,
    down: Annotated[bool, typer.Option("--down")] = False,
    all_: Annotated[bool, typer.Option("--all", "-a")] = False,
    confirm: Annotated[bool, typer.Option("--yes", "-y")] = False,
    compact: Annotated[bool, typer.Option("--compact")] = False,
):
    """
    Apply migrations to the database.
    You can specify the number of steps to apply and the direction.
    """

    # Validate client
    ctx.obj.check_client()

    client = ctx.obj.client
    migrations_dir = ctx.obj.migrations_dir
    verbose = ctx.obj.verbose

    # Get the current migration
    current_migration: Optional[Migration] = get_latest_migration(client)
    current_id: Optional[str] = current_migration.id if current_migration else None

    if down and current_id is None:
        fail("No migrations to rollback.")

    # Find migrations in migrations_dir
    migration_files: list[MigrationModuleInfo] = get_migration_files(migrations_dir)
    num_migrations_available = len(migration_files)
    if num_migrations_available == 0:
        fail("No migrations found.")

    # If all migrations are requested, set steps to the number of migrations available
    if all_:
        steps = num_migrations_available

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
    if not confirm:
        confirmed = typer.confirm("Are you sure you want to apply these migrations?")
        if not confirmed:
            raise typer.Abort()

    info("Migrating the database...")
    applied_successfully, migration_error = apply_migrations(
        client, migrations, down=down, verbose=verbose, from_cli=True
    )

    if compact:
        client.run("::compact")
        info("Database compaction initiated.")

    if applied_successfully:
        success("Database migrated.")
    else:
        fail("Migration failed.", error=migration_error)
