import os
from pathlib import Path
from typing import cast, Optional

from .types import EngineType

##########
## main ##
##########

DEFAULT_MIGRATIONS_DIR: Path = Path(
    os.environ.get("COZO_DEFAULT_MIGRATIONS_DIR", "./migrations")
)

DEFAULT_ENGINE: EngineType = cast(
    EngineType, os.environ.get("COZO_DEFAULT_ENGINE", EngineType.sqlite)
)

DEFAULT_HOST: str = os.environ.get("COZO_DEFAULT_HOST", "http://127.0.0.1:9070")

DEFAULT_AUTH: Optional[str] = os.environ.get("COZO_DEFAULT_AUTH", None)

DEFAULT_VERBOSE: bool = os.environ.get("COZO_DEFAULT_VERBOSE", False)
