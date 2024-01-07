#!/usr/bin/env python3

from pycozo.client import Client

from .fn import doesnt_throw


@doesnt_throw
def is_connected(client: Client) -> bool:
    client.run("?[a] <- [[1]]")
    return True
