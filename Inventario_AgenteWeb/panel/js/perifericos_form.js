document.addEventListener("DOMContentLoaded", function () {

    const contenedor = document.getElementById("contenedor-perifericos");
    const btnAgregar = document.getElementById("btnAgregarPerifericos");
    const btnQuitar = document.getElementById("btnQuitarPerifericos");

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

    btnQuitar.addEventListener("click", function () {

        const bloques = contenedor.querySelectorAll(".bloque-perifericos");

        if (bloques.length > 0) {
            bloques[bloques.length - 1].remove();
        }

        if (contenedor.children.length === 0) {
            contenedor.style.display = "none";
        }
    });

});