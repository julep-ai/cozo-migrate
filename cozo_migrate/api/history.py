from pycozo.client import Client

from ..queries import get_history


def history(client: Client):
    """Get the migration history in the database as a pandas dataframe."""

    history = get_history(client)
    return history
