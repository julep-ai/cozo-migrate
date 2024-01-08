from rich import print
import typer

from ..history import get_history
from ..schema import schema_exists
from ..utils.console import fail
from ..utils.rich import df_to_table, pretty_transforms

from .main import app


@app.command()
def history(ctx: typer.Context):
    """Display the migration history in the database as a pretty table."""

    client = ctx.obj.client

    if not schema_exists(client):
        fail("Schema does not exist. Run `init` first.")

    history = get_history(client).transform(pretty_transforms)
    history_table = df_to_table(history)

    print(history_table)
