from pycozo.client import Client

from ..schema import create_schema, schema_exists


def init(client: Client):
    """Initialize the database with the migration manager table."""

    assert not schema_exists(client), "Schema already exists."
    create_schema(client)
