from pathlib import Path
import re

from ..files import get_migration_files
from ..template import migration_template
from ..utils.datetime import utcnow


def create(
    id: str,
    migration_dir: str | Path,
) -> None:
    """
    Create a new migration file in the migrations directory.
    Format: {migration_dir}/migrate_<timestamp>_<id>.py
    """

    # Create migrations_dir if it doesn't exist
    migrations_dir = Path(migration_dir)
    migrations_dir.mkdir(parents=True, exist_ok=True)

    # id can only contain letters, numbers, and underscores
    # can only start with a lowercase letter
    regex = r"^[a-z][a-zA-Z0-9_]*$"
    assert re.match(
        regex, id
    ), "`id` can only contain letters, numbers, and underscores"

    # Check that a migration with same id doesn't already exist
    migration_files = get_migration_files(migrations_dir)
    any_existing = any(m.id == id for m in migration_files)

    assert not any_existing, f"A migration with id `{id}` already exists."

    # Create the migration file
    ts = utcnow().timestamp()
    path = migrations_dir / f"migrate_{int(ts)}_{id}.py"

    with open(path, "w") as f:
        f.write(migration_template.format(migration_id=id, created_at=ts))
