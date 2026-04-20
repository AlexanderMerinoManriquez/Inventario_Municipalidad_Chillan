<?php

function procesarPerifericos($json)
{
    if (!$json || trim($json) === "") {
        return [];
    }

    $lista = json_decode($json, true);

    if (!is_array($lista)) {
        return [];
    }

    $resultado = [];
    $contador = 1; // 

    foreach ($lista as $p) {

        $resultado[] = [
            "id_periferico" => $contador, //
            "tipo" => $p["tipo"] ?? null,
            "marca" => $p["marca"] ?? null,
            "modelo" => $p["modelo"] ?? null,
            "toner" => $p["toner"] ?? null,
            "ip" => $p["ip"] ?? null,
            "ci" => $p["ci"] ?? null,
            "sn" => $p["sn"] ?? null
        ];

        $contador++; // 
    }

    return $resultado;
}