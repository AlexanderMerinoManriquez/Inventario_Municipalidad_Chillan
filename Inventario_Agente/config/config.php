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
   SELECCIONAR BASE
   ========================== */

$conn->select_db(DB_NAME);

?>