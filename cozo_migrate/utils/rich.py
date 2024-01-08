#!/usr/bin/env python3

from typing import Optional

import numpy as np
import pandas as pd
from rich import box
from rich.table import Table

from .fn import maybe_apply, format_ts


def reject_nullish(x):
    return x is None or np.isnan(x)


pretty_transforms = dict(
    created_at=lambda x: maybe_apply(format_ts, x, reject_if=reject_nullish) or "---",
    migrated_at=lambda x: maybe_apply(format_ts, x, reject_if=reject_nullish) or "---",
    id=lambda x: f"[bold green]{x}[/bold green]" if x else "---",
    previous_id=lambda x: f"[bold red]{x}[/bold red]" if x else "---",
)


def dict_to_table(data: dict) -> Table:
    """Convert a dict into a rich.Table obj.
    Args:
        data (dict): A dictionary to be converted to a rich Table.
    Returns:
        Table: a rich Table instance populated with the dictionary values."""

    rich_table: Table = Table(box=box.SQUARE)

    columns, values = list(zip(*data.items()))
    for column in columns:
        rich_table.add_column(str(column))

    rich_table.add_row(*map(str, values))

    return rich_table


def df_to_table(
    pandas_dataframe: pd.DataFrame,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.
    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: a rich Table instance populated with the DataFrame values."""

    rich_table: Table = Table(box=box.SQUARE)

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table
