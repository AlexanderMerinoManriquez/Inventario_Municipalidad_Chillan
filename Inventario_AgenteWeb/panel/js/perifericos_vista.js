document.addEventListener("DOMContentLoaded", function () {

    let vistaActual = "equipos";

    const theadOriginal = document.getElementById("theadTabla").innerHTML;
    const tbodyOriginal = document.getElementById("tbodyTabla").innerHTML;

    const btnVista = document.getElementById("btnVistaPerifericos");

    btnVista.addEventListener("click", () => {

        const thead = document.getElementById("theadTabla");
        const tbody = document.getElementById("tbodyTabla");

        if (vistaActual === "equipos") {

            vistaActual = "perifericos";
            btnVista.innerText = "💻 Ver Equipos";

            thead.innerHTML = `
                <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Departamento</th>
                    <th>Tipo</th>
                    <th>Marca</th>
                    <th>Modelo</th>
                    <th>Tóner</th>
                    <th>IP</th>
                    <th>C.I</th>
                    <th>S/N</th>
                    <th>Detalles</th>
                    <th>Editar</th>
                </tr>
            `;

            tbody.innerHTML = `<tr><td colspan="12">Cargando periféricos...</td></tr>`;

            fetch("/Inventario_AgenteWeb/api/obtener_perifericos.php")
                .then(res => res.json())
                .then(data => {

                    tbody.innerHTML = "";

                    if (!data.length) {
                        tbody.innerHTML = `<tr><td colspan="12">Sin periféricos</td></tr>`;
                        return;
                    }

                    let contador = 1;

                    data.forEach(p => {
                        tbody.innerHTML += `
                            <tr>
                                <td>${contador}</td>
                                <td>${p.usuario}</td>
                                <td>${p.departamento}</td>
                                <td>${p.tipo || ""}</td>
                                <td>${p.marca || ""}</td>
                                <td>${p.modelo || ""}</td>
                                <td>${p.toner || ""}</td>
                                <td>${p.ip || ""}</td>
                                <td>${p.ci || ""}</td>
                                <td>${p.sn || ""}</td>

                                <td>
                                    <a class="btn btn-primary"
                                    href="/Inventario_AgenteWeb/panel/pdf.php?id=${p.equipo_id}"
                                    target="_blank">
                                    Ver ficha
                                    </a>
                                </td>

                                <td>
                                    <button class="btn btn-warning btn-editar-periferico"
                                        data-equipo="${p.equipo_id}">
                                        Editar
                                    </button>
                                </td>
                            </tr>
                        `;
                        contador++;
                    });

                })
                .catch(err => {
                    console.error(err);
                    alert("Error cargando periféricos");
                });

        } else {

            vistaActual = "equipos";
            btnVista.innerText = "🔧 Ver Periféricos";

            thead.innerHTML = theadOriginal;
            tbody.innerHTML = tbodyOriginal;
        }

    });

});