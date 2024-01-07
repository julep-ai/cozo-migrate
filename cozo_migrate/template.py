#!/usr/bin/env python3

migration_template = """\
#/usr/bin/env python3

MIGRATION_ID = "{migration_id}"
CREATED_AT = {created_at}

def up(client):
    pass

def down(client):
    pass
"""
