<?php

require_once __DIR__ . "/../config/conexion.php";
require_once __DIR__ . "/../agente/logica/perifericos.php";
require_once __DIR__ . "/../agente/vistas/perifericos.php";

$sql = "SELECT id, usuario, departamento, perifericos FROM equipos";
$result = $conn->query($sql);

$perifericosFinal = [];

if ($result && $result->num_rows > 0) {

    while ($row = $result->fetch_assoc()) {

        $lista = procesarPerifericos(
            $row["perifericos"],
            $row["id"],
            $row["usuario"],
            $row["departamento"]
        );

        $perifericosFinal = array_merge($perifericosFinal, $lista);
    }
}

// 🔥 AQUÍ SE USA TU VISTA
echo renderizarPerifericos($perifericosFinal);