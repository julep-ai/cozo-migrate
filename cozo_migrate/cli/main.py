from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

import typer

from ..context import AppContext
from ..types import CozoConnectionOptions, EngineType

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.callback()
def main(
    ctx: typer.Context,
    migrations_dir: Annotated[
        Path,
        typer.Option(
            "--migrations-dir",
            "-d",
            help="Directory to use for looking up migration files.",
            envvar="COZO_MIGRATIONS_DIR",
        ),
    ] = Path("./migrations"),
    engine: Annotated[
        EngineType,
        typer.Option("--engine", "-e", help="Engine to use", envvar="COZO_ENGINE"),
    ] = EngineType.sqlite,
    path: Annotated[
        Optional[Path],
        typer.Option(
            "--path",
            "-f",
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

    # Prepare context
    options: CozoConnectionOptions = {"host": host, "auth": auth}

    app_context: AppContext = AppContext(
        engine=engine,
        path=path,
        options=options,
        migrations_dir=migrations_dir,
        verbose=verbose,
    )

    ctx.obj = app_context
