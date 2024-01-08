from rich import print
import typer

from ..history import get_latest_migration
from ..schema import schema_exists
from ..types import Migration
from ..utils.console import fail

from .main import app


@app.command()
def status(ctx: typer.Context):
    """Display the current migration status."""

    client = ctx.obj.client

    if not schema_exists(client):
        fail("Schema does not exist. Run `init` first.")

    last_migration: Migration = get_latest_migration(client)
    if not last_migration:
        fail("No migrations have been applied yet.")

    print(last_migration.to_table())
