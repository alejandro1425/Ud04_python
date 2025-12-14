"""Módulo responsable de gestionar la conexión con la base de datos SQLite.

Se inspira en el tutorial oficial de Flask pero añade anotaciones de tipos y
comentarios para facilitar la comprensión.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from flask import current_app, g
from flask.cli import with_appcontext
import click


def get_db() -> sqlite3.Connection:
    """Crea una conexión a la base de datos si no existe y la almacena en ``g``.

    Returns:
        Conexión SQLite con ``row_factory`` configurada para devolver diccionarios.
    """

    if "db" not in g:
        db_path = current_app.config["DATABASE"]
        connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def close_db(_: Any = None) -> None:
    """Cierra la conexión de base de datos asociada al contexto actual."""

    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Inicializa las tablas necesarias ejecutando el script SQL incluido."""

    db = get_db()
    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Comando de CLI: ``flask init-db`` para crear las tablas desde cero."""

    init_db()
    click.echo("Base de datos inicializada correctamente.")


def init_app(app: Any) -> None:
    """Registra los manejadores necesarios en la aplicación."""

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
