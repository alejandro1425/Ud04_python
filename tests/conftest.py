"""Configuración de pruebas para pytest.

Se reutiliza el patrón del tutorial de Flask pero adaptado a nuestra estructura
(español y tablas personalizadas).
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Asegura que la carpeta raíz del proyecto esté en ``sys.path`` para que ``todoapp``
# se importe correctamente incluso cuando las herramientas de pruebas cambien el
# directorio de trabajo.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from todoapp import create_app
from todoapp.db import get_db, init_db


@pytest.fixture()
def app() -> Generator:
    """Crea una instancia de la aplicación para pruebas con una base de datos temporal."""

    db_fd, db_path = tempfile.mkstemp()
    try:
        app = create_app({"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "test"})

        with app.app_context():
            init_db()
            # Cargar datos de ejemplo para acelerar las pruebas.
            with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
                get_db().executescript(f.read().decode("utf8"))

        yield app
    finally:
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture()
def client(app):
    """Cliente de prueba para enviar peticiones HTTP a la aplicación."""

    return app.test_client()


@pytest.fixture()
def runner(app):
    """Permite ejecutar comandos de la CLI de Flask en pruebas."""

    return app.test_cli_runner()
