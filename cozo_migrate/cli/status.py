from rich import print
import typer

from ..history import get_latest_migration
from ..types import Migration
from ..utils.console import fail

from .main import app


@app.command()
def status(ctx: typer.Context):
    """Display the current migration status."""

    # Validate client
    ctx.obj.check_client()

    client = ctx.obj.client

    last_migration: Migration = get_latest_migration(client)
    if not last_migration:
        fail("No migrations have been applied yet.")

    print(last_migration.to_table())
