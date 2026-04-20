<?php
function procesarDiscos($texto)
{
    if (!$texto) return [];

    $discos = json_decode($texto, true);

    if (!is_array($discos)) return [];

    return $discos;
}