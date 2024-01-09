# /usr/bin/env python3

MIGRATION_ID = "init"
CREATED_AT = 1704506472.363848


def up(client):
    client.run(
        """
    :create test {
        name: String,
    }
    """
    )


def down(client):
    client.run(
        """
    ::remove test
    """
    )
