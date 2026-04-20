<?php

define("DB_HOST", "localhost");
define("DB_USER", "root");
define("DB_PASS", "");
define("DB_NAME", "inventario_pc");

/* ==========================
   CONEXION MYSQL
   ========================== */

$conn = new mysqli(DB_HOST, DB_USER, DB_PASS);

if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

/* ==========================
   CREAR BASE DE DATOS
   ========================== */

$sql_db = "CREATE DATABASE IF NOT EXISTS " . DB_NAME . "
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci";

if (!$conn->query($sql_db)) {
    die("Error creando base de datos: " . $conn->error);
}

/* ==========================
   SELECCIONAR BASE
   ========================== */

$conn->select_db(DB_NAME);

/* ==========================
   CREAR TABLA EQUIPOS
   ========================== */

$sql_equipos = "
CREATE TABLE IF NOT EXISTS equipos (
  id INT NOT NULL AUTO_INCREMENT,
  nombre_pc VARCHAR(30) DEFAULT NULL,
  usuario VARCHAR(50) DEFAULT NULL,
  departamento VARCHAR(30) DEFAULT NULL,
  sistema_operativo VARCHAR(30) DEFAULT NULL,
  anydesk VARCHAR(20) DEFAULT NULL,
  cpu VARCHAR(100) DEFAULT NULL,
  ram VARCHAR(10) DEFAULT NULL,
  disco_total VARCHAR(10) DEFAULT NULL,
  ip VARCHAR(15) DEFAULT NULL,
  uuid VARCHAR(50) DEFAULT NULL,
  serial VARCHAR(50) DEFAULT NULL,
  discos TEXT,
  ultimo_inventario DATETIME DEFAULT NULL,
  codigo_inventario VARCHAR(20) DEFAULT NULL,
  perifericos TEXT,

  PRIMARY KEY (id),
  UNIQUE KEY unique_uuid (uuid),
  UNIQUE KEY unique_serial (serial)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
";

if (!$conn->query($sql_equipos)) {
    die("Error creando tabla equipos: " . $conn->error);
}

/* ==========================
   CREAR TABLA USUARIOS
   ========================== */

$sql_usuarios = "
CREATE TABLE IF NOT EXISTS usuarios (
  id INT NOT NULL AUTO_INCREMENT,
  usuario VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY unique_usuario (usuario)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
";

if (!$conn->query($sql_usuarios)) {
    die("Error creando tabla usuarios: " . $conn->error);
}

/* ==========================
   CREAR USUARIO ADMIN AUTOMATICO
   ========================== */

$result = $conn->query("SELECT id FROM usuarios WHERE usuario = 'admin' LIMIT 1");

if (!$result) {
    die("Error verificando usuario admin: " . $conn->error);
}

if ($result->num_rows === 0) {

    $usuario = "admin";
    $password = password_hash("1234", PASSWORD_DEFAULT);

    $stmt = $conn->prepare("INSERT INTO usuarios (usuario, password) VALUES (?, ?)");
    
    if (!$stmt) {
        die("Error en prepare: " . $conn->error);
    }

    $stmt->bind_param("ss", $usuario, $password);
    
    if (!$stmt->execute()) {
        die("Error insertando admin: " . $stmt->error);
    }

}

?>