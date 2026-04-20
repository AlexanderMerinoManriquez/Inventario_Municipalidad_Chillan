const buscador = document.getElementById("buscador");
const botonBuscar = document.getElementById("btnBuscar");
const mensaje = document.getElementById("sinResultados");

// 🔥 Bloquear autocompletado agresivamente
window.addEventListener("DOMContentLoaded", () => {
    buscador.value = "";
    buscador.setAttribute("autocomplete", "off");
    buscador.setAttribute("readonly", true);

    // truco para evitar autofill
    setTimeout(() => {
        buscador.removeAttribute("readonly");
    }, 100);
});

// 🔄 Obtener filas dinámicamente
function obtenerFilas() {
    return document.querySelectorAll("tbody tr");
}

// 🔍 Función de búsqueda (manual)
function ejecutarBusqueda() {
    const filtro = buscador.value.toLowerCase().trim();
    let visibles = 0;

    const filas = obtenerFilas();

    filas.forEach(fila => {
        const texto = fila.innerText.toLowerCase();

        if (filtro === "") {
            fila.style.display = "";
            visibles++;
        } else if (texto.includes(filtro)) {
            fila.style.display = "";
            visibles++;
        } else {
            fila.style.display = "none";
        }
    });

    mensaje.style.display = visibles === 0 ? "block" : "none";
}

// 🔘 Click en botón
botonBuscar.addEventListener("click", ejecutarBusqueda);

// ⌨️ Enter también busca
buscador.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        ejecutarBusqueda();
    }
});