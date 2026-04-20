<?php
// 🔥 INICIAR SESIÓN SOLO UNA VEZ
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// 🔐 SI YA ESTÁ LOGUEADO → REDIRIGE
if (isset($_SESSION["usuario"])) {
    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <link rel="icon" href="/Inventario_AgenteWeb/panel/images/favicon.ico">
    <link rel="stylesheet" href="/Inventario_AgenteWeb/panel/css/login.css">

    <meta charset="UTF-8">
    <title>Login</title>

    <link rel="stylesheet" href="css/login.css">
</head>
<body>

<div class="login-box">
    <h4 class="login-title">Iniciar Sesión</h4>

    <form id="loginForm">
        <input type="text" id="usuario" placeholder="Usuario" required>
        <input type="password" id="password" placeholder="Contraseña" required>

        <button type="submit">Ingresar</button>
    </form>
</div>

<script src="/Inventario_AgenteWeb/panel/js/login.js"></script>

</body>
</html>