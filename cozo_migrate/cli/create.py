import re
from typing_extensions import Annotated

import typer

from ..files import get_migration_files
from ..template import migration_template
from ..utils.console import fail, success
from ..utils.datetime import utcnow

from .main import app


@app.command()
def create(
    ctx: typer.Context,
    id: Annotated[
        str,
        typer.Argument(
            ...,
            help="A short, descriptive, alphanumeric id for the migration. Only letters, numbers, and underscores are allowed.",
        ),
    ],
    confirm: Annotated[bool, typer.Option("--yes", "-y")] = False,
):
    """
    Create a new migration file in the migrations directory.
    Format: {migration_dir}/migrate_<timestamp>_<id>.py
    """

    migrations_dir = ctx.obj.migrations_dir

    # Create migrations_dir if it doesn't exist
    migrations_dir.mkdir(parents=True, exist_ok=True)

    # id can only contain letters, numbers, and underscores
    # can only start with a lowercase letter
    regex = r"^[a-z][a-zA-Z0-9_]*$"
    if not re.match(regex, id):
        fail("`id` can only contain letters, numbers, and underscores")

    # Check that a migration with same id doesn't already exist
    migration_files = get_migration_files(migrations_dir)
    any_existing = any(m.id == id for m in migration_files)
    if any_existing:
        fail(f"A migration with id `{id}` already exists.")

    # Create the migration file
    ts = utcnow().timestamp()
    path = migrations_dir / f"migrate_{int(ts)}_{id}.py"

    # Confirm
    if not confirm:
        confirmed = typer.confirm(f"Writing '{path}' Confirm?")
        if not confirmed:
            raise typer.Abort()

    with open(path, "w") as f:
        f.write(migration_template.format(migration_id=id, created_at=ts))

    success(f"Created migration at: {path}")
