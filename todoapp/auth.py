"""Blueprint de autenticación: registro, inicio y cierre de sesión."""
from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar, cast

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/registro", methods=("GET", "POST"))
def register() -> str | Any:
    """Permite crear un nuevo usuario.

    Valida que el nombre de usuario no exista y guarda la contraseña cifrada
    usando :func:`werkzeug.security.generate_password_hash`.
    """

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        db = get_db()
        error = None

        if not username:
            error = "Debes indicar un nombre de usuario."
        elif not password:
            error = "La contraseña no puede estar vacía."
        elif db.execute("SELECT id FROM usuario WHERE username = ?", (username,)).fetchone():
            error = "El usuario ya existe."  # No revelar demasiada información.

        if error is None:
            db.execute(
                "INSERT INTO usuario (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash("Registro exitoso. Ya puedes iniciar sesión.")
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> str | Any:
    """Inicia sesión verificando credenciales y almacenando el id del usuario en sesión."""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        db = get_db()
        error = None

        user = db.execute("SELECT * FROM usuario WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = "Nombre de usuario incorrecto."
        elif not check_password_hash(user["password"], password):
            error = "Contraseña incorrecta."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            flash("Sesión iniciada. ¡Bienvenido de nuevo!")
            return redirect(url_for("tasks.dashboard"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user() -> None:
    """Carga el usuario actual antes de manejar cada petición."""

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM usuario WHERE id = ?", (user_id,)).fetchone()


@bp.route("/logout")
def logout() -> Any:
    """Cierra la sesión actual y redirige a la página de inicio."""

    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("auth.login"))


F = TypeVar("F", bound=Callable[..., Any])


def login_required(view: F) -> F:
    """Decorador que exige autenticación para acceder a una vista."""

    @functools.wraps(view)
    def wrapped_view(**kwargs: Any) -> Any:
        if g.get("user") is None:
            flash("Para continuar inicia sesión.")
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return cast(F, wrapped_view)
