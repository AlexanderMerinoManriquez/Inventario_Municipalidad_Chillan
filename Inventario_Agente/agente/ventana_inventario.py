import json
import os
import socket
from datetime import datetime

import requests
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from funciones.anydesk import obtener_anydesk
from funciones.cpu import obtener_cpu
from funciones.discos.main import obtener_discos_smart
from funciones.discos.utils import obtener_ruta_smart
from funciones.grupo_trabajo import obtener_grupo_trabajo
from funciones.ip import obtener_ip
from funciones.monitores import obtener_monitores
from funciones.impresoras import obtener_impresoras_activas
from funciones.permisos import admin
from funciones.ram import obtener_ram
from funciones.serial import obtener_serial
from funciones.sistema_operativo import obtener_sistema
from funciones.uuid import obtener_uuid

# ── Rutas ──────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH   = os.path.join(BASE_DIR, "config.txt")
RESPALDOS_DIR = os.path.join(BASE_DIR, "RESPALDOS_FALLIDOS")
ICON_PATH     = os.path.join(BASE_DIR, "iconoMuni.png")
BANNER_PATH   = os.path.join(BASE_DIR, "Bannermuni.png")

# ── Campos automáticos ────────────────────────────────────────────────────────
CAMPOS_AUTO = [
    ("nombre_pc",         socket.gethostname,   "Nombre PC"),
    ("departamento",      obtener_grupo_trabajo, "Departamento PC"),
    ("sistema_operativo", obtener_sistema,       "Sistema operativo"),
    ("anydesk",           obtener_anydesk,       "AnyDesk"),
    ("cpu",               obtener_cpu,           "Procesador"),
    ("ram",               obtener_ram,           "RAM"),
    ("ip",                obtener_ip,            "IP"),
    ("uuid",              obtener_uuid,          "UUID"),
    ("serial",            obtener_serial,        "N° Serie"),
]

CAMPOS_MONITOR   = [("marca", "Marca:"), ("modelo", "Modelo:"), ("pulgadas", "Pulgadas:")]
CAMPOS_IMPRESORA = [("tipo", "Tipo:"), ("marca", "Marca:"), ("modelo", "Modelo:"),
                    ("ip", "IP:"), ("toner_tinta", "Tóner / Tinta:")]

OBLIGATORIOS = {
    "usuario":             "Funcionario responsable",
    "registrado_por":      "Registrado por",
    "ubicacion":           "Ubicación",
    "departamento_manual": "Departamento / dirección",
}

