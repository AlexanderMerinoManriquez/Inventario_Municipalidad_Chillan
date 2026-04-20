<?php
function obtenerDiscosPorEquipo($id_equipo)
{
    global $conn;

    $sql = "SELECT discos FROM equipos WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $id_equipo);
    $stmt->execute();

    $resultado = $stmt->get_result()->fetch_assoc();
    $stmt->close();

    return $resultado["discos"] ?? null;
}