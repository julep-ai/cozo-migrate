from rich import print
import typer

from ..queries import get_history
from ..utils.rich import df_to_table, pretty_transforms

from .main import app


@app.command()
def history(ctx: typer.Context):
    """Display the migration history in the database as a pretty table."""

    # Validate client
    ctx.obj.check_client()

    client = ctx.obj.client

    history = get_history(client).transform(pretty_transforms)
    history_table = df_to_table(history)

    print(history_table)
