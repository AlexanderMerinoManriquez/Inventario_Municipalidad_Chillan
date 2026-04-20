<?php 

// 🔥 OCULTAR ERRORES
error_reporting(0);
ini_set('display_errors', 0);

// =============================
// 🔌 CONEXIÓN
// =============================
require_once __DIR__ . "/../config/conexion.php";

header('Content-Type: application/json');

// =============================
// ❌ ERROR DE CONEXIÓN
// =============================
if ($conn->connect_error) {
    echo json_encode([
        "success" => false,
        "message" => "Error de conexión"
    ]);
    exit;
}

// =============================
// 📥 FILTRO OPCIONAL
// =============================
$equipoFiltro = $_GET["equipo_id"] ?? null;

// =============================
// 📥 CONSULTA
// =============================
$sql = "SELECT id, usuario, departamento, perifericos FROM equipos";
$result = $conn->query($sql);

$perifericosFinal = [];

// =============================
// 🔄 RECORRER RESULTADOS
// =============================
if ($result && $result->num_rows > 0) {

    while ($row = $result->fetch_assoc()) {

        $equipo_id = $row["id"];

        // 🔥 FILTRO POR EQUIPO
        if ($equipoFiltro && $equipoFiltro != $equipo_id) {
            continue;
        }

        $usuario = $row["usuario"];
        $departamento = $row["departamento"];
        $json = $row["perifericos"];

        if (!$json || trim($json) === "") {
            continue;
        }

        $lista = json_decode($json, true);

        if (!is_array($lista)) {
            continue;
        }

        $contador = 1;

        foreach ($lista as $p) {

            $perifericosFinal[] = [
                "equipo_id" => $equipo_id,
                "id_periferico" => $contador,

                "usuario" => $usuario,
                "departamento" => $departamento,

                "tipo" => $p["tipo"] ?? "",
                "marca" => $p["marca"] ?? "",
                "modelo" => $p["modelo"] ?? "",
                "toner" => $p["toner"] ?? "",
                "ip" => $p["ip"] ?? "",
                "ci" => $p["ci"] ?? "",
                "sn" => $p["sn"] ?? ""
            ];

            $contador++;
        }
    }
}

// =============================
// 📤 RESPUESTA
// =============================
echo json_encode($perifericosFinal, JSON_UNESCAPED_UNICODE);

$conn->close();