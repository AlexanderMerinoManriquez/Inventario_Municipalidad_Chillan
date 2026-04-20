document.addEventListener("DOMContentLoaded", function () {

    const contenedor = document.getElementById("contenedor-perifericos");
    const btnAgregar = document.getElementById("btnAgregarPerifericos");
    const btnQuitar = document.getElementById("btnQuitarPerifericos");

    // =========================
    // AGREGAR PERIFERICOS
    // =========================
    btnAgregar.addEventListener("click", function () {

        contenedor.style.display = "block";

        const bloque = document.createElement("div");
        bloque.classList.add("bloque-perifericos");

        const numero = contenedor.children.length + 1;

        bloque.innerHTML = `

            <div style="font-weight: bold; margin-bottom: 10px;">
                Periférico ${numero}
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">Tipo periférico:</label>
                <select class="form-control form-control-sm tipo">
                    <option value="">Seleccione..</option>
                    <option value="Multifuncional">Multifuncional</option>
                    <option value="Impresora">Impresora</option>
                    <option value="Plotter">Plotter</option>
                    <option value="Scanner">Scanner</option>
                </select>
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">Marca:</label>
                <select class="form-control form-control-sm marca">
                    <option value="">Seleccione..</option>
                    <option value="HP">HP</option>
                    <option value="Epson">Epson</option>
                    <option value="Brother">Brother</option>
                    <option value="Canon">Canon</option>
                    <option value="Samsung">Samsung</option>
                    <option value="RICOH">RICOH</option>
                </select>
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">Modelo:</label>
                <input type="text" class="form-control form-control-sm modelo">
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">Tóner:</label>
                <input type="text" class="form-control form-control-sm toner">
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">IP:</label>
                <input type="text" class="form-control form-control-sm ip">
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">C.I:</label>
                <input type="text" class="form-control form-control-sm ci">
            </div>

            <div class="mb-2 d-flex align-items-center">
                <label style="min-width: 180px;">S/N:</label>
                <input type="text" class="form-control form-control-sm sn">
            </div>

            <hr>
        `;

        contenedor.appendChild(bloque);
    });

    // =========================
    // QUITAR PERIFERICOS
    // =========================
    btnQuitar.addEventListener("click", function () {

        const bloques = contenedor.querySelectorAll(".bloque-perifericos");

        if (bloques.length > 0) {
            bloques[bloques.length - 1].remove();
        }

        if (contenedor.children.length === 0) {
            contenedor.style.display = "none";
        }
    });

    // =========================
    // VISTA PERIFERICOS
    // =========================

    let vistaActual = "equipos";

    const theadOriginal = document.getElementById("theadTabla").innerHTML;
    const tbodyOriginal = document.getElementById("tbodyTabla").innerHTML;

    const btnVista = document.getElementById("btnVistaPerifericos");

    btnVista.aperiféricos_form.jsddEventListener("click", () => {

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

            tbody.innerHTML = `<tr><td colspan="9">Cargando periféricos...</td></tr>`;

            fetch("/Inventario_AgenteWeb/api/obtener_perifericos.php")
            .then(res => res.json())
            .then(data => {

                tbody.innerHTML = "";

                if (!data.length) {
                    tbody.innerHTML = `<tr><td colspan="9">Sin periféricos</td></tr>`;
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

                            <td class="text-center">
                                <a class="btn btn-primary"
                                href="/Inventario_AgenteWeb/panel/pdf.php?id=${p.equipo_id}"
                                target="_blank">
                                Ver ficha
                                </a>
                            </td>

                            <td>
                                <button class="btn btn-warning">
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

document.getElementById("tbodyTabla").addEventListener("click", function (e) {

    if (e.target.classList.contains("btn-editar-periferico")) {

        const fila = e.target.closest("tr");

        const datos = {
            equipo_id: e.target.dataset.equipo,
            tipo: fila.children[3].innerText,
            marca: fila.children[4].innerText,
            modelo: fila.children[5].innerText,
            toner: fila.children[6].innerText,
            ip: fila.children[7].innerText,
            ci: fila.children[8].innerText,
            sn: fila.children[9].innerText
        };

        abrirModalPeriferico(datos);
    }

});

function abrirModalPeriferico(data) {

    const modal = new bootstrap.Modal(document.getElementById("modalPeriferico"));

    // Cargar datos en inputs
    document.getElementById("editTipo").value = data.tipo || "";
    document.getElementById("editMarca").value = data.marca || "";
    document.getElementById("editModelo").value = data.modelo || "";
    document.getElementById("editToner").value = data.toner || "";
    document.getElementById("editIp").value = data.ip || "";
    document.getElementById("editCi").value = data.ci || "";
    document.getElementById("editSn").value = data.sn || "";

    // guardar equipo_id oculto
    document.getElementById("editEquipoId").value = data.equipo_id;

    modal.show();
}