document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // MODAL
    // =========================
    const modalElement = document.getElementById("modalFicha");
    const modal = new bootstrap.Modal(modalElement);

    // =========================
    // INPUTS
    // =========================
    const inputId = document.getElementById("equipoId");
    const inputCodigo = document.getElementById("inputCodigo");
    const inputDepartamento = document.getElementById("inputDepartamento");
    const inputUsuario = document.getElementById("inputUsuario");

    const contenedorPerifericos = document.getElementById("contenedor-perifericos");
    const btnGuardar = document.getElementById("guardarCodigo");

    // =========================
    // CLICK GLOBAL PARA EDITAR
    // =========================
    document.addEventListener("click", function (e) {

        if (!e.target.classList.contains("btn-editar")) return;

        const btn = e.target;

        // 🔥 MODO SEGÚN BOTÓN
        const modo = btn.dataset.modo || "equipos";

        // =========================
        // CARGA DATOS COMUNES
        // =========================
        inputId.value = btn.dataset.id;

        inputCodigo.value = (btn.dataset.codigo === "SIN")
            ? "sin"
            : (btn.dataset.codigo || "");

        inputDepartamento.value = btn.dataset.departamento || "";
        inputUsuario.value = btn.dataset.usuario || "";

        // limpiar errores
        inputCodigo.classList.remove("is-invalid");
        inputDepartamento.classList.remove("is-invalid");

        // =========================
        // LIMPIAR CONTENEDOR
        // =========================
        contenedorPerifericos.innerHTML = "";
        contenedorPerifericos.style.display = "none";

        // =========================
        // SI ES PERIFÉRICOS
        // =========================
        if (modo === "perifericos") {

            contenedorPerifericos.style.display = "block";

            fetch("/Inventario_AgenteWeb/api/obtener_perifericos.php")
                .then(res => res.json())
                .then(data => {

                    const equipoId = btn.dataset.id;

                    const perifericosEquipo = data.filter(p => p.equipo_id == equipoId);

                    perifericosEquipo.forEach((p, index) => {

                        const bloque = document.createElement("div");
                        bloque.classList.add("bloque-perifericos");

                        bloque.innerHTML = `
                            <div><strong>Periférico ${index + 1}</strong></div>

                            <input class="form-control tipo mb-1" value="${p.tipo || ""}" placeholder="Tipo">
                            <input class="form-control marca mb-1" value="${p.marca || ""}" placeholder="Marca">
                            <input class="form-control modelo mb-1" value="${p.modelo || ""}" placeholder="Modelo">
                            <input class="form-control toner mb-1" value="${p.toner || ""}" placeholder="Tóner">
                            <input class="form-control ip mb-1" value="${p.ip || ""}" placeholder="IP">
                            <input class="form-control ci mb-1" value="${p.ci || ""}" placeholder="C.I">
                            <input class="form-control sn mb-1" value="${p.sn || ""}" placeholder="S/N">

                            <hr>
                        `;

                        contenedorPerifericos.appendChild(bloque);
                    });

                })
                .catch(err => {
                    console.error(err);
                    alert("Error cargando periféricos");
                });
        }

        modal.show();
    });

    // =========================
    // GUARDAR CAMBIOS
    // =========================
    btnGuardar.addEventListener("click", () => {

        const id = inputId.value;
        const codigo = inputCodigo.value.trim();
        const departamento = inputDepartamento.value.trim();
        const usuario = inputUsuario.value.trim();

        if (!id || !departamento || !usuario) {
            alert("⚠️ Usuario y Departamento son obligatorios");
            return;
        }

        let body = {
            id: id,
            codigo_inventario: codigo,
            departamento: departamento,
            usuario: usuario
        };

        // =========================
        // PERIFÉRICOS
        // =========================
        const bloques = document.querySelectorAll(".bloque-perifericos");

        if (bloques.length > 0) {

            let perifericos = [];

            bloques.forEach(b => {

                const tipo = b.querySelector(".tipo")?.value.trim();
                const marca = b.querySelector(".marca")?.value.trim();
                const modelo = b.querySelector(".modelo")?.value.trim();
                const toner = b.querySelector(".toner")?.value.trim();
                const ip = b.querySelector(".ip")?.value.trim();
                const ci = b.querySelector(".ci")?.value.trim();
                const sn = b.querySelector(".sn")?.value.trim();

                if (tipo || marca || modelo || toner || ip || ci || sn) {
                    perifericos.push({ tipo, marca, modelo, toner, ip, ci, sn });
                }
            });

            body.perifericos = perifericos;
        }

        btnGuardar.disabled = true;

        fetch("/Inventario_AgenteWeb/api/editar.php", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        })
        .then(res => res.json())
        .then(data => {

            if (data.success) {
                alert("✅ Actualizado");
                modal.hide();
                location.reload();
            } else {
                alert("❌ " + data.message);
            }

        })
        .catch(err => {
            console.error(err);
            alert("Error servidor");
        })
        .finally(() => {
            btnGuardar.disabled = false;
        });

    });

});