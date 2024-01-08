from importlib import metadata

from ..utils.console import info
from .main import app


@app.command()
def version():
    """Display the current version."""

    info(f"cozo-migrate {metadata.version('cozo-migrate')}")
