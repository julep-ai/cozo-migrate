from typing import Optional

from rich import print
import typer

from ..queries import get_latest_migration
from ..types import Migration
from ..utils.console import fail

from .main import app


@app.command()
def status(ctx: typer.Context):
    """Display the current migration status."""

    # Validate client
    ctx.obj.check_client()

    client = ctx.obj.client

    last_migration: Optional[Migration] = get_latest_migration(client)
    if last_migration is None:
        fail("No migrations have been applied yet.")

    else:
        print(last_migration.to_table())
