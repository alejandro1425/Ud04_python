"""Pruebas relacionadas con el flujo de autenticación."""
from __future__ import annotations

import pytest
from werkzeug.security import check_password_hash

from todoapp.db import get_db


def test_register(client, app):
    """Un usuario puede registrarse y se almacena en la base de datos."""

    response = client.post("/auth/registro", data={"username": "nuevo", "password": "clave"})
    assert response.status_code == 302  # redirección a login

    with app.app_context():
        user = get_db().execute("SELECT * FROM usuario WHERE username = ?", ("nuevo",)).fetchone()
        assert user is not None
        assert check_password_hash(user["password"], "clave")


def test_register_input_validation(client):
    """El registro muestra mensajes de error cuando falta algún dato."""

    response = client.post("/auth/registro", data={"username": "", "password": ""}, follow_redirects=True)
    assert b"Debes indicar" in response.data


def test_login_logout_cycle(client):
    """El usuario puede iniciar y cerrar sesión correctamente."""

    login_response = client.post(
        "/auth/login", data={"username": "usuario", "password": "test"}, follow_redirects=True
    )
    assert b"Sesión iniciada" in login_response.data

    logout_response = client.get("/auth/logout", follow_redirects=True)
    assert b"Sesión cerrada" in logout_response.data


def test_login_invalid_credentials(client):
    """Credenciales incorrectas muestran el mensaje adecuado."""

    response = client.post(
        "/auth/login", data={"username": "usuario", "password": "mal"}, follow_redirects=True
    )
    assert b"Contraseña incorrecta" in response.data
