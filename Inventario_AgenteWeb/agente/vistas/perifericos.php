<?php
function renderizarPerifericos($perifericos)
{
    if (empty($perifericos)) {
        return "<p>Sin información de periféricos</p>";
    }

    ob_start(); //
    ?>

    <h3>Periféricos</h3>

    <table class="tabla-perifericos">
        <tr>
            <th>ID</th>
            <th>Tipo</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Tóner</th>
            <th>IP</th>
            <th>C.I</th>
            <th>S/N</th>
            <th>Editar</th>
        </tr>

        <pre>
        <?php print_r($perifericos); ?>
        </pre>
        <?php foreach ($perifericos as $p): ?>
            <tr>
                <td><?= htmlspecialchars($p["id_periferico"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["tipo"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["marca"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["modelo"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["toner"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["ip"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["ci"] ?? "N/A") ?></td>
                <td><?= htmlspecialchars($p["sn"] ?? "N/A") ?></td>

                
                <td>
                    <button 
                        class="btn btn-warning btn-editar"
                        data-id="<?= $p['equipo_id'] ?? '' ?>"
                        data-codigo=""
                        data-departamento="<?= htmlspecialchars($p['departamento'] ?? '') ?>"
                        data-usuario="<?= htmlspecialchars($p['usuario'] ?? '') ?>">
                        Editar
                    </button>
                </td>
            </tr>
        <?php endforeach; ?>

    </table>

    <?php

    return ob_get_clean(); // 
}