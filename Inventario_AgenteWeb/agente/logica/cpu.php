<?php

function formatearCPU($cpu)
{
    $cpu = explode(",", $cpu)[0];
    $cpu = str_replace("(R)", "", $cpu);
    $cpu = str_replace("(TM)", "", $cpu);
    $cpu = str_replace("CPU", "", $cpu);
    $cpu = str_replace("with Radeon Graphics", "", $cpu);
    $cpu = str_replace("APU with Radeon HD Graphics", "", $cpu);
    $cpu = preg_replace('/\s+/', ' ', $cpu);
    return trim($cpu);
}