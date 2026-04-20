<?php
session_start();
header('Content-Type: application/json');

require_once __DIR__ . "/../config/conexion.php";

$data = json_decode(file_get_contents("php://input"), true);

$usuario = $data["usuario"] ?? "";
$password = $data["password"] ?? "";

if (empty($usuario) || empty($password)) {
    echo json_encode([
        "success" => false,
        "message" => "Campos obligatorios"
    ]);
    exit;
}

$sql = "SELECT * FROM usuarios WHERE usuario = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $usuario);
$stmt->execute();

$result = $stmt->get_result();

if ($result->num_rows === 1) {

    $user = $result->fetch_assoc();

    if (password_verify($password, $user["password"])) {

        $_SESSION["usuario"] = $user["usuario"];

        echo json_encode([
            "success" => true
        ]);

    } else {
        echo json_encode([
            "success" => false,
            "message" => "Contraseña incorrecta"
        ]);
    }

} else {
    echo json_encode([
        "success" => false,
        "message" => "Usuario no existe"
    ]);
}