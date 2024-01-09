#!/usr/bin/env python3

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import cast, Optional

from pycozo.client import Client

from .types import MigrationModule, MigrationModuleInfo
from .utils.fn import create_obj


class NullMigrationModule(MigrationModule):
    MIGRATION_ID: Optional[str] = None
    CREATED_AT: Optional[float] = None

    @staticmethod
    def up(client: Client) -> None:
        ...

    @staticmethod
    def down(client: Client) -> None:
        ...


def sanity_check(module: MigrationModule) -> None:
    for attr in ["up", "down", "MIGRATION_ID", "CREATED_AT"]:
        assert hasattr(
            module, attr
        ), f"Missing {attr} attribute in migration:{module.__file__}"


def import_migration_file(path: str | Path) -> MigrationModule:
    path = Path(path)
    module_name: str = path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module: ModuleType = importlib.util.module_from_spec(spec)

    if not (spec and module):
        raise Exception(f"Could not import migration file: {path}")

    spec.loader.exec_module(module)

    module = cast(MigrationModule, module)
    sanity_check(module)

    return module


def get_adjacent_migrations(
    migration_files: list[MigrationModuleInfo],
    starting_id: Optional[str],
    num: int,
    down: bool = False,
) -> list[MigrationModule]:
    """Get the next num migrations after the starting_id."""

    # Add None to the beginning of the list
    migration_files = [create_obj(id=None)] + migration_files

    # Reverse the list if we're going down
    migration_files = migration_files[::-1] if down else migration_files

    # Get the index of the starting_id
    start = next(
        (i for i, m in enumerate(migration_files) if m.id == starting_id), None
    )

    assert start is not None, f"Migration {starting_id} not found."

    end = start + num + 1

    # Load the migration files
    migrations: list[MigrationModule] = [
        import_migration_file(m_file.path)
        if m_file.id is not None
        else NullMigrationModule("", "")
        for m_file in migration_files[start:end]
    ]

    return migrations
