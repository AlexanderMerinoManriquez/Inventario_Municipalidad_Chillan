<?php

require_once __DIR__ . "/../config/conexion.php";

header('Content-Type: application/json');

$data = json_decode(file_get_contents("php://input"), true);


function esInyeccion($valor) {
    return preg_match('/<[^>]+>|<!\[CDATA\[|\?>|<\?xml/i', $valor);
}

function esNombreHardwareValido($valor) {
    return preg_match('/^[\p{L}\p{N}\s\-\_\.\(\)\/]+$/u', $valor);
}

function esTextoValido($valor) {
    return preg_match('/^[\p{L}\p{N}\s\-\_\.\(\)\/\@\:\,]+$/u', $valor);
}
function error($msg, $code = "GENERAL") {
    echo json_encode([
        "success" => false,
        "message" => $msg,
        "code" => $code
    ]);
    exit;
}

function esTamanoValido($valor) {
    $valor = trim($valor);
    return preg_match('/^\d+(\.\d+)?\s*(GB|MB|TB)$/i', $valor);
}



$id = $data["id"] ?? null;

$nombre_pc = $data["nombre_pc"] ?? "";
$usuario = $data["usuario"] ?? "";
$departamento = strtoupper(trim($data["departamento"] ?? ""));
$sistema = $data["sistema_operativo"] ?? "";
$anydesk = $data["anydesk"] ?? "";
$cpu = $data["cpu"] ?? "";
$ram = $data["ram"] ?? "";
$disco = $data["disco_total"] ?? "";
$ip = $data["ip"] ?? "";
$uuid = trim($data["uuid"] ?? "");
$serial = $data["serial"] ?? "";

$ubicacion = $data["ubicacion"] ?? "";
$departamento_manual = $data["departamento_manual"] ?? "";

$marca_pantalla = $data["marca_pantalla"] ?? "";
$modelo_pantalla = $data["modelo_pantalla"] ?? "";
$pulgadas_pantalla = $data["pulgadas_pantalla"] ?? "";

$tipo_impresora = $data["tipo_impresora"] ?? "";
$marca_impresora = $data["marca_impresora"] ?? "";
$modelo_impresora = $data["modelo_impresora"] ?? "";
$toner_tinta = $data ["toner_tinta"] ?? "";
$ip_impresora = $data ["ip_impresora"] ?? "";

$observaciones = $data["observaciones"] ??"";
$codigo = $data["codigo_inventario"] ?? null;

// =============================
// VALIDACIONES (RECHAZA DATOS)
// =============================

$camposTexto = [
    "nombre_pc" => $nombre_pc,
    "usuario" => $usuario,
    "departamento" => $departamento,
    "sistema_operativo" => $sistema,
    "anydesk" => $anydesk,
    "ubicacion" => $ubicacion,
    "departamento_manual" => $departamento_manual,
    "observaciones" => $observaciones,
    "codigo_inventario" => $codigo
];

foreach ($camposTexto as $campo => $valor) {

    if (!empty($valor) && esInyeccion($valor)) {
        error("⚠️ Intento de inyección detectado en $campo");
    }

    if (!empty($valor) && !esTextoValido($valor)) {
        error("Dato inválido en $campo");
    }
}

if (!empty($cpu) && esInyeccion($cpu)) {
    error(" Intento de inyección detectado en cpu");
}

// IP válida
if (!empty($ip) && !filter_var($ip, FILTER_VALIDATE_IP)) {
    error("IP inválida");
}

// RAM
if (!empty($ram) && !esTamanoValido($ram)) {
    error("RAM inválida");
}

// Disco numéricos
if (!empty($disco) && !esTamanoValido($disco)) {
    error("Disco inválido");
}

// UUID
if (!empty($uuid) && $uuid !== "UUID_DESCONOCIDO" && !preg_match('/^[a-zA-Z0-9\-]+$/', $uuid)) {
    error("UUID inválido");
}

// SERIAL
if (!empty($serial) && !preg_match('/^[a-zA-Z0-9\-]+$/', $serial)) {
    error("Serial inválido");
}



$discos = [];

if (isset($data["discos"])) {

    if (!is_array($data["discos"])) {
        error("Formato de discos inválido");
    }

        foreach ($data["discos"] as $d) {

            if (esInyeccion($d["modelo"] ?? "")) {
                error("⚠️ Intento de inyección detectado en modelo de disco");
            }

            if (!esNombreHardwareValido($d["modelo"] ?? "")) {
                error("Nombre de disco inválido");
            }

            if (!esTamanoValido($d["capacidad"] ?? "")) {
                error("Tamaño de disco inválido");
            }

            $discos[] = [
                "modelo" => $d["modelo"],
                "capacidad" => $d["capacidad"],
                "espacio_libre_gb" => $d["espacio_libre_gb"] ?? null,
                "tipo" => $d["tipo"] ?? null,
                "salud" => $d["salud"] ?? null,
                "horas" => $d["horas"] ?? null,
                "errores" => $d["errores"] ?? null,
                "temperatura" => $d["temperatura"] ?? null
            ];
        }
}

$discos = json_encode($discos);


if ($departamento === "") {
    $departamento = "SIN_DEFINIR";
}

// =============================
// UPDATE POR ID
// =============================
               
