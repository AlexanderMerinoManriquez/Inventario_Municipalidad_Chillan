document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault();

    fetch("../api/login.php", {
        method: "POST",
        credentials: "include", // 🔥 IMPORTANTE PARA SESIÓN
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            usuario: document.getElementById("usuario").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(res => {

        if (res.success) {
            window.location.href = "index.php";
        } else {
            alert(res.message);
        }

    })
    .catch(() => {
        alert("Error de conexión");
    });
});