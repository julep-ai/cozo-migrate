from datetime import datetime
import re

import typer

from ..files import get_migration_files
from ..template import migration_template
from ..utils.console import fail, success

from .main import app


@app.command()
def create(id: str, ctx: typer.Context):
    migrations_dir = ctx.obj.migrations_dir

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
    ts = datetime.utcnow().timestamp()
    path = migrations_dir / f"migrate_{int(ts)}_{id}.py"

    with open(path, "w") as f:
        f.write(migration_template.format(migration_id=id, created_at=ts))

    success(f"Created migration at: {path}")
