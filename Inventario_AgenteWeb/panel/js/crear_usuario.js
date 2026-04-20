document.getElementById("btnCrearUsuario").addEventListener("click", () => {
    let usuario = document.getElementById("inputUsuarioNuevo").value;
    let password = document.getElementById("inputPasswordNuevo").value;

    fetch("/Inventario_AgenteWeb/api/crear_usuario.php", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            usuario: usuario,
            password: password
        })
    })
    .then(res => res.text())
    .then(res => {
        console.log("RESPUESTA RAW:", res);
        try {
            let json = JSON.parse(res);
            if (json.success) {
                alert("Usuario creado correctamente");

                const modalElement = document.getElementById("modalCrearUsuario");
                const modal = bootstrap.Modal.getInstance(modalElement);
                modal.hide();

                document.getElementById("inputUsuarioNuevo").value = "";
                document.getElementById("inputPasswordNuevo").value = "";
            } else {
                alert(json.message);
            }
        } catch (e) {
            alert("Error del servidor (no es JSON)");
        }
    })
    .catch(() => {
        alert("Error de conexión");
    });
});