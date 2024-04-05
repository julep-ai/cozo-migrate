# cozo-migrate

A simple utility for migrations for cozo db

## Features

- It uses [typer](https://typer.tiangolo.com) and `pycozo` as its only dependencies.
- Loosely modeled after [hasura-migrate](https://hasura.io/docs/latest/hasura-cli/commands/hasura_migrate/) which is one of the simplest migration tools I have used.
- Auto-rollback if something goes wrong during the migrations
- Has a programmatic API for using inside tests etc.

## CLI Usage

#### Example

```bash
$ # Install cozo-migrate
$ pip install cozo-migrate

$ # Let's start a cozo server in the background
$ cozo server -e rocksdb &

$ # Let's create a migration
$ cozo-migrate -e http -d ./migrations create demo
  Writing 'migrations/migrate_1704803704_demo.py' Confirm? [y/N]: y
  ✔ Created migration at: migrations/migrate_1704803704_demo.py

$ cat migrations/migrate_1704803704_demo.py
  #/usr/bin/env python3

  MIGRATION_ID = "demo"
  CREATED_AT = 1704803704.762879

  def up(client):
      pass

  def down(client):
      pass

$ # Edit the migration to add schema change queries and then apply!
$ cozo-migrate -e http -d ./migrations apply -a
  • Migrate path: [NONE] → demo
  Are you sure you want to apply these migrations? [y/N]: y
  ✔ Database migrated.
```

#### Core options

```bash
 Usage: cozo-migrate [OPTIONS] COMMAND [ARGS]...

 A simple migration tool for Cozo databases.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --migrations-dir      -d      PATH                       Directory to use for looking up migration files. [env var: COZO_MIGRATIONS_DIR] [default: migrations] │
│ --engine              -e      [sqlite|rocksdb|http|mem]  Engine to use [env var: COZO_ENGINE] [default: EngineType.sqlite]                                     │
│ --path                -f      PATH                       Database file (not applicable for mem or http engines) [env var: COZO_PATH] [default: None]           │
│ --host                -h      TEXT                       Host to connect to (http engine only) [env var: COZO_HOST] [default: http://127.0.0.1:9070]           │
│ --auth                        TEXT                       Auth header (http engine only) [default: None]                                                        │
│ --verbose             -v                                                                                                                                       │
│ --install-completion                                     Install completion for the current shell.                                                             │
│ --show-completion                                        Show completion for the current shell, to copy it or customize the installation.                      │
│ --help                                                   Show this message and exit.                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ apply        Apply migrations to the database. You can specify the number of steps to apply and the direction.            │
│ create       Create a new migration file in the migrations directory. Format: {migration_dir}/migrate_<timestamp>_<id>.py │
│ history      Display the migration history in the database as a pretty table.                                             │
│ init         Initialize the database with the migration manager table.                                                    │
│ status       Display the current migration status.                                                                        │
│ version      Display the current version.                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Init

```bash
 Usage: cozo-migrate init [OPTIONS]

 Initialize the database with the migration manager table.

╭─ Options ───────────────────────────────────╮
│ --help          Show this message and exit. │
╰─────────────────────────────────────────────╯
```

#### Create

```bash
 Usage: cozo-migrate create [OPTIONS] ID

 Create a new migration file in the migrations directory. Format: {migration_dir}/migrate_<timestamp>_<id>.py

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    id      TEXT  A short, descriptive, alphanumeric id for the migration. Only letters, numbers, and underscores are allowed. [required]│
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --yes   -y                                                                                                                                │
│ --help            Show this message and exit.                                                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Apply

```bash
 Usage: cozo-migrate apply [OPTIONS] [STEPS]

 Apply migrations to the database. You can specify the number of steps to apply and the direction.

╭─ Arguments ────────────────────────╮
│   steps      [STEPS]  [default: 1] │
╰────────────────────────────────────╯
╭─ Options ──────────────────────────────────────╮
│ --down                                         │
│ --all   -a                                     │
│ --yes   -y                                     │
│ --help            Show this message and exit.  │
╰────────────────────────────────────────────────╯
```

#### Show

```bash
 Usage: cozo-migrate show

 Show the current schema in the database.

╭─ Options ────────────────────────────────────╮
│ --help          Show this message and exit.  │
╰──────────────────────────────────────────────╯
```

#### Status

```bash
 Usage: cozo-migrate status [OPTIONS]

 Display the current migration status.

╭─ Options ────────────────────────────────────╮
│ --help          Show this message and exit.  │
╰──────────────────────────────────────────────╯
```

#### History

```bash
 Usage: cozo-migrate history [OPTIONS]

 Display the migration history in the database as a pretty table.

╭─ Options ────────────────────────────────────╮
│ --help          Show this message and exit.  │
╰──────────────────────────────────────────────╯
```

## API Usage

```python
from cozo_migrate.api import init, apply
from pycozo import Client

migrations_dir: str = "./migrations"

# Create a new client for testing
# and initialize the schema.
client = Client()

# Initialize the migration schema
init(client)

# Apply migrations from the migration directory
apply(client, migrations_dir=migrations_dir, all_=True)
```
