CREATE TABLE empleados (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  dni      TEXT UNIQUE NOT NULL,
  nombre   TEXT
);

CREATE TABLE retiros (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  empleado_id  INTEGER NOT NULL REFERENCES empleados(id),
  fecha        DATE    NOT NULL,
  importe      REAL    NOT NULL
);
CREATE UNIQUE INDEX unq_retiro_dia ON retiros(empleado_id, fecha);