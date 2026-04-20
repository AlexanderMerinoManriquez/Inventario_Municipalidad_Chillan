const toggle = document.getElementById("themeToggle");

// Cargar estado guardado
window.onload = function () {
    const theme = localStorage.getItem("theme");

    if (theme === "dark") {
        document.body.classList.add("dark");
        toggle.checked = true;
    }
};

// Evento del switch
toggle.addEventListener("change", function () {
    document.body.classList.toggle("dark");

    if (toggle.checked) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
});