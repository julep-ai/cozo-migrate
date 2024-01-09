#!/usr/bin/env python3

from dataclasses import asdict, dataclass
from enum import Enum
from types import ModuleType
from typing import Any, Optional, TypedDict

import pandas as pd
from pycozo.client import Client
from rich.table import Table

from .utils.rich import dict_to_table, pretty_transforms


class EngineType(str, Enum):
    sqlite = "sqlite"
    rocksdb = "rocksdb"
    http = "http"
    mem = "mem"


@dataclass
class Migration:
    id: Optional[str] = None
    previous_id: Optional[str] = None
    created_at: Optional[float] = None
    migrated_at: Optional[int] = None

    def to_pretty_dict(self) -> dict[str, Any]:
        data = asdict(self)
        pretty_dict = {k: pretty_transforms[k](v) for k, v in data.items()}

        return pretty_dict

    def to_table(self) -> Table:
        return dict_to_table(self.to_pretty_dict())

    @classmethod
    def from_pandas(cls, df: pd.DataFrame) -> list["Migration"]:
        return [cls(**row) for row in df.to_dict(orient="records")]

    @classmethod
    def get_first(cls, df: pd.DataFrame, default: Any = None) -> "Migration":
        items = cls.from_pandas(df)
        return items[0] if items else default


class MigrationModule(ModuleType):
    MIGRATION_ID: Optional[str]
    CREATED_AT: Optional[float]

    @staticmethod
    def up(client: Client) -> None:
        ...

    @staticmethod
    def down(client: Client) -> None:
        ...


@dataclass
class MigrationModuleInfo:
    path: str
    id: str
    created_at: int


class CozoConnectionOptions(TypedDict):
    host: str
    auth: Optional[str]