DEPARTAMENTOS_UBICACION = {
    "ADMINISTRACION": "Dieciocho de Septiembre 510",
    "ADM-INFORMATICA": "Dieciocho de Septiembre 510",
    "ADM-EVENTOSRECREATIVOS": "Dieciocho de Septiembre 510",
    "ADM-PSICOSOCIAL": "Dieciocho de Septiembre 510",
    "ADM-TRANSPARENCIA": "Dieciocho de Septiembre 510",
    "ADM-VIGILANTES": "Dieciocho de Septiembre 510",
    "ADM-ORGANISMO DE SEGURIDAD INTERNO": "Dieciocho de Septiembre 510",
    "CONCEJO": "Dieciocho de Septiembre 510",
    "CONTROL": "Dieciocho de Septiembre 510",
    "DAF": "Dieciocho de Septiembre 510",
    "DAF-RENTAS": "Dieciocho de Septiembre 510",
    "DAF-R.R.H.H.": "Dieciocho de Septiembre 510",
    "DAF-TESORERIA": "Dieciocho de Septiembre 510",
    "DAF-ADQUISICIONES": "Dieciocho de Septiembre 510",
    "DAF-CONTABILIDAD": "Dieciocho de Septiembre 510",
    "DAF-COBRANZAS": "Dieciocho de Septiembre 510",
    "DAF-BIENESTAR": "Dieciocho de Septiembre 510",
    "DAF-GESTION DE PAGO": "Dieciocho de Septiembre 510",
    "DAF-HONORARIOS": "Dieciocho de Septiembre 510",
    "DAF-CONVENIOS": "Dieciocho de Septiembre 510",
    "DAF-INVENTARIO": "Dieciocho de Septiembre 510",
    "DAF-PREVENCION DE RIESGO": "Dieciocho de Septiembre 510",
    "JURIDICA": "Dieciocho de Septiembre 510",
    "OFICINA DE PARTES": "Dieciocho de Septiembre 510",
    "SECRETARIA MUNICIPAL": "Dieciocho de Septiembre 510",
    "SUREFI": "Dieciocho de Septiembre 510",
    "TRANSPARENCIA EXTERNA": "Dieciocho de Septiembre 510",
    "ALCALDIA": "Dieciocho de Septiembre 510",
    "ALCALDIA-COMUNICACIONES": "Dieciocho de Septiembre 510",
    "ALCALDIA-REDES SOCIALES": "Dieciocho de Septiembre 510",
    "RELACIONES PUBLICAS": "Dieciocho de Septiembre 510",
    "PROTOCOLO": "Dieciocho de Septiembre 510",
    "GABINETE": "Dieciocho de Septiembre 510",
    "CASCHILE": "Dieciocho de Septiembre 510",
    "DIDECO": "Arauco 983",
    "DIDECO-CHILE CRECE CONTIGO": "Arauco 983",
    "DIDECO-VIVIENDA": "Arauco 983",
    "DIDECO-HABITABILIDAD": "Arauco 983",
    "DIDECO-4 A 7": "Arauco 983",
    "DIDECO-JEFAS DE HOGAR": "Arauco 983",
    "DIDECO-VINCULOS": "Arauco 983",
    "DIDECO-ESTRATIFICACION SOCIAL": "Arauco 983",
    "DIDECO-OOCC": "Arauco 983",
    "DIDECO-COMUNICACIONES": "Arauco 983",
    "DIDECO-CENTRO DE LA MUJER": "Arauco 983",
    "DIDECO-MUJER SEXUALIDAD Y MATERNIDAD": "Arauco 983",
    "DIDECO-CASA DE ACOGIDA": "Arauco 983",
    "DIDECO-ASISTENCIA SOCIAL": "Arauco 983",
    "DIDECO-PROGRAMA CALLE": "Arauco 983",
    "DIDECO-PROGRAMA FAMILIAS": "Arauco 983",
    "DIDECO-EMPODERAMIENTO DESARROLLO INTEGRAL": "Arauco 983",
    "DIDECO-OMAJ": "Arauco 983",
    "DIDECO-SUBISDIOS ESTATALES Y PENSIONES": "Arauco 983",
    "DIDECO-SUBSIDIOS ESTATALES": "Arauco 983",
    "DIDECO- PREVENCIÓN DE LA VIOLENCIA": "Arauco 983",
    "DIDECO-ADULTO MAYOR": "Arauco 983",
    "DIDECO-CENTRO DIURNO": "Arauco 983",
    "DIDECO-RESIDENCIA TRANSITORIA": "Arauco 983",
    "DIDECO-SUBSIDIOS Y PENSIONES": "Arauco 983",
    "DIDECO-ORGANIZACIONES COMUNITARIAS": "Arauco 983",
    "DIDECO-CONTROL Y GESTION Y LOGISTICA": "Arauco 983",
    "DIDECO-REGISTRO SOCIAL DE HOGARES": "Arauco 983",
    "DIDECO-BECAS": "Arauco 983",
    "DIDECO-OFICINA DE LA DIVERSIDAD SOCIAL Y CULTURAL": "Arauco 983",
    "DIDECO-MUJERES JEFAS DE HOGAR": "Arauco 983",
    "DIDECO-MUJERES DERECHOS SEXUALES Y REPRODUCTIVOS": "Arauco 983",
    "PROGRAMA DE PREVENCION DE LA VIOLENCIA DE GENERO": "Arauco 983",
    "DIDECO-RED LOCAL DE APOYOS Y CIUDADANOS": "Arauco 983",
    "DIDECO-DISCAPACIDAD": "Arauco 983",
    "DIDECO-OMAR": "Arauco 983",
    "DIDECO-EMERGENCIAS SOCIALES": "Arauco 983",
    "DIDECO-CONSULTORIO JURIDICO": "Arauco 983",
    "DIDECO-DERECHO DE ASEO": "Arauco 983",
    "DIDECO-SERNAC": "Arauco 983",
    "DIDECO-BIENES NACIONALES MUNICIPAL": "Arauco 983",
    "DIDECO-PROGRAMA APOYO A LA SEGURIDAD ALIMENTARIA": "Arauco 983",
    "DIDECO-ASENTAMIENTOS PRECARIOS(CAMPAMENTOS)": "Arauco 983",
    "DIDECO-PROGRAMA DE ACOMPAÑAMIENTO INTEGRAL FAMILIAR": "Arauco 983",
    "DIDECO-OFICINA DE MEDIACION": "Arauco 983",
    "OBRAS": "Avenida Libertad 431, Interior",
    "OBRAS-DEPTO ELECTRICO": "Avenida Libertad 431, Interior",
    "OBRAS-EDIFICACIÓN": "Avenida Libertad 431, Interior",
    "OBRAS-VIAL": "Avenida Libertad 431, Interior",
    "OBRAS-VIAL ELECTRICOS": "Avenida Libertad 431, Interior",
    "OBRAS-SUBDIVISION Y LOTEO": "Avenida Libertad 431, Interior",
    "OBRAS-EJECUCION": "Avenida Libertad 431, Interior",
    "DIDEPRO": "Claudio Arrau 602",
    "DESARROLLO ECON. Y PRODUCTIVO": "Claudio Arrau 602",
    "OMIL": "Claudio Arrau 602",
    "DIDEPRO-OMIL": "Claudio Arrau 602",
    "DIDEPRO-PRODESAL": "Claudio Arrau 602",
    "DIDEPRO-COWORK": "Claudio Arrau 602",
    "ASEO": "Sepúlveda Labbé 109",
    "ASEO-ORNATO": "Sepúlveda Labbé 109",
    "ASEO-AREAS VERDES": "Sepúlveda Labbé 109",
    "ASEO-DIMENSION": "Sepúlveda Labbé 109",
    "ASEO-MEDIO AMBIENTE": "Sepúlveda Labbé 109",
    "ASEO-CENTRO VETERINARIO": "Sepúlveda Labbé 109",
    "ASEO-MEJORAMIENTO DE ESPACIOS PÚBLICOS": "Sepúlveda Labbé 109",
    "SEGURIDAD PUBLICA": "Pedro Aguirre Cerda 297",
    "SEGURIDAD PUBLICA - OPERADOR DE CAMARAS": "Pedro Aguirre Cerda 297",
    "SEGURIDAD PUBLICA-APARCADERO MUNICIPAL": "Pedro Aguirre Cerda 297",
    "INSPECCION": "Pedro Aguirre Cerda 297",
    "INSPECCION-JUSTICIA VECINAL": "Pedro Aguirre Cerda 297",
    "ADM-EMERGENCIA": "Pedro Aguirre Cerda 297",
    "SUREFI-ESTADIO": "Pedro Aguirre Cerda 297",
    "SECPLA": "Herminda Martín 563",
    "SECPLA - QUIERO MI BARRIO": "Herminda Martín 563",
    "SECPLA - PARTICIPACION CIUDADANA": "Herminda Martín 563",
    "CULTURA": "Herminda Martín 579",
    "CULTURA-CENTRO CULTURAL": "Herminda Martín 579",
    "CULTURA-BIBLIOTECA": "Arauco 974",
    "CULTURA-MUSEO ARRAU": "Claudio Arrau 558",
    "CULTURA-MUSEO CIENCIAS NATURALES": "Pedro Aguirre Cerda s/n",
    "CULTURA-ESCUELA ARTISTICA": "Arauco 356",
    "EDUCACION": "Rosas 530",
    "SALUD": "Herminda Martín 557",
    "SALUD-FINANZAS": "Herminda Martín 557",
    "TRANSITO": "Maipón 277",
    "TRANSITO-LICENCIAS": "Maipón 277",
    "1ER JPL": "Avenida Ecuador 317",
    "2DO JPL": "Avenida Ecuador 429",
    "DEPORTE Y RECREACION": "5 de Abril 535",
    "DEPORTES Y RECREACION": "5 de Abril 535",
    "TURISMO": "Dieciocho de Septiembre 510",
    "DIDECO-HOSPEDERIA": "Avenida O´Higgins 1290",
    "SEGURIDAD PUBLICA - 24 HRS": "Avenida Libertad 374",
    "DIDECO-OPD": "Gamero 318",
    "INSPECCION-SENDA": "Claudio Arrau 718",
    "SUREFI-CENTRO DEPORTIVO QUILAMAPU": "Paul Harris con Flores Millán",
    "CEMENTERIO": "Sepúlveda Bustos s/n",
    "ADM-MERCADO": "Arturo Prat 605",
    "DELEGACION QUINCHAMALI": "Camino a Quinchamalí s/n",
    "DELEGACIÓN ORIENTE": "Avenida Nueva Oriente con Alonso de Ercilla",
    "EXTERIOR": "Sin dirección fija",
}

