<?php
session_start();

if (!isset($_SESSION["usuario"])) {
    header("Location: /Inventario_AgenteWeb/panel/login.php");
    exit;
}
?>

<?php
require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/../config/conexion.php';
require_once __DIR__ . '/../agente/database/disco.php';
require_once __DIR__ . '/../agente/logica/disco.php';
require_once __DIR__ . '/../agente/vistas/disco.php';
require_once __DIR__ . '/../agente/logica/perifericos.php';
require_once __DIR__ . '/../agente/vistas/perifericos.php';
require_once __DIR__ . '/../agente/logica/cpu.php';

use Dompdf\Dompdf;

$id = intval($_GET['id'] ?? 0);

if (!$id) {
    die("Equipo no especificado");
}

// ==============================
// CONSULTA INFO GENERAL
// ==============================
$sql = "SELECT * FROM equipos WHERE id = $id";
$result = $conn->query($sql);
$row = $result->fetch_assoc();

if (!$row) {
    die("Equipo no encontrado");
}

// ==============================
// 🔥 OBTENER PERIFÉRICOS
// ==============================
$perifericosProcesados = procesarPerifericos($row["perifericos"] ?? "");
$tablaPerifericos = renderizarPerifericos($perifericosProcesados);

// ==============================
// OBTENER Y PROCESAR DISCOS
// ==============================
$textoDiscos = obtenerDiscosPorEquipo($id);
$discos = procesarDiscos($textoDiscos);
$tablaDiscos = renderizarDiscos($discos);

// ==============================
// TABLA PRINCIPAL
// ==============================
$tabla = '<table class="tabla-info">';

$etiquetas = [
    "codigo_inventario" => "Código de Inventario",
    "anydesk" => "Anydesk",
    "nombre_pc" => "Nombre del PC",
    "usuario" => "Usuario",
    "departamento" => "Departamento",
    "sistema_operativo" => "Sistema Operativo",
    "cpu" => "CPU",
    "ram" => "Memoria RAM",
    "disco_total" => "Disco Principal",
    "ip" => "Dirección IP",
    "ultimo_inventario" => "Último Inventario",
    "serial" => "Serial",
    "uuid" => "UUID"
];

foreach ($etiquetas as $campo => $nombreCampo) {

    $valor = $row[$campo] ?? "";

    if ($campo == "cpu") {
        $valor = formatearCPU($valor);
    }

    if ($campo == "disco_total") {
        $valor = htmlspecialchars($valor);
    }

    $tabla .= '<tr>';
    $tabla .= '<td class="etiqueta">' . htmlspecialchars($nombreCampo) . '</td>';
    $tabla .= '<td>' . htmlspecialchars($valor) . '</td>';
    $tabla .= '</tr>';
}

$tabla .= '</table>';

// ==============================
// ESTILOS
// ==============================
$estilos = '
<style>
body{
    font-family: Arial, sans-serif;
    font-size:12px;
    color:#333;
}
h1{
    text-align:center;
    margin-bottom:25px;
}
h3{
    margin-top:30px;
    margin-bottom:10px;
}
table{
    width:100%;
    border-collapse:collapse;
}
.tabla-info td{
    border:1px solid #444;
    padding:6px;
}
.tabla-info .etiqueta{
    background:#f2f2f2;
    font-weight:bold;
    width:35%;
}
.tabla-discos{
    margin-top:10px;
}
.tabla-discos th{
    background:#eaeaea;
    border:1px solid #444;
    padding:6px;
    text-align:left;
}
.tabla-discos td{
    border:1px solid #444;
    padding:6px;
}
.tabla-discos tr{
    page-break-inside: avoid;
}

/* 🔥 NUEVO: estilos perifericos */
.tabla-perifericos{
    margin-top:10px;
}
.tabla-perifericos th{
    background:#eaeaea;
    border:1px solid #444;
    padding:6px;
}
.tabla-perifericos td{
    border:1px solid #444;
    padding:6px;
}
</style>
';

// ==============================
// HTML FINAL
// ==============================
$html = $estilos;
$html .= '<h1>Ficha Técnica del Equipo</h1>';
$html .= '<h3>Información General</h3>';
$html .= $tabla;

$html .= $tablaDiscos;        // discos
$html .= $tablaPerifericos;   // 👈 PERIFÉRICOS AQUÍ

// ==============================
// GENERAR PDF
// ==============================
$dompdf = new Dompdf();
$dompdf->loadHtml($html);
$dompdf->setPaper('A4', 'portrait');
$dompdf->render();
$dompdf->stream("ficha_equipo_{$row['id']}.pdf", ["Attachment" => false]);