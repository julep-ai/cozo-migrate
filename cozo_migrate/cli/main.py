from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

from pycozo.client import Client
import typer

from ..defaults import (
    DEFAULT_ENGINE,
    DEFAULT_HOST,
    DEFAULT_AUTH,
    DEFAULT_MIGRATIONS_DIR,
    DEFAULT_VERBOSE,
)
from ..types import AppContext, CozoConnectionOptions, EngineType
from ..utils.client import is_connected
from ..utils.console import fail

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.callback()
def main(
    ctx: typer.Context,
    migrations_dir: Annotated[
        Path,
        typer.Option(
            "--migrations-dir",
            "-m",
            help="Directory to use for looking up migration files.",
        ),
    ] = DEFAULT_MIGRATIONS_DIR,
    engine: Annotated[
        EngineType, typer.Option("--engine", "-e", help="Engine to use")
    ] = DEFAULT_ENGINE,
    path: Annotated[
        Optional[Path],
        typer.Option(help="Database file (not applicable for mem or http engines)"),
    ] = None,
    host: Annotated[
        str, typer.Option(help="Host to connect to (http engine only)")
    ] = DEFAULT_HOST,
    auth: Annotated[
        Optional[str], typer.Option(help="Auth header (http engine only)")
    ] = DEFAULT_AUTH,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = DEFAULT_VERBOSE,
):
    """
    A simple migration tool for Cozo databases.
    """

    # Validate options
    if engine in (EngineType.sqlite, EngineType.rocksdb):
        if not path:
            fail("`--path` is required for sqlite and rocksdb engines")

        path = path.resolve()

    # Connect to database
    options: CozoConnectionOptions = {"host": host, "auth": auth}
    client = Client(engine, str(path), options=options)

    if not is_connected(client):
        fail("Could not connect to database")

    migrations_dir.mkdir(parents=True, exist_ok=True)

    app_context: AppContext = AppContext(
        client=client,
        engine=engine,
        path=path,
        options=options,
        migrations_dir=migrations_dir,
        verbose=verbose,
    )

    ctx.obj = app_context
