<?php

// =============================
// 🔌 CONEXIÓN A LA BASE DE DATOS
// =============================
require_once __DIR__ . "/../config/conexion.php";

// Indicamos que la respuesta será JSON
header('Content-Type: application/json');

// =============================
// 📥 RECIBIR DATOS DESDE JS (fetch)
// =============================
$data = json_decode(file_get_contents("php://input"), true);

// =============================
// 📌 OBTENER VARIABLES
// =============================
$id = $data["id"] ?? null;

$codigo = trim($data["codigo_inventario"] ?? "");
$departamento = strtoupper(trim($data["departamento"] ?? ""));
$perifericos = $data["perifericos"] ?? []; // 🔥 NUEVO

// =============================
// 🚫 VALIDACIONES
// =============================

// Validar ID
if (!$id) {
    echo json_encode([
        "success" => false,
        "message" => "ID requerido"
    ]);
    exit;
}

// Validar que haya al menos un dato
if ($codigo === "" && $departamento === "") {
    echo json_encode([
        "success" => false,
        "message" => "No hay datos para actualizar"
    ]);
    exit;
}

// Validar código inventario
$regex = '/^\d{2}-\d{2}-\d{2}-\d{3}-\d{5}$/';

if ($codigo === "") {
    // Pendiente → OK
}
elseif (strtolower($codigo) === "sin") {
    $codigo = "SIN";
}
elseif (preg_match($regex, $codigo)) {
    // OK
}
else {
    echo json_encode([
        "success" => false,
        "field" => "codigo",
        "message" => "Formato inválido. Usa: 12-34-56-789-12345 o escribe 'SIN'"
    ]);
    exit;
}

// Validar departamento
if ($departamento !== "" && strlen($departamento) < 3) {
    echo json_encode([
        "success" => false,
        "field" => "departamento",
        "message" => "El departamento debe tener al menos 3 caracteres"
    ]);
    exit;
}

// =============================
// 🛠️ ARMAR UPDATE DINÁMICO
// =============================

$sql = "UPDATE equipos SET ";
$params = [];
$types = "";

// Código
if ($codigo !== "") {
    $sql .= "codigo_inventario = ?, ";
    $params[] = $codigo;
    $types .= "s";
}

// Departamento
if ($departamento !== "") {
    $sql .= "departamento = ?, ";
    $params[] = $departamento;
    $types .= "s";
}

// 🔥 PERIFERICOS
if (is_array($perifericos)) {

    if (count($perifericos) > 0) {
        $perifericos_json = json_encode($perifericos, JSON_UNESCAPED_UNICODE);

        $sql .= "perifericos = ?, ";
        $params[] = $perifericos_json;
        $types .= "s";
    } else {
        // Si viene vacío → guardar NULL
        $sql .= "perifericos = NULL, ";
    }
}

// Quitar última coma
$sql = rtrim($sql, ", ");

// Condición final
$sql .= " WHERE id = ?";
$params[] = $id;
$types .= "i";

// =============================
// 💾 PREPARAR Y EJECUTAR
// =============================

$stmt = $conn->prepare($sql);

if (!$stmt) {
    echo json_encode([
        "success" => false,
        "message" => "Error en servidor (prepare): " . $conn->error
    ]);
    exit;
}

// bind dinámico
$stmt->bind_param($types, ...$params);

// ejecutar
if ($stmt->execute()) {
    echo json_encode([
        "success" => true,
        "message" => "Datos actualizados correctamente"
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "Error al actualizar: " . $stmt->error
    ]);
}

// cerrar conexión
$conn->close();