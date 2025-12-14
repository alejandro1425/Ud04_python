-- Contraseña en texto plano: "test" (generada con werkzeug.security.generate_password_hash)
INSERT INTO usuario (username, password) VALUES ('usuario', 'scrypt:32768:8:1$MMdMj7CfCsuRiOsy$ac8422c683df7e721941670850b95fa0885842d41ccef2ea8cbfa00d6d2a8485e19262a21c470c6e8aa3bc7f0054ea93f7961e0feaa28793ac988d6d248c2167');
INSERT INTO tarea (titulo, descripcion, autor_id) VALUES ('Primera tarea', 'Descripción inicial', 1);