# ── Paleta institucional ───────────────────────────────────────────────────────
C = {
    "rojo":              "#C8102E",
    "rojo_hover":        "#a00d23",
    "rojo_light":        "#fce8ec",
    "rojo_dark":         "#8b0a1f",
    "blanco":            "#ffffff",
    "gris_bg":           "#f0f2f7",
    "gris_borde":        "#dde3ec",
    "gris_sub":          "#6b7a99",
    "gris_placeholder":  "#a0aec0",
    "texto":             "#1a2035",
    "texto_claro":       "#4a5568",
    "verde":             "#16783a",
    "verde_light":       "#e8f5ee",
    "amarillo":          "#b45309",
    "amarillo_light":    "#fef3c7",
    "azul_acento":       "#2563eb",
    "sombra":            "#e2e8f0",
    "badge_bg":          "#eef2ff",
    "badge_fg":          "#3730a3",
    "label_claro":       "#6f8fb3",
    "gris_panel":        "#f9fafb",
    "dropdown_sel":      "#fff0f3",
    "dropdown_sel_fg":   "#C8102E",
    "dropdown_hover":    "#f5f7ff",
}


# ── Respaldo local ─────────────────────────────────────────────────────────────
def guardar_respaldo(data: dict, estado: str, respuesta: str = "") -> str:
    try:
        os.makedirs(RESPALDOS_DIR, exist_ok=True)
        ts     = datetime.now()
        nombre = str(data.get("nombre_pc", "sin_nombre")).replace(" ", "_")
        ruta   = os.path.join(RESPALDOS_DIR, f"ERROR_{ts:%Y%m%d_%H%M%S}_{nombre}.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({
                "fecha":              ts.strftime("%Y-%m-%d %H:%M:%S"),
                "estado":             estado,
                "respuesta_servidor": respuesta,
                "datos_equipo":       data,
            }, f, ensure_ascii=False, indent=4)
        return ruta
    except Exception as e:
        return f"ERROR_AL_CREAR_RESPALDO: {e}"


# ── Formateo de capacidad ──────────────────────────────────────────────────────
def formatear_capacidad(valor: str) -> str:
    texto  = str(valor or "").strip().replace(",", ".")
    partes = texto.split()
    if not partes:
        return texto
    try:
        numero = float(partes[0])
        unidad = partes[1].upper() if len(partes) > 1 else "GB"
        return f"{round(numero)} {unidad}"
    except Exception:
        return texto


