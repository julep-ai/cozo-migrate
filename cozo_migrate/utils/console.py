#!/usr/bin/env python3

from rich.console import Console
import typer


console = Console(stderr=True)
error_console = Console(stderr=True)


def warn(msg: str, console=console) -> None:
    console.print(f"[bold yellow]⚠[/bold yellow] {msg}")


def info(msg: str, console=console) -> None:
    console.print(f"[bold blue]•[/bold blue] {msg}")


def fail(msg: str, console=error_console) -> None:
    console.print(f"[bold red]❌[/bold red] {msg}")
    console.print()

    raise typer.Exit(1)


def success(msg: str, console=console) -> None:
    console.print(f"[bold green]✔[/bold green] {msg}")
    console.print()

    raise typer.Exit(0)
