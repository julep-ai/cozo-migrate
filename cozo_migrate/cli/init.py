import typer

from ..schema import schema_exists, create_schema
from ..utils.console import fail, success, info

from .main import app


@app.command()
def init(ctx: typer.Context):
    """Initialize the database with the migration history table (under the name `migrations_manager`)."""

    client = ctx.obj.client

    if schema_exists(client):
        fail("Schema already exists.")

    else:
        info("Initializing the database")
        create_schema(client)
        success("Schema created.")
