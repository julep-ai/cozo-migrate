# cozo-migrate
A simple utility for migrations for cozo db

## Usage

#### Core options

```bash
cozo-migrate --help

 Usage: cozo-migrate [OPTIONS] COMMAND [ARGS]...

 A simple migration tool for Cozo databases.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --migrations-dir      -m      PATH                       Directory to use for looking up migration files. [default: migrations]          │
│ --engine              -e      [sqlite|rocksdb|http|mem]  Engine to use [default: EngineType.sqlite]                                      │
│ --path                        PATH                       Database file (not applicable for mem or http engines) [default: None]          │
│ --host                        TEXT                       Host to connect to (http engine only) [default: http://127.0.0.1:9070]          │
│ --auth                        TEXT                       Auth header (http engine only) [default: None]                                  │
│ --verbose             -v                                                                                                                 │
│ --install-completion                                     Install completion for the current shell.                                       │
│ --show-completion                                        Show completion for the current shell, to copy it or customize the installation.│
│ --help                                                   Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ apply        Apply migrations to the database. You can specify the number of steps to apply and the direction.                           │
│ create       Create a new migration file in the migrations directory. Format: {migration_dir}/migrate_<timestamp>_<id>.py                │
│ history      Display the migration history in the database as a pretty table.                                                            │
│ init         Initialize the database with the migration history table (under the name `migrations_manager`).                             │
│ status       Display the current migration status.                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Init

```bash
cozo-migrate --path ./cozo.db init --help

 Usage: cozo-migrate init [OPTIONS]

 Initialize the database with the migration history table (under the name `migrations_manager`).
```

#### Create

```bash
cozo-migrate --path ./cozo.db create --help

 Usage: cozo-migrate create [OPTIONS] ID

 Create a new migration file in the migrations directory. Format: {migration_dir}/migrate_<timestamp>_<id>.py

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    id      TEXT  A short, descriptive, alphanumeric id for the migration. Only letters, numbers, and underscores are allowed.          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Apply

```bash
cozo-migrate --path ./cozo.db apply --help

 Usage: cozo-migrate apply [OPTIONS] [STEPS]

 Apply migrations to the database. You can specify the number of steps to apply and the direction.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────╮
│   steps      [STEPS]  [default: 1]                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --down                                                                                            │
│ --help          Show this message and exit.                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Status

```bash
cozo-migrate --path ./cozo.db status --help

 Usage: cozo-migrate status [OPTIONS]

 Display the current migration status.

```

#### History

```bash
cozo-migrate --path ./cozo.db history --help

 Usage: cozo-migrate history [OPTIONS]

 Display the migration history in the database as a pretty table.

```
