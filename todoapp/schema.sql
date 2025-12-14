-- Esquema de la base de datos para la aplicación de tareas.
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS tarea;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tarea (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    completada INTEGER NOT NULL DEFAULT 0,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    autor_id INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES usuario (id)
);
