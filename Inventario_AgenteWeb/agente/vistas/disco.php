<?php
function renderizarDiscos($discos)
{
    if (empty($discos)) {
        return "<p>Sin información de discos</p>";
    }

    $html = "<h3>Discos Físicos</h3>";
    $html .= "<table class='tabla-discos'>";

    $html .= "<tr>
        <th>Modelo</th>
        <th>Capacidad</th>
        <th>Espacio Libre</th>
        <th>Tipo</th>
        <th>Salud</th>
        <th>Temperatura</th>
        <th>Horas</th>
        <th>Errores</th>
    </tr>";

    foreach ($discos as $d) {

        $modelo = htmlspecialchars($d["modelo"] ?? "Desconocido");
        $capacidad = htmlspecialchars($d["capacidad"] ?? "N/A");
        $espacio_libre = htmlspecialchars($d["espacio_libre_gb"] ?? "N/A");
        $tipo = htmlspecialchars($d["tipo"] ?? "N/A");
        $salud = htmlspecialchars($d["salud"] ?? "N/A");
        $temp = $d["temperatura"] ?? null;

        $temperatura = ($temp !== null && $temp !== "") 
            ? htmlspecialchars($temp) . " °C" 
            : "N/A";

        $horas = htmlspecialchars($d["horas"] ?? "N/A");
        $errores = htmlspecialchars($d["errores"] ?? "0");

        $html .= "<tr>
            <td>$modelo</td>
            <td>$capacidad</td>
            <td>$espacio_libre GB</td>
            <td>$tipo</td>
            <td>$salud</td>
            <td>$temperatura</td>
            <td>$horas</td>
            <td>$errores</td>
        </tr>";
    }

    $html .= "</table>";

    return $html;
}