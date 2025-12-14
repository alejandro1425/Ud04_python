"""Pruebas del flujo de tareas (CRUD y marcado de completadas)."""
from __future__ import annotations

import pytest

from todoapp.db import get_db


@pytest.fixture()
def auth(client):
    """Ayuda a iniciar sesión en las pruebas."""

    client.post("/auth/login", data={"username": "usuario", "password": "test"})
    yield


def test_dashboard_requires_login(client):
    """Sin autenticación se redirige a la página de login."""

    response = client.get("/tareas/", follow_redirects=True)
    assert "Para continuar inicia sesión" in response.get_data(as_text=True)


def test_create_task(auth, client, app):
    """Se puede crear una nueva tarea y aparece en el tablero."""

    response = client.post("/tareas/crear", data={"titulo": "Nueva", "descripcion": "texto"}, follow_redirects=True)
    assert "Tarea creada" in response.get_data(as_text=True)

    with app.app_context():
        count = get_db().execute("SELECT COUNT(*) FROM tarea").fetchone()[0]
        assert count == 2  # Se suma a la tarea inicial de pruebas.

    dashboard = client.get("/tareas/", follow_redirects=True)
    assert b"Nueva" in dashboard.data


def test_update_task(auth, client):
    """Actualizar una tarea modifica el título."""

    response = client.post(
        "/tareas/1/editar", data={"titulo": "Actualizada", "descripcion": "nueva"}, follow_redirects=True
    )
    assert "Tarea actualizada" in response.get_data(as_text=True)
    assert "Actualizada" in client.get("/tareas/", follow_redirects=True).get_data(as_text=True)


def test_toggle_complete(auth, client):
    """Se puede marcar y desmarcar una tarea como completada."""

    response = client.post("/tareas/1/completar", follow_redirects=True)
    assert "marcada como completada" in response.get_data(as_text=True)

    response = client.post("/tareas/1/completar", follow_redirects=True)
    assert "marcada como pendiente" in response.get_data(as_text=True)


def test_delete_task(auth, client):
    """Eliminar una tarea elimina sus datos."""

    response = client.post("/tareas/1/borrar", follow_redirects=True)
    assert "Tarea eliminada" in response.get_data(as_text=True)
    assert "Primera tarea" not in client.get("/tareas/", follow_redirects=True).get_data(as_text=True)
