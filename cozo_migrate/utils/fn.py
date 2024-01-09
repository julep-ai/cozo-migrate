#!/usr/bin/env python3

from datetime import datetime
from functools import wraps
from typing import Callable, Any


def format_ts(ts):
    return datetime.fromtimestamp(int(ts))


def doesnt_throw(fn: Callable[..., Any]) -> Callable[..., bool]:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
            return True

        except Exception:
            return False

    return wrapper


def maybe_apply(
    fn: Callable[..., Any],
    value: Any,
    reject_if: Callable[[Any], bool] = lambda x: x is None,
) -> Any:
    if reject_if(value):
        return None

    return fn(value)


def paired(lst):
    return [*zip(lst[:-1], lst[1:])]


def create_obj(**kwargs):
    return type("obj", (), kwargs)()
