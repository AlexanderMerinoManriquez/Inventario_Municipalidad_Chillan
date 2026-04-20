<?php
/* Desactivar errores de php a usuario */
ini_set('display_errors', 0);
error_reporting(0);
/* Verifica la secion iniciada e importa la conexion a la BDD */
session_start();
require_once __DIR__ . "/../config/conexion.php";
/* Indica que toda respuesta estara en formato JSON */
header('Content-Type: application/json');
/* Lee el contenido previo en formato JSON */
$data = json_decode(file_get_contents("php://input"), true);
/* Recibir los datos y "trim()" evita los espacios indeseados */
$usuario = trim($data["usuario"] ?? "");
$password = trim($data["password"] ?? "");
// Verificar que los input no esten vacios
if (empty($usuario) || empty($password)) {
    echo json_encode([
        "success" => false,
        "message" => "Campos obligatorios"
    ]);
    exit;
}
// Contraseña arriba de 4 digitos
if (strlen($password) < 4) {
    echo json_encode([
        "success" => false,
        "message" => "La contraseña es muy corta"
    ]);
    exit;
}
// Formato hash a contraseña
$password_hash = password_hash($password, PASSWORD_DEFAULT);
// Insertar usuario en la BDD
$sql = "INSERT INTO usuarios (usuario, password) VALUES (?, ?)";
// Preparar formato a el parametro de usuario y hashear contraseña
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $usuario, $password_hash);
// Tramo correcto en el caso de insercion correcta
if ($stmt->execute()) {
    echo json_encode([
        "success" => true,
        "message" => "Usuario creado correctamente"
    ]);
// Tramo alternativo en el caso de que la insercion sea incorrecta
} else {
    // Capturar error de usuario duplicado
    if ($stmt->errno === 1062) {
        echo json_encode([
            "success" => false,
            "message" => "El usuario ya existe"
        ]);
    } 
    // Captura el error y responder con el codigo de error
    else {
        echo json_encode([
            "success" => false,
            "message" => "Error SQL " . $stmt->errno,
            "detalle" => $stmt->error
        ]);
    }

}