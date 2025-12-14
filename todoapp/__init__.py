"""Aplicación Flask para la gestión de tareas pendientes con autenticación.

Este módulo inicializa la aplicación utilizando el patrón de fábrica recomendado
por Flask. La configuración se carga desde un fichero específico de entorno o se
usa una base de datos SQLite por defecto. También registra los *blueprints* de
autenticación y tareas.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask

from . import auth, db, tasks


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Crea y configura la instancia de la aplicación Flask.

    Args:
        test_config: Diccionario opcional con valores de configuración para
            pruebas. Si se proporciona, evita cargar la configuración por
            defecto y permite usar una base de datos temporal.

    Returns:
        Instancia de :class:`~flask.Flask` configurada y lista para usar.
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="desarrollo-seguro",  # En despliegues reales, cargar desde env.
        DATABASE=Path(app.instance_path) / "todoapp.sqlite",
    )

    if test_config is None:
        # Cargar variables desde un fichero config.py en la carpeta instance si existe.
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    # Asegurarse de que existe la carpeta instance (para la base de datos).
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        # En entornos de CI la carpeta puede no ser necesaria, así que ignoramos errores.
        pass

    # Inicializar base de datos y registrar blueprints.
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)

    # Ruta principal: redirige al tablero de tareas.
    @app.route("/")
    def home() -> Any:
        return tasks.dashboard()

    return app
