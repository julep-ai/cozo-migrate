from typing import Optional

from pycozo.client import Client

from ..queries import get_latest_migration
from ..types import Migration


def status(client: Client):
    """Display the current migration status."""

    last_migration: Optional[Migration] = get_latest_migration(client)
    assert last_migration is not None, "No migrations have been applied yet."

    return last_migration
