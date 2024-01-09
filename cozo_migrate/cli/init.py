import typer

from ..schema import create_schema, schema_exists
from ..utils.console import success, info, fail

from .main import app


@app.command()
def init(ctx: typer.Context):
    """Initialize the database with the migration manager table."""

    # Validate client
    ctx.obj.validate_options()

    client = ctx.obj.client

    if schema_exists(client):
        fail("Schema already exists.")

    else:
        info("Initializing the database")
        create_schema(client)
        success("Schema created.")