if (!empty($id)) {

    $sql_update = "UPDATE equipos SET
        codigo_inventario=?,
        nombre_pc=?,
        usuario=?,
        departamento=?,
        sistema_operativo=?,
        anydesk=?,
        cpu=?,
        ram=?,
        disco_total=?,
        ip=?,

        ubicacion=?,
        departamento_manual=?,

        marca_pantalla=?,
        modelo_pantalla=?,
        pulgadas_pantalla=?,

        tipo_impresora=?,
        marca_impresora=?,
        modelo_impresora=?,
        toner_tinta=?,
        ip_impresora=?,

        observaciones=?,
        ultimo_inventario = NOW()";

    $params = [
        $codigo,
        $nombre_pc,
        $usuario,
        $departamento,
        $sistema,
        $anydesk,
        $cpu,
        $ram,
        $disco,
        $ip,

        $ubicacion,
        $departamento_manual,

        $marca_pantalla,
        $modelo_pantalla,
        $pulgadas_pantalla,

        $tipo_impresora,
        $marca_impresora,
        $modelo_impresora,
        $toner_tinta,
        $ip_impresora,

        $observaciones
    ];

    $types = "sssssssssssssssssssss";

    if (!empty($uuid)) {
        $sql_update .= ", uuid=?";
        $params[] = $uuid;
        $types .= "s";
    }

    if (!empty($serial)) {
        $sql_update .= ", serial=?";
        $params[] = $serial;
        $types .= "s";
    }

    if (!empty($discos) && $discos !== "[]") {
        $sql_update .= ", discos=?";
        $params[] = $discos;
        $types .= "s";
    }

    $sql_update .= " WHERE id=?";
    $params[] = $id;
    $types .= "i";

    $stmt = $conn->prepare($sql_update);
    $stmt->bind_param($types, ...$params);

    if ($stmt->execute()) {
        echo json_encode([
            "success" => true,
            "message" => "Equipo actualizado"
        ]);
    } else {
        error("Error actualizando");
    }

    $conn->close();
    exit;
}


$sql = "SELECT id FROM equipos WHERE uuid = ? AND serial = ? LIMIT 1";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $uuid, $serial);
$stmt->execute();
$resultado = $stmt->get_result();

// =============================
// SI EXISTE → UPDATE
// =============================
if ($resultado->num_rows > 0) {

    $row = $resultado->fetch_assoc();
    $id = $row["id"];
//
    $sql_update = "UPDATE equipos SET
        codigo_inventario=?,
        nombre_pc=?,
        usuario=?,
        departamento=?,
        sistema_operativo=?,
        anydesk=?,
        cpu=?,
        ram=?,
        disco_total=?,
        discos=?,
        ip=?,
        uuid=?,
        serial=?,

        ubicacion=?,
        departamento_manual=?,

        marca_pantalla=?,
        modelo_pantalla=?,
        pulgadas_pantalla=?,

        tipo_impresora=?,
        marca_impresora=?,
        modelo_impresora=?,
        toner_tinta=?,
        ip_impresora=?,

        observaciones=?,
        ultimo_inventario = NOW()
        WHERE id=?";

    $stmt = $conn->prepare($sql_update);

    $stmt->bind_param(
        "ssssssssssssssssssssssssi",
        $codigo,
        $nombre_pc,
        $usuario,
        $departamento,
        $sistema,
        $anydesk,
        $cpu,
        $ram,
        $disco,
        $discos,
        $ip,
        $uuid,
        $serial,

        $ubicacion,
        $departamento_manual,

        $marca_pantalla,
        $modelo_pantalla,
        $pulgadas_pantalla,

        $tipo_impresora,
        $marca_impresora,
        $modelo_impresora,
        $toner_tinta,
        $ip_impresora,

       $observaciones,
        $id
    );

    if ($stmt->execute()) {
        echo json_encode([
            "success" => true,
            "message" => "Equipo actualizado"
        ]);
    } else {
        error("Error actualizando");
    }

}


else {
            
    $sql_insert = "INSERT INTO equipos
    (codigo_inventario, nombre_pc, usuario, departamento, sistema_operativo, anydesk, cpu, ram, disco_total, discos, ip, uuid, serial, ubicacion, departamento_manual, marca_pantalla, modelo_pantalla, pulgadas_pantalla, tipo_impresora, marca_impresora, modelo_impresora, toner_tinta, ip_impresora, observaciones, ultimo_inventario)
    VALUES
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, NOW())";

    $stmt = $conn->prepare($sql_insert);

    $stmt->bind_param(
        "ssssssssssssssssssssssss",
        $codigo,
        $nombre_pc,
        $usuario,
        $departamento,
        $sistema,
        $anydesk,
        $cpu,
        $ram,
        $disco,
        $discos,
        $ip,
        $uuid,
        $serial,

        $ubicacion,
        $departamento_manual,

        $marca_pantalla,
        $modelo_pantalla,
        $pulgadas_pantalla,

        $tipo_impresora,
        $marca_impresora,
        $modelo_impresora,
        $toner_tinta,
        $ip_impresora,

        $observaciones
    );

    if ($stmt->execute()) {
        echo json_encode([
            "success" => true,
            "message" => "Equipo registrado"
        ]);
    } else {
        error("Error insertando");
    }
}

$conn->close();

?>

