# cozo-migrate

A simple utility for migrations for cozo db

## Usage

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