# ── Dropdown con búsqueda inline ───────────────────────────────────────────────
class BuscadorDepartamento(tk.Frame):
    MIN_CHARS = 2
    MAX_RESULTADOS = 8

    def __init__(self, parent, opciones, variable, on_select=None):
        super().__init__(parent, bg=C["gris_panel"])

        self.opciones = sorted(opciones)
        self.variable = variable
        self.on_select = on_select

        self.var_buscar = tk.StringVar(value=variable.get())

        self.entry = ttk.Entry(self, textvariable=self.var_buscar)
        self.entry.pack(fill="x")

        self.lista = tk.Listbox(
            self,
            height=0,
            font=("Segoe UI", 9),
            activestyle="none",
            bg=C["blanco"],
            fg=C["texto"],
            selectbackground=C["rojo"],
            selectforeground=C["blanco"],
            borderwidth=1,
            relief="solid",
        )
        self.lista.pack(fill="x", pady=(3, 0))
        self.lista.pack_forget()

        self.var_buscar.trace_add("write", lambda *_: self._filtrar())
        self.lista.bind("<ButtonRelease-1>", lambda e: self._seleccionar())
        self.lista.bind("<Return>", lambda e: self._seleccionar())
        self.entry.bind("<Return>", lambda e: self._seleccionar_primero())
        self.entry.bind("<Escape>", lambda e: self._ocultar_lista())

    def _normalizar(self, texto: str) -> str:
        tabla = str.maketrans("áéíóúÁÉÍÓÚüÜñÑ", "aeiouAEIOUuUnN")
        return texto.translate(tabla).replace("-", " ").lower()

    def _filtrar(self):
        texto = self._normalizar(self.var_buscar.get().strip())

        if not texto:
            self.variable.set("")
            if self.on_select:
                self.on_select("")
            self._ocultar_lista()
            return

        if len(texto) < self.MIN_CHARS:
            self._ocultar_lista()
            return

        palabras = texto.split()

        coinciden = [
            dep for dep in self.opciones
            if all(p in self._normalizar(dep) for p in palabras)
        ]

        empiezan = [
            dep for dep in coinciden
            if self._normalizar(dep).startswith(texto)
        ]
        resto = [dep for dep in coinciden if dep not in empiezan]
        resultados = (empiezan + resto)[:self.MAX_RESULTADOS]

        self.lista.delete(0, tk.END)

        if not resultados:
            self._ocultar_lista()
            return

        for dep in resultados:
            self.lista.insert(tk.END, dep)

        self.lista.config(height=len(resultados))
        self.lista.pack(fill="x", pady=(3, 0))

    def _seleccionar_primero(self):
        if self.lista.size() > 0:
            self.lista.selection_clear(0, tk.END)
            self.lista.selection_set(0)
            self._seleccionar()
            return "break"

    def _seleccionar(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            return

        valor = self.lista.get(seleccion[0])
        self.var_buscar.set(valor)
        self.variable.set(valor)
        self._ocultar_lista()

        if self.on_select:
            self.on_select(valor)

    def _ocultar_lista(self):
        self.lista.pack_forget()


# ── Aplicación principal ───────────────────────────────────────────────────────
class InventarioApp:

    AUTO_FIELDS = [(c, e) for c, _, e in CAMPOS_AUTO]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sistema de Inventario — Municipalidad de Chillán")
        self.root.geometry("1200x900")
        self.root.minsize(1020, 740)
        self.root.configure(bg=C["gris_bg"])

        try:
            icon = tk.PhotoImage(file=ICON_PATH)
            self.root.iconphoto(True, icon)
        except Exception:
            pass

        # Estado interno
        self.fecha_hora_envio       = ""
        self.var_fecha_hora_visible = tk.StringVar()
        self.datos_auto             = {}
        self.discos_fisicos         = []
        self.monitores_detectados   = []
        self.monitores_vars         = []
        self.impresoras_vars        = []
        self.auto_entries           = {}
        self.discos_widgets         = []
        self.discos_entries         = []

        # Variables de formulario
        self.var_usuario             = tk.StringVar()
        self.var_registrado_por      = tk.StringVar()
        self.var_ubicacion           = tk.StringVar()
        self.var_departamento_manual = tk.StringVar()

        self._configurar_estilo()
        self._construir_interfaz()
        self._cargar_datos_automaticos()

    # ── Estilos ────────────────────────────────────────────────────────────────
    def _configurar_estilo(self) -> None:
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except Exception:
            pass

        s.configure(".", background=C["gris_bg"], foreground=C["texto"],
                    font=("Segoe UI", 10))
        s.configure("TFrame",  background=C["gris_bg"])
        s.configure("TLabel",  background=C["gris_bg"], foreground=C["texto"])

        s.configure("Section.TLabelframe",
                    background=C["gris_panel"], bordercolor=C["gris_borde"],
                    relief="solid", borderwidth=1)
        s.configure("Section.TLabelframe.Label",
                    background=C["gris_bg"], foreground=C["rojo"],
                    font=("Segoe UI", 10, "bold"))

        s.configure("TEntry",
                    fieldbackground=C["gris_panel"],
                    bordercolor=C["gris_borde"], padding=6)

        s.configure("Primary.TButton",
                    font=("Segoe UI", 10, "bold"), padding=(22, 9),
                    background=C["rojo"], foreground="white", borderwidth=0)
        s.map("Primary.TButton",
              background=[("active", C["rojo_hover"]), ("pressed", C["rojo_dark"])],
              foreground=[("active", "white")])

        s.configure("TButton", font=("Segoe UI", 9), padding=(10, 4),
                    background="#eaeff6", bordercolor=C["gris_borde"])
        s.map("TButton", background=[("active", "#d8e2ef")])

        s.configure("Small.TButton", font=("Segoe UI", 8), padding=(6, 3),
                    background="#eaeff6", bordercolor=C["gris_borde"])
        s.map("Small.TButton", background=[("active", "#d8e2ef")])

        s.configure("Danger.TButton", font=("Segoe UI", 10), padding=(22, 9),
                    background=C["rojo_light"], foreground=C["rojo"], borderwidth=0)
        s.map("Danger.TButton", background=[("active", "#f9cdd4")])

        s.configure("Edit.TButton", font=("Segoe UI", 8), padding=(5, 3),
                    background=C["badge_bg"], foreground=C["badge_fg"], borderwidth=0)
        s.map("Edit.TButton",
              background=[("active", "#dde7ff")],
              foreground=[("active", C["azul_acento"])])

        s.configure("Vertical.TScrollbar",
                    background=C["gris_bg"], troughcolor=C["sombra"],
                    bordercolor=C["gris_bg"], arrowsize=12)

    # ── Interfaz con scroll ────────────────────────────────────────────────────
    def _construir_interfaz(self) -> None:
        outer  = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, highlightthickness=0, bg=C["gris_bg"])
        sb     = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)

        self.scroll_frame = ttk.Frame(canvas, padding=20)
        self.scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        win_id = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfigure(win_id, width=e.width))
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._build_header()

        cuerpo = ttk.Frame(self.scroll_frame)
        cuerpo.pack(fill="both", expand=True)

        izq = ttk.Frame(cuerpo)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 10))
        der = ttk.Frame(cuerpo)
        der.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self._build_auto_frame(izq)
        self._build_monitores_frame(izq)
        self._build_trazabilidad_frame(der)
        self._build_manual_frame(der)
        self._build_impresoras_frame(der)
        self._build_observaciones_frame(der)
        self._build_acciones_frame(der)

    # ── Header institucional ───────────────────────────────────────────────────
    def _build_header(self) -> None:
        header = tk.Frame(self.scroll_frame, bg=C["rojo"], bd=0)
        header.pack(fill="x", pady=(0, 22))
        tk.Frame(header, bg=C["rojo_dark"], height=4).pack(fill="x")

        inner = tk.Frame(header, bg=C["rojo"], padx=20, pady=16)
        inner.pack(fill="x")

        banner_loaded = False
        try:
            banner_img = tk.PhotoImage(file=BANNER_PATH)
            w = banner_img.width()
            if w > 260:
                banner_img = banner_img.subsample(max(1, round(w / 260)))
            lbl = tk.Label(inner, image=banner_img, bg=C["rojo"], bd=0)
            lbl.image = banner_img
            lbl.pack(side="left", padx=(0, 20))
            banner_loaded = True
        except Exception:
            pass

        if not banner_loaded:
            tk.Label(inner, text="Municipalidad de Chillán",
                     bg=C["rojo"], fg=C["blanco"],
                     font=("Segoe UI", 18, "bold")).pack(side="left")

        tk.Frame(inner, bg="#e8849a", width=1).pack(side="left", fill="y", padx=(0, 20))

        txt = tk.Frame(inner, bg=C["rojo"])
        txt.pack(side="left", fill="y")
        tk.Label(txt, text="Sistema de Inventario de Equipos",
                 bg=C["rojo"], fg="#ffe5ea",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(txt, text="Registro y seguimiento de activos tecnológicos municipales",
                 bg=C["rojo"], fg="#ffd6de",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))

    # ── Helper: sección card ───────────────────────────────────────────────────
    def _seccion(self, parent, titulo, *, fill="x", expand=False,
                 pady=(0, 14)) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=f"  {titulo}",
                               style="Section.TLabelframe", padding=10)
        frame.pack(fill=fill, expand=expand, pady=pady)
        return frame

    # ── Helper: fila etiqueta + entry ─────────────────────────────────────────
    def _campo(self, parent, texto: str, variable: tk.StringVar,
               fila: int, width: int = 30, readonly: bool = False) -> ttk.Entry:
        ttk.Label(parent, text=texto, foreground=C["label_claro"],
                  font=("Segoe UI", 9)).grid(
            row=fila, column=0, sticky="w", padx=(10, 6), pady=5)
        entry = ttk.Entry(parent, textvariable=variable, width=width,
                          state="readonly" if readonly else "normal")
        entry.grid(row=fila, column=1, sticky="ew", padx=(0, 10), pady=5)
        parent.columnconfigure(1, weight=1)
        return entry

    # ── Helper: campo ubicación editable ──────────────────────────────────────
    def _campo_ubicacion(self, parent, fila: int) -> ttk.Entry:
        ttk.Label(parent, text="Ubicación:", foreground=C["label_claro"],
                  font=("Segoe UI", 9)).grid(
            row=fila, column=0, sticky="w", padx=(10, 6), pady=5)

        inner = ttk.Frame(parent)
        inner.grid(row=fila, column=1, sticky="ew", padx=(0, 10), pady=5)
        inner.columnconfigure(0, weight=1)

        entry = ttk.Entry(inner, textvariable=self.var_ubicacion, state="readonly")
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ttk.Button(inner, text="✎ Editar", style="Small.TButton",
                   command=lambda: self._habilitar_grupo_generico([entry])
                   ).grid(row=0, column=1)
        return entry

    # ── Sección: datos automáticos ────────────────────────────────────────────
    def _build_auto_frame(self, parent) -> None:
        frame = self._seccion(parent, "Datos detectados automáticamente",
                              fill="both", expand=False)
        self.auto_frame = frame

        for fila, (clave, texto) in enumerate(self.AUTO_FIELDS):
            ttk.Label(frame, text=f"{texto}:", foreground=C["gris_sub"],
                      font=("Segoe UI", 9)).grid(
                row=fila, column=0, sticky="w", padx=(10, 6), pady=4)
            var   = tk.StringVar(value="Cargando…")
            entry = ttk.Entry(frame, textvariable=var, width=34, state="readonly")
            entry.grid(row=fila, column=1, sticky="ew", padx=(0, 10), pady=4)
            self.auto_entries[clave] = {"var": var, "entry": entry}

        self.fila_discos_inicio = len(self.AUTO_FIELDS)

        ttk.Button(frame, text="✎ Editar", style="Small.TButton",
                   command=self._editar_bloque_automatico).grid(
            row=0, column=2, rowspan=max(1, len(self.AUTO_FIELDS)),
            padx=(4, 8), pady=4, sticky="n")
        frame.columnconfigure(1, weight=1)

    def _editar_bloque_automatico(self) -> None:
        entries = [i["entry"] for i in self.auto_entries.values()] + self.discos_entries
        self._habilitar_grupo_generico(entries)

    def _habilitar_grupo_generico(self, entries: list) -> None:
        for e in entries:
            e.config(state="normal")
        if entries:
            entries[0].focus_set()
            entries[0].icursor("end")

        def revisar(_=None):
            def bloquear():
                if self.root.focus_get() not in entries:
                    for e in entries:
                        e.config(state="readonly")
            self.root.after_idle(bloquear)

        for e in entries:
            e.unbind("<FocusOut>")
            e.unbind("<Return>")
            e.bind("<FocusOut>", revisar, add="+")
            e.bind("<Return>",   revisar, add="+")

    # ── Sección: trazabilidad ─────────────────────────────────────────────────
    def _build_trazabilidad_frame(self, parent) -> None:
        frame = self._seccion(parent, "Trazabilidad del registro")

        ttk.Label(frame, text="Fecha y hora:", foreground=C["gris_sub"],
                  font=("Segoe UI", 9)).grid(
            row=0, column=0, sticky="w", padx=(10, 6), pady=5)

        reloj = tk.Frame(frame, bg=C["gris_panel"])
        reloj.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=5)
        tk.Label(reloj, text="●", bg=C["gris_panel"], fg=C["rojo"],
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        tk.Label(reloj, textvariable=self.var_fecha_hora_visible,
                 bg=C["gris_panel"], fg=C["rojo"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")

        self._campo(frame, "Registrado por:", self.var_registrado_por, 1, width=28)
        frame.columnconfigure(1, weight=1)
        self._actualizar_reloj()

    # ── Sección: datos manuales con dropdown inline ───────────────────────────
    def _build_manual_frame(self, parent) -> None:
        frame = self._seccion(parent, "Datos del equipo y ubicación")

        self._campo(frame, "Funcionario responsable:", self.var_usuario, 0)
        
        # Etiqueta departamento
        ttk.Label(frame, text="Departamento / dirección:", foreground=C["label_claro"],
                  font=("Segoe UI", 9)).grid(
            row=1, column=0, sticky="nw", padx=(10, 6), pady=5)

        # Dropdown buscable inline
        self.buscador_departamento = BuscadorDepartamento(
            frame,
            opciones=list(DEPARTAMENTOS_UBICACION.keys()),
            variable=self.var_departamento_manual,
            on_select=self._on_departamento_seleccionado,
        )
        self.buscador_departamento.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 10),
            pady=5,
        )
        
        self._campo_ubicacion(frame, 2)
        frame.columnconfigure(1, weight=1)
        
    def _on_departamento_seleccionado(self, departamento: str) -> None:
        if not departamento:
            self.var_ubicacion.set("")
            return

        self.var_ubicacion.set(
            DEPARTAMENTOS_UBICACION.get(departamento.strip(), "")
        )


    # ── Sección: monitores ────────────────────────────────────────────────────
    def _build_monitores_frame(self, parent) -> None:
        frame = self._seccion(parent, "Monitores asociados")
        ttk.Button(frame, text="＋ Agregar monitor", style="Small.TButton",
                   command=self._crear_bloque_monitor).pack(
            anchor="w", padx=10, pady=(4, 4))
        self.monitores_container = ttk.Frame(frame)
        self.monitores_container.pack(fill="x", padx=10, pady=(0, 6))

    # ── Sección: impresoras ───────────────────────────────────────────────────
    def _build_impresoras_frame(self, parent) -> None:
        frame = self._seccion(parent, "Impresoras asociadas")
        ttk.Button(frame, text="＋ Agregar impresora", style="Small.TButton",
                   command=self._crear_bloque_impresora).pack(
            anchor="w", padx=10, pady=(4, 4))
        self.impresoras_container = ttk.Frame(frame)
        self.impresoras_container.pack(fill="x", padx=10, pady=(0, 6))

    # ── Sección: observaciones ────────────────────────────────────────────────
    def _build_observaciones_frame(self, parent) -> None:
        frame = self._seccion(parent, "Observaciones", fill="both", expand=True)
        self.txt_observaciones = ScrolledText(
            frame, height=5, wrap="word",
            font=("Segoe UI", 10), relief="solid", borderwidth=1,
            background=C["gris_panel"], highlightthickness=0,
        )
        self.txt_observaciones.pack(fill="both", expand=True, padx=10, pady=8)

    # ── Sección: acciones ─────────────────────────────────────────────────────
    def _build_acciones_frame(self, parent) -> None:
        tk.Frame(parent, bg=C["gris_borde"], height=1).pack(fill="x", pady=(10, 16))
        row = ttk.Frame(parent)
        row.pack(fill="x")
        ttk.Button(row, text="  Registrar equipo  ", style="Primary.TButton",
                   command=self.enviar_datos).pack(side="left")
        ttk.Button(row, text="Cancelar", style="Danger.TButton",
                   command=self.root.destroy).pack(side="right")
        self.lbl_estado = ttk.Label(parent, text="● Estado: listo",
                                    foreground=C["gris_sub"], font=("Segoe UI", 9))
        self.lbl_estado.pack(fill="x", pady=(10, 0))

    # ── Discos en panel automático ────────────────────────────────────────────
    def _mostrar_discos_en_auto_frame(self) -> None:
        for w in self.discos_widgets:
            w.destroy()
        self.discos_widgets.clear()
        self.discos_entries.clear()

        for i, disco in enumerate(self.discos_fisicos):
            tipo      = str(disco.get("tipo", "") or "Disco").strip()
            capacidad = formatear_capacidad(str(disco.get("capacidad", "") or "").strip())
            if not capacidad:
                continue
            disco["capacidad"] = capacidad
            fila = self.fila_discos_inicio + i
            lbl  = ttk.Label(self.auto_frame, text=f"{tipo}:",
                             foreground=C["gris_sub"], font=("Segoe UI", 9))
            lbl.grid(row=fila, column=0, sticky="w", padx=(10, 6), pady=4)
            entry = ttk.Entry(self.auto_frame, width=34, state="normal")
            entry.insert(0, capacidad)
            entry.config(state="readonly")
            entry.grid(row=fila, column=1, sticky="ew", padx=(0, 10), pady=4)
            self.discos_widgets.extend([lbl, entry])
            self.discos_entries.append(entry)

    # ── Bloques dinámicos monitor / impresora ─────────────────────────────────
    def _crear_bloque(self, container, lista: list, titulo: str,
                      campos: list, renumerar, datos: dict = None) -> None:
        datos = datos or {}
        frame = ttk.LabelFrame(container, text=f"  {titulo} {len(lista) + 1}",
                               style="Section.TLabelframe")
        frame.pack(fill="x", pady=5)

        vars_   = {k: tk.StringVar(value=str(datos.get(k, "")).lower())
                   for k, _ in campos}
        entries = {k: self._campo(frame, lbl, vars_[k], i, width=22, readonly=True)
                   for i, (k, lbl) in enumerate(campos)}

        btns = ttk.Frame(frame)
        btns.grid(row=0, column=2, rowspan=len(campos), padx=(4, 8), pady=4, sticky="n")
        ttk.Button(btns, text="✎ Editar", style="Small.TButton",
                   command=lambda e=entries: self._habilitar_grupo(e)).pack(pady=(0, 4))
        ttk.Button(btns, text="✕ Quitar", style="Small.TButton",
                   command=lambda f=frame: self._quitar_bloque(f, lista, renumerar)
                   ).pack()

        lista.append({"frame": frame, "entries": entries, **vars_})

    def _quitar_bloque(self, frame, lista: list, renumerar) -> None:
        if len(lista) == 1:
            return
        lista[:] = [i for i in lista if i["frame"] != frame]
        frame.destroy()
        renumerar()

    def _crear_bloque_monitor(self, datos: dict = None) -> None:
        self._crear_bloque(self.monitores_container, self.monitores_vars,
                           "Monitor", CAMPOS_MONITOR,
                           self._renumerar_monitores, datos)

    def _crear_bloque_impresora(self, datos: dict = None) -> None:
        self._crear_bloque(self.impresoras_container, self.impresoras_vars,
                           "Impresora", CAMPOS_IMPRESORA,
                           self._renumerar_impresoras, datos)

    def _renumerar_monitores(self) -> None:
        for i, item in enumerate(self.monitores_vars, 1):
            item["frame"].configure(text=f"  Monitor {i}")

    def _renumerar_impresoras(self) -> None:
        for i, item in enumerate(self.impresoras_vars, 1):
            item["frame"].configure(text=f"  Impresora {i}")

    def _habilitar_grupo(self, entries: dict) -> None:
        lista = list(entries.values())
        for e in lista:
            e.config(state="normal")
        if lista:
            lista[0].focus_set()
            lista[0].icursor("end")

        def revisar(_=None):
            def bloquear():
                if self.root.focus_get() not in lista:
                    for e in lista:
                        e.config(state="readonly")
            self.root.after_idle(bloquear)

        for e in lista:
            e.unbind("<FocusOut>")
            e.unbind("<Return>")
            e.bind("<FocusOut>", revisar, add="+")
            e.bind("<Return>",   revisar, add="+")

    # ── Reloj ─────────────────────────────────────────────────────────────────
    def _actualizar_reloj(self) -> None:
        self.var_fecha_hora_visible.set(datetime.now().strftime("%Y-%m-%d   %H:%M:%S"))
        self.root.after(1000, self._actualizar_reloj)

    def _get_auto(self, clave: str) -> str:
        item = self.auto_entries.get(clave)
        return item["var"].get().strip() if item else ""

    def _clean(self, var: tk.StringVar) -> str:
        return var.get().strip().lower()

    # ── Carga automática ───────────────────────────────────────────────────────
    def _cargar_datos_automaticos(self) -> None:
        self._set_estado("Cargando datos automáticos…", C["gris_sub"])
        self.root.update_idletasks()
        errores = []

        try:
            admin()
        except Exception as e:
            errores.append(f"admin(): {e}")

        for clave, fn, _ in CAMPOS_AUTO:
            try:
                valor = fn()
            except Exception as e:
                valor = "ERROR"
                errores.append(f"{clave}: {e}")

            if clave == "ram":
                valor = formatear_capacidad(valor)

            self.datos_auto[clave] = valor
            self.auto_entries[clave]["var"].set(str(valor))

        try:
            obtener_ruta_smart()
            self.discos_fisicos = obtener_discos_smart()
        except Exception as e:
            self.discos_fisicos = []
            errores.append(f"discos_smart: {e}")

        try:
            self.monitores_detectados = obtener_monitores()
        except Exception as e:
            self.monitores_detectados = []
            errores.append(f"monitores: {e}")

        self._mostrar_discos_en_auto_frame()

        for m in self.monitores_detectados:
            self._crear_bloque_monitor(m)
        if not self.monitores_vars:
            self._crear_bloque_monitor()

        try:
            impresoras = obtener_impresoras_activas()
        except Exception as e:
            impresoras = []
            errores.append(f"impresoras: {e}")

        for imp in impresoras:
            self._crear_bloque_impresora(imp)
        if not self.impresoras_vars:
            self._crear_bloque_impresora({"tipo": "no detectada"})

        if errores:
            self._set_estado("● Carga parcial con errores", C["amarillo"])
            messagebox.showwarning("Carga parcial",
                "La ventana abrió, pero algunos datos automáticos fallaron:\n\n"
                + "\n".join(errores))
        else:
            self._set_estado("● Datos automáticos cargados ✓", C["verde"])

    # ── Payload ────────────────────────────────────────────────────────────────
    def construir_payload(self) -> dict:
        monitores = [
            {k: item[k].get().strip().lower() for k in ("marca", "modelo", "pulgadas")}
            for item in self.monitores_vars
        ]
        impresoras = [
            {k: item[k].get().strip().lower() for k in ("tipo", "marca", "modelo", "ip", "toner_tinta")}
            for item in self.impresoras_vars
        ]

        return {
            **{c: self._get_auto(c) for c, _ in self.AUTO_FIELDS},
            "usuario":             self._clean(self.var_usuario),
            "registrado_por":      self._clean(self.var_registrado_por),
            "fecha_hora_registro": self.fecha_hora_envio
                                   or datetime.now().strftime("%Y-%m-%d %H:%M"),
            "discos":              self.discos_fisicos,
            "codigo_inventario":   None,
            "ubicacion":           self._clean(self.var_ubicacion),
            "departamento_manual": self._clean(self.var_departamento_manual),
            "monitores":           monitores,
            "impresoras":          impresoras,
            "observaciones":       self.txt_observaciones.get("1.0", "end").strip().lower() or None,
        }

    # ── Validación ─────────────────────────────────────────────────────────────
    def validar_payload(self, payload: dict) -> bool:
        faltantes = [nombre for clave, nombre in OBLIGATORIOS.items()
                     if not payload.get(clave)]
        if not payload.get("fecha_hora_registro"):
            faltantes.append("Fecha y hora")
        if faltantes:
            messagebox.showwarning("Faltan datos",
                "Completa estos campos obligatorios:\n\n— " +
                "\n— ".join(faltantes))
            return False
        return True

    def _set_estado(self, texto: str, color: str) -> None:
        self.lbl_estado.config(text=texto, foreground=color)

    # ── Envío ──────────────────────────────────────────────────────────────────
    def enviar_datos(self) -> None:
        self.fecha_hora_envio = datetime.now().strftime("%Y-%m-%d %H:%M")
        payload = self.construir_payload()
        if not self.validar_payload(payload):
            return
        if not messagebox.askyesno("Confirmar registro",
                                   "¿Confirmas el envío de este inventario?"):
            return

        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                url = f.read().strip()
        except Exception as e:
            messagebox.showerror("Error de configuración",
                                 f"No se encontró config.txt\n\n{e}")
            return

        self._set_estado("● Enviando datos…", C["rojo"])
        self.root.update_idletasks()

        try:
            resp = requests.post(url, json=payload,
                                 headers={"ngrok-skip-browser-warning": "true"},
                                 timeout=60)
            try:
                rj = resp.json()
            except Exception:
                ruta = guardar_respaldo(payload, "RESPUESTA_NO_JSON", resp.text)
                messagebox.showerror("Respuesta inválida",
                    f"El servidor no devolvió JSON válido.\n\nRespaldo en:\n{ruta}")
                self._set_estado("● Error — respuesta no JSON", C["rojo"])
                return

            if rj.get("success") is True:
                messagebox.showinfo("Registro exitoso",
                    f"Equipo registrado correctamente.\n\n{rj.get('message', '')}")
                self._set_estado("● Registrado correctamente ✓", C["verde"])
            else:
                ruta = guardar_respaldo(payload, "ERROR_SERVIDOR", resp.text)
                messagebox.showerror("Error del servidor",
                    f"Motivo: {rj.get('message', 'Sin mensaje')}\n\nRespaldo:\n{ruta}")
                self._set_estado("● Error del servidor", C["rojo"])

        except requests.exceptions.RequestException as e:
            ruta = guardar_respaldo(payload, "ERROR_ENVIO", str(e))
            messagebox.showerror("Error de conexión",
                f"No se pudo conectar con el servidor.\n\n{e}\n\nRespaldo:\n{ruta}")
            self._set_estado("● Sin conexión", C["rojo"])


# ── Punto de entrada ───────────────────────────────────────────────────────────
def main() -> None:
    try:
        root = tk.Tk()
        InventarioApp(root)
        root.mainloop()
    except Exception:
        import traceback
        print("ERROR AL INICIAR:\n", traceback.format_exc())
        input("Presiona ENTER para salir...")


if __name__ == "__main__":
    main()