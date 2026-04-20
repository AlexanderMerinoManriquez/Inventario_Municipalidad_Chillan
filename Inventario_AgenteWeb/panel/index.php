<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if (!isset($_SESSION["usuario"])) {
    header("Location: panel/login.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Inventario</title>
    <link rel="icon" href="/Inventario_AgenteWeb/panel/images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="/Inventario_AgenteWeb/panel/css/index.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>

    <?php
    require_once __DIR__ . "/../config/conexion.php";
    require_once __DIR__ . "/../agente/logica/cpu.php";

    if ($conn->connect_error) {
        die("Error de conexión: " . $conn->connect_error);
    }

    $result = $conn->query("SELECT * FROM equipos");
    ?>

    <div class="user-panel">
        <div class="bienvenida">
            Bienvenido, <strong><?php echo htmlspecialchars($_SESSION["usuario"]); ?></strong>
        </div>
        <div class="acciones">
            <a href="/Inventario_AgenteWeb/api/logout.php" class="btn btn-danger btn-sm">
                Cerrar sesión
            </a>
            <button class="btn btn-success btn-sm" data-bs-toggle="modal" data-bs-target="#modalCrearUsuario">
                Crear usuario
            </button>
        </div>
    </div>

    <h1>Inventario de Equipos</h1>
    <p>Total de equipos: <?php echo $result->num_rows; ?></p>

    <label class="switch">
        <input type="checkbox" id="themeToggle">
        <span class="slider"></span>
    </label>

    <div class="tabla-equipo">

        <input type="text" style="display:none">
        <input type="password" style="display:none">

        <div class="buscador-container d-flex justify-content-between align-items-center">

            <button id="btnVistaPerifericos" class="btn btn-info">
                🔧 Ver Periféricos
            </button>

            <div class="d-flex gap-2">
                <input type="text" id="buscador" class="form-control" placeholder="Buscar..." autocomplete="off">
                <button type="button" id="btnBuscar" class="btn btn-primary">🔍</button>
            </div>

        </div>

        <div class="tabla-scroll">
            <table>
                <thead id="theadTabla">
                    <tr>
                        <th>Código Inventario</th>
                        <th>PC</th>
                        <th>Usuario</th>
                        <th>Departamento</th>
                        <th>Departamento Manual</th>
                        <th>Ubicación</th>
                        <th>Observaciones</th>
                        <th>Sistema</th>
                        <th>AnyDesk</th>
                        <th>CPU</th>
                        <th>RAM</th>
                        <th>Disco</th>
                        <th>IP</th>
                        <th>Detalles</th>
                        <th>Editar</th>
                    </tr>
                </thead>

                <tbody id="tbodyTabla">
                    <?php
                    if ($result->num_rows > 0) {
                        while ($row = $result->fetch_assoc()) {
                            $codigo = trim($row["codigo_inventario"] ?? "");
                            $regex = '/^\d{2}-\d{2}-\d{2}-\d{3}-\d{5}$/';
                            $observaciones = trim($row["observaciones"] ?? "");
                            ?>
                            <tr>
                                <td class="text-center">
                                    <?php
                                    if ($codigo === "" || is_null($row["codigo_inventario"])) {
                                        echo "<span class='badge bg-warning text-dark fs-6'>Pendiente</span>";
                                    } elseif (strtolower($codigo) === "sin") {
                                        echo "<span class='badge bg-success fs-6'>No Tiene</span>";
                                    } elseif (preg_match($regex, $codigo)) {
                                        echo htmlspecialchars($codigo);
                                    } else {
                                        echo "<span class='badge bg-danger fs-6'>Error</span>";
                                    }
                                    ?>
                                </td>

                                <td><?php echo htmlspecialchars($row["nombre_pc"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["usuario"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["departamento"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["departamento_manual"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["ubicacion"] ?? ""); ?></td>
                                <td title="<?php echo htmlspecialchars($observaciones); ?>">
                                    <?php echo htmlspecialchars(mb_strimwidth($observaciones, 0, 40, "...")); ?>
                                </td>
                                <td><?php echo htmlspecialchars($row["sistema_operativo"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["anydesk"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars(formatearCPU($row["cpu"] ?? "")); ?></td>
                                <td><?php echo htmlspecialchars($row["ram"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["disco_total"] ?? ""); ?></td>
                                <td><?php echo htmlspecialchars($row["ip"] ?? ""); ?></td>

                                <td class="text-center align-middle">
                                    <a class="btn btn-primary btn-ficha-grande"
                                        href="/Inventario_AgenteWeb/panel/pdf.php?id=<?php echo (int)$row['id']; ?>" target="_blank">
                                        Ver ficha
                                    </a>
                                </td>

                                <td>
                                    <button
                                        type="button"
                                        class="btn btn-warning btn-editar"
                                        data-modo="equipos"
                                        data-id="<?php echo (int)$row['id']; ?>"
                                        data-codigo="<?php echo htmlspecialchars($row['codigo_inventario'] ?? '', ENT_QUOTES, 'UTF-8'); ?>"
                                        data-departamento="<?php echo htmlspecialchars($row['departamento'] ?? '', ENT_QUOTES, 'UTF-8'); ?>"
                                        data-departamento-manual="<?php echo htmlspecialchars($row['departamento_manual'] ?? '', ENT_QUOTES, 'UTF-8'); ?>"
                                        data-ubicacion="<?php echo htmlspecialchars($row['ubicacion'] ?? '', ENT_QUOTES, 'UTF-8'); ?>"
                                        data-observaciones="<?php echo htmlspecialchars($row['observaciones'] ?? '', ENT_QUOTES, 'UTF-8'); ?>"
                                        data-usuario="<?php echo htmlspecialchars($row['usuario'] ?? '', ENT_QUOTES, 'UTF-8'); ?>">
                                        Editar
                                    </button>
                                </td>
                            </tr>
                            <?php
                        }
                    } else {
                        echo "<tr><td colspan='15'>No hay equipos registrados</td></tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>

        <p id="sinResultados" style="display:none;">No se encontraron resultados</p>
    </div>

    <!-- Modal para poder editar -->
    <div class="modal fade" id="modalFicha" tabindex="-1" aria-labelledby="tituloModalFicha" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" style="max-width: 500px;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="tituloModalFicha">Editar equipo</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <input type="hidden" id="equipoId">

                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Usuario:</label>
                        <input type="text" id="inputUsuario" class="form-control form-control-sm">
                    </div>

                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Departamento:</label>
                        <input type="text" id="inputDepartamento" class="form-control form-control-sm">
                    </div>

                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Departamento Manual:</label>
                        <input type="text" id="inputDepartamentoManual" class="form-control form-control-sm">
                    </div>

                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Ubicación:</label>
                        <input type="text" id="inputUbicacion" class="form-control form-control-sm">
                    </div>

                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Código Inventario:</label>
                        <input type="text" id="inputCodigo" class="form-control form-control-sm">
                    </div>

                    <hr>

                    <div class="form-group">
                        <div id="contenedor-perifericos" style="display:none;"></div>

                        <div id="acciones-perifericos" style="display:none;">
                            <div class="d-flex justify-content-center align-items-center gap-2">
                                <button type="button" id="btnAgregarPerifericos" class="btn btn-success btn-accion">
                                    Agregar Periféricos
                                </button>
                                <button type="button" id="btnQuitarPerifericos" class="btn btn-danger btn-accion">
                                    Eliminar Periféricos
                                </button>
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12">
                                Observaciones
                            </label>
                            <div class="col-md-6 col-sm-6 col-xs-12">
                                <textarea
                                    class="form-control"
                                    rows="3"
                                    id="detalleEquipoEditar"
                                    placeholder="Ingrese observaciones del equipo"
                                    style="height: 100px; width: 425px;"></textarea>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancelar
                    </button>
                    <button type="button" class="btn btn-primary" id="guardarCodigo">
                        Guardar cambios
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal crear usuario -->
    <div class="modal fade" id="modalCrearUsuario" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered" style="max-width: 500px;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Crear Usuario</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <div class="mb-2">
                        <label>Usuario:</label>
                        <input type="text" id="inputUsuarioNuevo" class="form-control">
                    </div>

                    <div class="mb-2">
                        <label>Contraseña:</label>
                        <input type="password" id="inputPasswordNuevo" class="form-control">
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancelar
                    </button>
                    <button id="btnCrearUsuario" class="btn btn-success">
                        Crear
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- SCRIPTS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/modo_oscuro.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/crud.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/busqueda.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/crear_usuario.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/perifericos_form.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/perifericos_modal.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/perifericos_vista.js"></script>

</body>

</html>