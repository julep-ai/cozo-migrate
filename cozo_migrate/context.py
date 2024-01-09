#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pycozo.client import Client

from .schema import schema_exists
from .types import EngineType, CozoConnectionOptions
from .utils.client import is_connected
from .utils.console import fail


@dataclass
class AppContext:
    engine: EngineType
    path: Path
    options: CozoConnectionOptions
    migrations_dir: Path
    verbose: bool
    _client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(self.engine, str(self.path), options=self.options)

        return self._client

    def ensure_connected(self) -> None:
        if not is_connected(self.client):
            fail("Could not connect to database")

    def ensure_schema(self) -> None:
        # Ensure schema exists
        if not schema_exists(self.client):
            fail("Schema does not exist. Run `cozo-migrate init` first.")

    def validate_options(self) -> None:
        # Validate options
        if self.engine in (EngineType.sqlite, EngineType.rocksdb):
            if not self.path:
                fail(
                    "`--path / -f` is required for sqlite and rocksdb engines"
                    "\n\n"
                    "Example:\n"
                    "$ cozo-migrate -e sqlite -f ./mydb.db [COMMAND] [OPTIONS]"
                )

            self.path = self.path.resolve()

        if self.engine == EngineType.http:
            if not (self.options and self.options.get("host")):
                fail("`--host / -h` is required for http engine")

    def check_client(self) -> None:
        self.validate_options()
        self.ensure_connected()
        self.ensure_schema()
