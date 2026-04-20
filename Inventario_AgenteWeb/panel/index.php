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

            <!-- 🔥 BOTÓN PERIFÉRICOS (IZQUIERDA) -->
            <button id="btnVistaPerifericos" class="btn btn-info">
                🔧 Ver Periféricos
            </button>

            <!-- 🔍 BUSCADOR (DERECHA) -->
            <div class="d-flex gap-2">
                <input type="text" id="buscador" class="form-control" placeholder="Buscar..." autocomplete="off">
                <button type="button" id="btnBuscar" class="btn btn-primary">🔍</button>
            </div>

        </div>

        <div class="tabla-scroll">
            <table>

                <!-- 🔥 THEAD CON ID -->
                <thead id="theadTabla">
                    <tr>
                        <th>Código Inventario</th>
                        <th>PC</th>
                        <th>Usuario</th>
                        <th>Departamento</th>
                        <th>Sistema</th>
                        <th>anydesk</th>
                        <th>CPU</th>
                        <th>RAM</th>
                        <th>Disco</th>
                        <th>IP</th>
                        <th>Detalles</th>
                        <th>Editar</th>
                    </tr>
                </thead>

                <!-- 🔥 TBODY CON ID -->
                <tbody id="tbodyTabla">
                    <?php
                    if ($result->num_rows > 0) {
                        while ($row = $result->fetch_assoc()) {
                            ?>
                            <tr>
                                <!-- CODIGO INVENTARIO -->
                                <td class="text-center">
                                    <?php
                                    $codigo = trim($row["codigo_inventario"] ?? "");
                                    $regex = '/^\d{2}-\d{2}-\d{2}-\d{3}-\d{5}$/';

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

                                <td><?php echo $row["nombre_pc"]; ?></td>
                                <td><?php echo $row["usuario"]; ?></td>
                                <td><?php echo $row["departamento"]; ?></td>
                                <td><?php echo $row["sistema_operativo"]; ?></td>
                                <td><?php echo $row["anydesk"]; ?></td>
                                <td><?php echo formatearCPU($row["cpu"]); ?></td>
                                <td><?php echo $row["ram"]; ?></td>
                                <td><?php echo $row["disco_total"]; ?></td>
                                <td><?php echo $row["ip"]; ?></td>

                                <td class="text-center align-middle">
                                    <a class="btn btn-primary btn-ficha-grande"
                                        href="/Inventario_AgenteWeb/panel/pdf.php?id=<?php echo $row['id']; ?>" target="_blank">
                                        Ver ficha
                                    </a>
                                </td>

                                <td>
                                    <button type="button" class="btn btn-warning btn-editar"
                                        data-modo="equipos"
                                        data-id="<?php echo $row['id']; ?>"
                                        data-codigo="<?php echo $row['codigo_inventario']; ?>"
                                        data-departamento="<?php echo $row['departamento']; ?>"
                                        data-usuario="<?php echo $row['usuario']; ?>">
                                        Editar
                                    </button>
                                </td>

                            </tr>
                            <?php
                        }
                    } else {
                        echo "<tr><td colspan='13'>No hay equipos registrados</td></tr>";
                    }
                    ?>
                </tbody>

            </table>
        </div>

        <p id="sinResultados" style="display:none;">No se encontraron resultados</p>
    </div>
    <!-- Modal para poder editar -->
    <div class="modal fade" id="modalFicha" tabindex="-1" aria-labelledby="tituloModalFicha" aria-hidden="true">
        <!-- Fijar el modal centrado y el tamaño de este mismo -->
        <div class="modal-dialog modal-dialog-centered" style="max-width: 500px;">
            <div class="modal-content">
                <!-- Definir formato del header del modal -->
                <div class="modal-header">
                    <h5 class="modal-title" id="tituloModalFicha">Editar equipo</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <!-- Items que se utilizaran en la edicion -->
                <div class="modal-body">
                    <!-- Identificador para insertar en BDD -->
                    <input type="hidden" id="equipoId">
                    <!-- Edicion del campo Usuario -->
                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Usuario:</label>
                        <input type="text" id="inputUsuario" class="form-control form-control-sm">
                    </div>
                    <!-- Edicion del campo Departamento -->
                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Departamento:</label>
                        <input type="text" id="inputDepartamento" class="form-control form-control-sm">
                    </div>
                    <!-- Edicion del campo Codigo de inventario -->
                    <div class="mb-2 d-flex align-items-center">
                        <label style="min-width: 180px; margin-bottom: 0;">Código Inventario:</label>
                        <input type="text" id="inputCodigo" class="form-control form-control-sm">
                    </div>
                    <hr>
                    <div class="form-group">
                        <!-- Campo para agregar perifericos -->
                        <div id="contenedor-perifericos" style="display:none;"></div>
                        <div id="acciones-perifericos" style="display:none;">
                            <div class="d-flex justify-content-center align-items-center gap-2">
                                <button type="button" id="btnAgregarPerifericos" class="btn btn-success btn-accion">
                                    Agregar Perifericos
                                </button>
                                <button type="button" id="btnQuitarPerifericos" class="btn btn-danger btn-accion">
                                    Eliminar Perifericos
                                </button>
                            </div>
                        </div>
                        <!-- Detalles -->
                        <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12">
                                Detalles
                            </label>
                            <div class="col-md-6 col-sm-6 col-xs-12">
                                <textarea class="form-control" rows="3" id="detalleEquipoEditar"
                                    placeholder="Ingrese detalle equipo" style="height: 100px; width: 425px;">
                                    </textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Botones de funcion dentro del modal -->
                <div class="modal-footer">
                    <!-- Boton para cancelar la edicion de datos -->
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancelar
                    </button>
                    <!-- Boton para guardar lo editado y enviar el UPDATE a la BDD -->
                    <button type="button" class="btn btn-primary" id="guardarCodigo">
                        Guardar cambios
                    </button>
                </div>
            </div>
        </div>
    </div>
    <!-- Modal crear usuario -->
    <div class="modal fade" id="modalCrearUsuario" tabindex="-1">
        <!-- Fijar el modal centrado y el tamaño de este mismo -->
        <div class="modal-dialog modal-dialog-centered" style="max-width: 500px;">
            <div class="modal-content">
                <!-- Definir formato del header del modal -->
                <div class="modal-header">
                    <h5 class="modal-title">Crear Usuario</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <!-- Valores que se piden para la creacion del usuario-->
                <div class="modal-body">
                    <!-- Definir el capo usuario -->
                    <div class="mb-2">
                        <label>Usuario:</label>
                        <input type="text" id="inputUsuarioNuevo" class="form-control">
                    </div>
                    <!-- Definir el campo contraseña -->
                    <div class="mb-2">
                        <label>Contraseña:</label>
                        <input type="password" id="inputPasswordNuevo" class="form-control">
                    </div>
                </div>
                <!-- Botones de funcion dentro del modal -->
                <div class="modal-footer">
                    <!-- Boton para cancelar la creacion de usuario -->
                    <button class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancelar
                    </button>
                    <!-- Boton para guardar los datos y enviarlos a la BDD -->
                    <button id="btnCrearUsuario" class="btn btn-success">
                        Crear
                    </button>
                </div>
            </div>
        </div>
    </div>
    <!-- SCRIPTS -->

    <!-- Script de los estilos y funciones de bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Script de los estilos y funciones del modo oscuro -->
    <script src="/Inventario_AgenteWeb/panel/js/modo_oscuro.js"></script>
    <!-- Script para la creacion, edicion y eliminacion de datos (CRUD) -->
    <script src="/Inventario_AgenteWeb/panel/js/crud.js"></script>
    <!-- Script para la funcion de busqueda -->
    <script src="/Inventario_AgenteWeb/panel/js/busqueda.js"></script>
    <!-- Script para la creacion de algun usuario en la BDD -->
    <script src="/Inventario_AgenteWeb/panel/js/crear_usuario.js"></script>
    <!-- Script para agregar perifericos -->
    <script src="/Inventario_AgenteWeb/panel/js/perifericos_form.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/perifericos_modal.js"></script>
    <script src="/Inventario_AgenteWeb/panel/js/perifericos_vista.js"></script>

</body>

</html>