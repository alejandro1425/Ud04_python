# Lembradoiro (TO-DO Flask)

Aplicación web de tareas pendientes desarrollada con Flask y SQLite. Incluye
registro e inicio de sesión de usuarios, tablero de tareas con marcado de
completadas y pruebas unitarias automatizadas.

## Características
- ✅ Autenticación: registro, login y cierre de sesión.
- ✅ Gestión de tareas: crear, editar, marcar como completada/pendiente y borrar.
- ✅ Interfaz responsive en castellano con estilo personalizado.
- ✅ Base de datos SQLite con comando `flask init-db` para inicializarla.
- ✅ Conjunto de pruebas con `pytest`.

## Requisitos
- Python 3.11+
- Pip y entorno virtual recomendado.

Instala dependencias con:

```bash
pip install -r requirements.txt
```

## Puesta en marcha local
1. Crea el entorno: `python -m venv .venv && source .venv/bin/activate`.
2. Instala dependencias.
3. Inicializa la base de datos:
   ```bash
   flask --app todoapp init-db
   ```
4. Ejecuta la aplicación en modo desarrollo:
   ```bash
   flask --app todoapp --debug run
   ```
5. Accede en <http://localhost:5000>.

## Ejecutar pruebas
```bash
pytest
```

## Despliegue
Puedes desplegar en cualquier proveedor que soporte Python/Flask (Heroku,
Railway, Render, PythonAnywhere). Asegúrate de establecer la variable
`SECRET_KEY` y la ruta `DATABASE` si no usas SQLite en `instance/`.

## Estructura principal
- `todoapp/__init__.py`: fábrica de la aplicación y registro de *blueprints*.
- `todoapp/auth.py`: rutas de autenticación.
- `todoapp/tasks.py`: lógica de tareas.
- `todoapp/db.py` y `todoapp/schema.sql`: conexión y esquema de base de datos.
- `todoapp/templates/` y `todoapp/static/`: interfaz HTML/CSS responsive.
- `tests/`: fixtures y pruebas automáticas.
