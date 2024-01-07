from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

from pycozo.client import Client
import typer

from ..types import AppContext, CozoConnectionOptions
from ..utils.client import is_connected
from ..utils.console import fail

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.callback()
def main(
    ctx: typer.Context,
    migrations_dir: Annotated[Path, typer.Option(help="Directory to use")] = Path(
        "./migrations"
    ),
    engine: Annotated[str, typer.Option(help="Engine to use")] = "sqlite",
    path: Annotated[
        Path,
        typer.Option(help="Database file (not applicable for mem or http engines)"),
    ] = Path("./cozo.db"),
    host: Annotated[
        str, typer.Option(help="Host to connect to (http engine only)")
    ] = "http://127.0.0.1:9070",
    auth: Annotated[
        Optional[str], typer.Option(help="Auth header (http engine only)")
    ] = None,
):
    """
    A simple migration tool for Cozo databases.
    """

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
    )

    ctx.obj = app_context
