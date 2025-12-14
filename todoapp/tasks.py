"""Blueprint principal para gestionar tareas pendientes."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db

bp = Blueprint("tasks", __name__, url_prefix="/tareas")


@bp.route("/")
@login_required
def dashboard() -> str:
    """Muestra el tablero con las tareas del usuario autenticado."""

    db = get_db()
    tasks = db.execute(
        """
        SELECT t.id, t.titulo, t.descripcion, t.completada, t.creado
        FROM tarea t
        WHERE t.autor_id = ?
        ORDER BY t.completada ASC, t.creado DESC
        """,
        (g.user["id"],),
    ).fetchall()
    return render_template("tasks/dashboard.html", tasks=tasks)


@bp.route("/crear", methods=("GET", "POST"))
@login_required
def create() -> str | Any:
    """Crea una nueva tarea asociada al usuario actual."""

    if request.method == "POST":
        title = request.form["titulo"].strip()
        description = request.form.get("descripcion", "").strip()
        error = None

        if not title:
            error = "El título es obligatorio."

        if error is None:
            db = get_db()
            db.execute(
                "INSERT INTO tarea (titulo, descripcion, autor_id) VALUES (?, ?, ?)",
                (title, description, g.user["id"]),
            )
            db.commit()
            flash("Tarea creada correctamente.")
            return redirect(url_for("tasks.dashboard"))

        flash(error)

    return render_template("tasks/create.html")


def get_task(task_id: int, check_author: bool = True) -> Any:
    """Recupera una tarea y verifica que pertenece al usuario.

    Args:
        task_id: Identificador de la tarea.
        check_author: Si es ``True``, asegura que la tarea pertenece al usuario
            logueado, lanzando un error en caso contrario.
    """

    task = get_db().execute(
        "SELECT * FROM tarea WHERE id = ?",
        (task_id,),
    ).fetchone()

    if task is None:
        raise ValueError("La tarea solicitada no existe.")

    if check_author and task["autor_id"] != g.user["id"]:
        raise PermissionError("No puedes modificar tareas de otra persona.")

    return task


@bp.route("/<int:id>/editar", methods=("GET", "POST"))
@login_required
def update(id: int) -> str | Any:
    """Actualiza el título o la descripción de una tarea."""

    task = get_task(id)

    if request.method == "POST":
        title = request.form["titulo"].strip()
        description = request.form.get("descripcion", "").strip()
        error = None

        if not title:
            error = "El título es obligatorio."

        if error is None:
            db = get_db()
            db.execute(
                "UPDATE tarea SET titulo = ?, descripcion = ? WHERE id = ?",
                (title, description, id),
            )
            db.commit()
            flash("Tarea actualizada.")
            return redirect(url_for("tasks.dashboard"))

        flash(error)

    return render_template("tasks/update.html", task=task)


@bp.route("/<int:id>/completar", methods=("POST",))
@login_required
def toggle_complete(id: int) -> Any:
    """Alterna el estado de completada de una tarea."""

    task = get_task(id)
    nuevo_estado = 0 if task["completada"] else 1
    db = get_db()
    db.execute("UPDATE tarea SET completada = ? WHERE id = ?", (nuevo_estado, id))
    db.commit()
    mensaje = "Tarea marcada como completada." if nuevo_estado else "Tarea marcada como pendiente."
    flash(mensaje)
    return redirect(url_for("tasks.dashboard"))


@bp.route("/<int:id>/borrar", methods=("POST",))
@login_required
def delete(id: int) -> Any:
    """Elimina una tarea existente."""

    get_task(id)  # Comprueba propiedad y existencia.
    db = get_db()
    db.execute("DELETE FROM tarea WHERE id = ?", (id,))
    db.commit()
    flash("Tarea eliminada.")
    return redirect(url_for("tasks.dashboard"))


@bp.app_template_filter("humanize_date")
def humanize_date(value: str | datetime) -> str:
    """Convierte fechas en textos amigables.

    Args:
        value: Cadena de fecha o instancia de :class:`datetime.datetime`.
    """

    if isinstance(value, str):
        try:
            date_value = datetime.fromisoformat(value)
        except ValueError:
            return value
    else:
        date_value = value
    return date_value.strftime("%d/%m/%Y %H:%M")
