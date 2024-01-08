from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

from pycozo.client import Client
import typer

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
            envvar="COZO_MIGRATIONS_DIR",
        ),
    ] = "./migrations",
    engine: Annotated[
        EngineType,
        typer.Option("--engine", "-e", help="Engine to use", envvar="COZO_ENGINE"),
    ] = EngineType.sqlite,
    path: Annotated[
        Optional[Path],
        typer.Option(
            "--path",
            "-p",
            help="Database file (not applicable for mem or http engines)",
            envvar="COZO_PATH",
        ),
    ] = None,
    host: Annotated[
        str,
        typer.Option(
            "--host",
            "-h",
            help="Host to connect to (http engine only)",
            envvar="COZO_HOST",
        ),
    ] = "http://127.0.0.1:9070",
    auth: Annotated[
        Optional[str],
        typer.Option(
            help="Auth header (http engine only)", envvar="COZO_AUTH", show_envvar=False
        ),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
):
    """
    A simple migration tool for Cozo databases.
    """

    # Validate options
    if engine in (EngineType.sqlite, EngineType.rocksdb):
        if not path:
            fail(
                "`--path` is required for sqlite and rocksdb engines"
                "\n\n"
                "Example:\n"
                "$ cozo-migrate --engine sqlite --path ./mydb.db [COMMAND] [OPTIONS]"
            )

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
