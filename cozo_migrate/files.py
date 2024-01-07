#!/usr/bin/env python3

import os
from pathlib import Path

from .types import MigrationModuleInfo


def get_migration_files(migrations_dir: str | Path) -> list[MigrationModuleInfo]:
    files: list[MigrationModuleInfo] = []

    for f in os.listdir(migrations_dir):
        path = os.path.join(migrations_dir, f)
        if not (os.path.isfile(path) and f.startswith("migrate_")):
            continue

        slug = f.replace("migrate_", "").replace(".py", "")
        timestamp, *id_parts = slug.split("_")
        timestamp = int(timestamp)
        id = "_".join(id_parts)

        files.append(
            MigrationModuleInfo(
                path=path,
                id=id,
                created_at=timestamp,
            )
        )

    return sorted(files, key=lambda f: f.created_at)
