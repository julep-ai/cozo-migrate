from typing import Optional

from rich import print
import typer

from ..queries import get_current_schema
from ..types import Migration
from ..utils.console import fail
from ..utils.rich import df_to_table, pretty_transforms

from .main import app


@app.command()
def show(ctx: typer.Context):
    """Show the current schema in the database."""

    # Validate client
    ctx.obj.check_client()

    client = ctx.obj.client

    db_schema = get_current_schema(client)

    for relation, columns in db_schema.items():
        print(f"[bold][blue]\[{relation}][/blue][/bold]")
        print(df_to_table(columns))
        print()
