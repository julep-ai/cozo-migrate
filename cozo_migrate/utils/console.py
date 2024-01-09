#!/usr/bin/env python3

from typing import Optional

from rich.console import Console
import typer


console = Console(stderr=True)
error_console = Console(stderr=True)


def warn(msg: str, console=console) -> None:
    console.print(f"[bold yellow]⚠[/bold yellow] {msg}")


def info(msg: str, console=console) -> None:
    console.print(f"[bold blue]•[/bold blue] {msg}")


def fail(
    msg: str, console=error_console, error: Optional[BaseException] = None
) -> None:
    console.print(f"[bold red]❌[/bold red] {msg}")
    console.print()

    raise typer.Exit(1) from error


def success(msg: str, console=console) -> None:
    console.print(f"[bold green]✔[/bold green] {msg}")
    console.print()

    raise typer.Exit(0)
