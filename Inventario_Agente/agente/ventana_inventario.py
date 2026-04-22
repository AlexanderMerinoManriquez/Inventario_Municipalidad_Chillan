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
from funciones.permisos import admin
from funciones.ram import obtener_ram
from funciones.serial import obtener_serial
from funciones.sistema_operativo import obtener_sistema
from funciones.uuid import obtener_uuid

# ── Rutas ──────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH   = os.path.join(BASE_DIR, "config.txt")
RESPALDOS_DIR = os.path.join(BASE_DIR, "RESPALDOS_FALLIDOS")

# ── Campos automáticos: (clave, función, etiqueta) ────────────────────────────
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

# ── Paleta de colores ──────────────────────────────────────────────────────────
PALETA = {
    "bg":             "#f0f2f5",
    "panel":          "#ffffff",
    "borde":          "#ced4da",
    "primario":       "#1a56db",
    "primario_hover": "#1048b8",
    "peligro":        "#c0392b",
    "texto":          "#1a1d23",
    "texto_sub":      "#6b7280",
    "acento":         "#e8f0fe",
}

# ── Definición de bloques dinámicos ───────────────────────────────────────────
CAMPOS_MONITOR    = [("marca", "Marca:"), ("modelo", "Modelo:"), ("pulgadas", "Pulgadas:")]
CAMPOS_IMPRESORA  = [("tipo", "Tipo:"), ("marca", "Marca:"), ("modelo", "Modelo:"),
                     ("ip", "IP:"), ("toner_tinta", "Toner/tinta:")]

# ── Campos obligatorios para validación ───────────────────────────────────────
OBLIGATORIOS = {
    "usuario":             "Funcionario responsable",
    "registrado_por":      "Registrado por",
    "ubicacion":           "Ubicación",
    "departamento_manual": "Departamento / dirección",
}


# ── Utilidad: respaldo local ───────────────────────────────────────────────────
def guardar_respaldo(data: dict, estado: str, respuesta: str = "") -> str:
    try:
        os.makedirs(RESPALDOS_DIR, exist_ok=True)
        ts     = datetime.now()
        nombre = str(data.get("nombre_pc", "sin_nombre")).replace(" ", "_")
        ruta   = os.path.join(RESPALDOS_DIR, f"ERROR_{ts:%Y%m%d_%H%M%S}_{nombre}.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(
                {"fecha": ts.strftime("%Y-%m-%d %H:%M:%S"), "estado": estado,
                 "respuesta_servidor": respuesta, "datos_equipo": data},
                f, ensure_ascii=False, indent=4,
            )
        return ruta
    except Exception as e:
        return f"ERROR_AL_CREAR_RESPALDO: {e}"


# ── Aplicación principal ───────────────────────────────────────────────────────
class InventarioApp:

    AUTO_FIELDS = [(c, e) for c, _, e in CAMPOS_AUTO]   # (clave, etiqueta)

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sistema de Inventario — Municipalidad de Chillán")
        self.root.geometry("1140x860")
        self.root.minsize(1000, 740)

        self.fecha_hora_envio       = ""
        self.var_fecha_hora_visible = tk.StringVar()
        self.datos_auto             = {}
        self.discos_fisicos         = []
        self.monitores_detectados   = []
        self.monitores_vars         = []
        self.impresoras_vars        = []
        self.auto_entries           = {}
        self.discos_widgets         = []

        self.var_usuario             = tk.StringVar()
        self.var_registrado_por      = tk.StringVar()
        self.var_ubicacion           = tk.StringVar()
        self.var_departamento_manual = tk.StringVar()

        self._configurar_estilo()
        self._construir_interfaz()
        self._cargar_datos_automaticos()

    # ── Estilos ────────────────────────────────────────────────────────────────
    def _configurar_estilo(self) -> None:
        p = PALETA
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except Exception:
            pass

        self.root.configure(bg=p["bg"])

        # Fuente base
        s.configure(".", background=p["bg"], foreground=p["texto"], font=("Segoe UI", 10))
        s.configure("TFrame",  background=p["bg"])
        s.configure("TLabel",  background=p["bg"], foreground=p["texto"])

        # Encabezado
        s.configure("Title.TLabel",    background=p["bg"], foreground=p["texto"],
                    font=("Segoe UI", 17, "bold"))
        s.configure("Subtitle.TLabel", background=p["bg"], foreground=p["texto_sub"],
                    font=("Segoe UI", 10))

        # Tarjetas / secciones
        s.configure("Section.TLabelframe",
                    background=p["panel"], bordercolor=p["borde"],
                    relief="solid", borderwidth=1)
        s.configure("Section.TLabelframe.Label",
                    background=p["bg"], foreground=p["texto"],
                    font=("Segoe UI", 10, "bold"))

        # Campos de texto
        s.configure("TEntry", fieldbackground=p["panel"],
                    bordercolor=p["borde"], padding=4)

        # Botón primario (Registrar)
        s.configure("Primary.TButton",
                    font=("Segoe UI", 10, "bold"), padding=(12, 5),
                    background=p["primario"], foreground="white", borderwidth=0)
        s.map("Primary.TButton",
              background=[("active", p["primario_hover"])],
              foreground=[("active", "white")])

        # Botón normal
        s.configure("TButton", font=("Segoe UI", 9), padding=(8, 3),
                    background="#e2e8f0", bordercolor=p["borde"])
        s.map("TButton", background=[("active", "#cbd5e1")])

        # Botón pequeño (Editar / Quitar)
        s.configure("Small.TButton", font=("Segoe UI", 8), padding=(5, 2),
                    background="#e2e8f0", bordercolor=p["borde"])
        s.map("Small.TButton", background=[("active", "#cbd5e1")])

        # Botón peligro (Cancelar)
        s.configure("Danger.TButton", font=("Segoe UI", 9), padding=(8, 3),
                    background="#fee2e2", foreground=p["peligro"], borderwidth=0)
        s.map("Danger.TButton", background=[("active", "#fecaca")])

        # Treeview
        s.configure("Treeview", background=p["panel"], fieldbackground=p["panel"],
                    foreground=p["texto"], rowheight=26, font=("Segoe UI", 9))
        s.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                    background=p["acento"], foreground=p["primario"])
        s.map("Treeview", background=[("selected", p["acento"])],
              foreground=[("selected", p["primario"])])

        # Scrollbar
        s.configure("Vertical.TScrollbar", background=p["bg"],
                    troughcolor=p["bg"], bordercolor=p["bg"])

    # ── Interfaz principal (con scroll) ───────────────────────────────────────
    def _construir_interfaz(self) -> None:
        contenedor = ttk.Frame(self.root)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, highlightthickness=0, bg=PALETA["bg"])
        sb     = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)

        self.scroll_frame = ttk.Frame(canvas, padding=16)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._win_id = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfigure(self._win_id, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Encabezado con franja de color
        header_wrap = tk.Frame(self.scroll_frame, bg=PALETA["primario"])
        header_wrap.pack(fill="x", pady=(0, 16))
        tk.Label(header_wrap, text="  Sistema de Inventario",
                 bg=PALETA["primario"], fg="white",
                 font=("Segoe UI", 17, "bold"), pady=10).pack(side="left")
        tk.Label(header_wrap, text="Municipalidad de Chillán  ",
                 bg=PALETA["primario"], fg="#93c5fd",
                 font=("Segoe UI", 10)).pack(side="right", anchor="s", pady=12)

        # Dos columnas
        cuerpo = ttk.Frame(self.scroll_frame)
        cuerpo.pack(fill="both", expand=True)

        izq = ttk.Frame(cuerpo)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 8))
        der = ttk.Frame(cuerpo)
        der.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self._build_auto_frame(izq)
        self._build_monitores_frame(izq)
        self._build_trazabilidad_frame(der)
        self._build_manual_frame(der)
        self._build_impresoras_frame(der)
        self._build_observaciones_frame(der)
        self._build_acciones_frame(der)

    # ── Helper: crear sección (LabelFrame) ────────────────────────────────────
    def _seccion(self, parent, titulo, *, fill="x", expand=False, pady=(0, 12)) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=titulo, style="Section.TLabelframe")
        frame.pack(fill=fill, expand=expand, pady=pady)
        return frame

    # ── Helper: fila etiqueta + entry ─────────────────────────────────────────
    def _campo(self, parent, texto: str, variable: tk.StringVar,
               fila: int, width: int = 30, readonly: bool = False) -> ttk.Entry:
        ttk.Label(parent, text=texto).grid(
            row=fila, column=0, sticky="w", padx=10, pady=5)
        state = "readonly" if readonly else "normal"
        entry = ttk.Entry(parent, textvariable=variable, width=width, state=state)
        entry.grid(row=fila, column=1, sticky="ew", padx=10, pady=5)
        parent.columnconfigure(1, weight=1)
        return entry

    # ── Secciones de la interfaz ───────────────────────────────────────────────
    def _build_auto_frame(self, parent) -> None:
        frame = self._seccion(parent, "Datos detectados automáticamente",
                              fill="both", expand=False)
        self.auto_frame = frame

        for fila, (clave, texto) in enumerate(self.AUTO_FIELDS):
            ttk.Label(frame, text=f"{texto}:").grid(
                row=fila, column=0, sticky="w", padx=10, pady=4)
            var   = tk.StringVar(value="Cargando…")
            entry = ttk.Entry(frame, textvariable=var, width=34, state="readonly")
            entry.grid(row=fila, column=1, sticky="ew", padx=10, pady=4)
            ttk.Button(frame, text="Editar", style="Small.TButton",
                       command=lambda e=entry: self._habilitar_entry(e)
                       ).grid(row=fila, column=2, padx=(4, 8), pady=4)
            self.auto_entries[clave] = {"var": var, "entry": entry}

        frame.columnconfigure(1, weight=1)
        self.fila_discos_inicio = len(self.AUTO_FIELDS)

    def _build_trazabilidad_frame(self, parent) -> None:
        frame = self._seccion(parent, "Trazabilidad")
        ttk.Label(frame, text="Fecha y hora:").grid(
            row=0, column=0, sticky="w", padx=10, pady=6)
        ttk.Label(frame, textvariable=self.var_fecha_hora_visible,
                  foreground=PALETA["primario"], font=("Segoe UI", 10, "bold")
                  ).grid(row=0, column=1, sticky="w", padx=10, pady=6)
        self._campo(frame, "Registrado por:", self.var_registrado_por, 1, width=28)
        self._actualizar_reloj()

    def _build_manual_frame(self, parent) -> None:
        frame = self._seccion(parent, "Datos manuales principales")
        self._campo(frame, "Funcionario responsable:", self.var_usuario, 0)
        self._campo(frame, "Ubicación:",               self.var_ubicacion, 1)
        self._campo(frame, "Departamento/dirección:",  self.var_departamento_manual, 2)

    def _build_monitores_frame(self, parent) -> None:
        frame = self._seccion(parent, "Monitores asociados")
        ttk.Button(frame, text="＋ Agregar monitor", style="Small.TButton",
                   command=self._crear_bloque_monitor).pack(anchor="w", padx=10, pady=8)
        self.monitores_container = ttk.Frame(frame)
        self.monitores_container.pack(fill="x", padx=10, pady=(0, 8))

    def _build_impresoras_frame(self, parent) -> None:
        frame = self._seccion(parent, "Impresoras asociadas")
        ttk.Button(frame, text="＋ Agregar impresora", style="Small.TButton",
                   command=self._crear_bloque_impresora).pack(anchor="w", padx=10, pady=8)
        self.impresoras_container = ttk.Frame(frame)
        self.impresoras_container.pack(fill="x", padx=10, pady=(0, 8))

    def _build_observaciones_frame(self, parent) -> None:
        frame = self._seccion(parent, "Observaciones", fill="both", expand=True)
        self.txt_observaciones = ScrolledText(
            frame, height=7, wrap="word", font=("Segoe UI", 10),
            relief="flat", borderwidth=0, background=PALETA["panel"])
        self.txt_observaciones.pack(fill="both", expand=True, padx=10, pady=8)

    def _build_acciones_frame(self, parent) -> None:
        sep = tk.Frame(parent, bg=PALETA["borde"], height=1)
        sep.pack(fill="x", pady=(8, 10))

        frame = ttk.Frame(parent)
        frame.pack(fill="x")

        ttk.Button(frame, text="Ver resumen",
                   command=self.mostrar_resumen).pack(side="left", padx=(0, 6))
        ttk.Button(frame, text="Registrar", style="Primary.TButton",
                   command=self.enviar_datos).pack(side="left")
        ttk.Button(frame, text="Cancelar", style="Danger.TButton",
                   command=self.root.destroy).pack(side="right")

        self.lbl_estado = ttk.Label(parent, text="Estado: listo",
                                    foreground=PALETA["texto_sub"],
                                    font=("Segoe UI", 9))
        self.lbl_estado.pack(fill="x", pady=(10, 0))

    # ── Helpers de edición ─────────────────────────────────────────────────────
    def _actualizar_reloj(self) -> None:
        self.var_fecha_hora_visible.set(datetime.now().strftime("%Y-%m-%d  %H:%M"))
        self.root.after(1000, self._actualizar_reloj)

    def _habilitar_entry(self, entry: ttk.Entry) -> None:
        """Habilita un entry de solo lectura y lo bloquea al perder el foco."""
        entry.config(state="normal")
        entry.focus_set()
        def _bloquear(_=None):
            entry.config(state="readonly")
        entry.unbind("<FocusOut>")
        entry.unbind("<Return>")
        entry.bind("<FocusOut>", _bloquear, add="+")
        entry.bind("<Return>",   _bloquear, add="+")

    def _habilitar_grupo(self, entries: dict) -> None:
        """Habilita un grupo de entries (bloque monitor/impresora)."""
        lista = list(entries.values())
        for e in lista:
            e.config(state="normal")
        if lista:
            lista[0].focus_set()

        def _revisar(_=None):
            def _bloquear_si_salio():
                if self.root.focus_get() not in lista:
                    for e in lista:
                        e.config(state="readonly")
            self.root.after_idle(_bloquear_si_salio)

        for e in lista:
            e.unbind("<FocusOut>")
            e.unbind("<Return>")
            e.bind("<FocusOut>", _revisar, add="+")
            e.bind("<Return>",   _revisar, add="+")

    def _get_auto(self, clave: str) -> str:
        item = self.auto_entries.get(clave)
        return item["var"].get().strip() if item else ""

    # ── Discos en el panel automático ─────────────────────────────────────────
    def _mostrar_discos_en_auto_frame(self) -> None:
        for w in self.discos_widgets:
            w.destroy()
        self.discos_widgets.clear()

        for fila_offset, disco in enumerate(self.discos_fisicos):
            tipo     = str(disco.get("tipo", "") or "Disco").strip()
            capacidad = str(disco.get("capacidad", "") or "").strip()
            if not capacidad:
                continue

            fila = self.fila_discos_inicio + fila_offset
            lbl  = ttk.Label(self.auto_frame, text=f"{tipo}:")
            lbl.grid(row=fila, column=0, sticky="w", padx=10, pady=4)

            entry = ttk.Entry(self.auto_frame, width=34, state="normal")
            entry.insert(0, capacidad)
            entry.config(state="readonly")
            entry.grid(row=fila, column=1, sticky="ew", padx=10, pady=4)

            btn = ttk.Button(self.auto_frame, text="Editar", style="Small.TButton",
                             command=lambda e=entry: self._habilitar_entry(e))
            btn.grid(row=fila, column=2, padx=(4, 8), pady=4)

            self.discos_widgets.extend([lbl, entry, btn])

    # ── Bloques dinámicos genérico ─────────────────────────────────────────────
    def _quitar_bloque(self, frame, lista: list, renumerar) -> None:
        if len(lista) == 1:
            return
        lista[:] = [item for item in lista if item["frame"] != frame]
        frame.destroy()
        renumerar()

    def _crear_bloque(self, container, lista: list, titulo: str,
                      campos: list, renumerar, datos: dict = None,
                      readonly: bool = False) -> None:
        datos = datos or {}
        frame = ttk.LabelFrame(container, text=f"{titulo} {len(lista) + 1}",
                               style="Section.TLabelframe")
        frame.pack(fill="x", pady=6)

        vars_   = {k: tk.StringVar(value=str(datos.get(k, "")).lower()) for k, _ in campos}
        entries = {k: self._campo(frame, lbl, vars_[k], i, width=22, readonly=readonly)
                   for i, (k, lbl) in enumerate(campos)}

        # Botones en columna 2
        btn_row = 0
        if readonly:
            ttk.Button(frame, text="Editar", style="Small.TButton",
                       command=lambda e=entries: self._habilitar_grupo(e)
                       ).grid(row=btn_row, column=2, padx=(4, 8), pady=4)
            btn_row += 1

        ttk.Button(frame, text="Quitar", style="Small.TButton",
                   command=lambda f=frame: self._quitar_bloque(f, lista, renumerar)
                   ).grid(row=btn_row, column=2, padx=(4, 8), pady=4)

        lista.append({"frame": frame, "entries": entries, **vars_})

    def _crear_bloque_monitor(self, datos: dict = None) -> None:
        self._crear_bloque(self.monitores_container, self.monitores_vars,
                           "Monitor", CAMPOS_MONITOR,
                           self._renumerar_monitores, datos, readonly=True)

    def _crear_bloque_impresora(self, datos: dict = None) -> None:
        self._crear_bloque(self.impresoras_container, self.impresoras_vars,
                           "Impresora", CAMPOS_IMPRESORA,
                           self._renumerar_impresoras, datos, readonly=False)

    def _renumerar_monitores(self) -> None:
        for i, item in enumerate(self.monitores_vars, 1):
            item["frame"].configure(text=f"Monitor {i}")

    def _renumerar_impresoras(self) -> None:
        for i, item in enumerate(self.impresoras_vars, 1):
            item["frame"].configure(text=f"Impresora {i}")

    # ── Carga automática ───────────────────────────────────────────────────────
    def _cargar_datos_automaticos(self) -> None:
        self.lbl_estado.config(text="Estado: cargando datos automáticos…",
                               foreground=PALETA["texto_sub"])
        self.root.update_idletasks()
        errores = []

        try:
            admin()
        except Exception as e:
            errores.append(f"admin(): {e}")

        for clave, fn, _ in CAMPOS_AUTO:
            try:
                self.datos_auto[clave] = fn()
            except Exception as e:
                self.datos_auto[clave] = "ERROR"
                errores.append(f"{clave}: {e}")
            self.auto_entries[clave]["var"].set(str(self.datos_auto[clave]))

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
        if not self.impresoras_vars:
            self._crear_bloque_impresora()

        if errores:
            self.lbl_estado.config(text="Estado: carga parcial con errores",
                                   foreground="#d97706")
            messagebox.showwarning("Carga parcial",
                "La ventana abrió, pero algunos datos automáticos fallaron:\n\n"
                + "\n".join(errores))
        else:
            self.lbl_estado.config(text="Estado: datos automáticos cargados ✓",
                                   foreground="#16a34a")

    # ── Payload ────────────────────────────────────────────────────────────────
    def construir_payload(self) -> dict:
        obs = self.txt_observaciones.get("1.0", "end").strip().lower() or None
        monitores  = [{k: item[k].get().strip().lower()
                       for k in ("marca", "modelo", "pulgadas")}
                      for item in self.monitores_vars]
        impresoras = [{k: item[k].get().strip().lower()
                       for k in ("tipo", "marca", "modelo", "ip", "toner_tinta")}
                      for item in self.impresoras_vars]
        return {
            **{c: self._get_auto(c) for c, _ in self.AUTO_FIELDS},
            "usuario":             self.var_usuario.get().strip().lower(),
            "registrado_por":      self.var_registrado_por.get().strip().lower(),
            "fecha_hora_registro": self.fecha_hora_envio
                                   or datetime.now().strftime("%Y-%m-%d %H:%M"),
            "discos":              self.discos_fisicos,
            "codigo_inventario":   None,
            "ubicacion":           self.var_ubicacion.get().strip().lower(),
            "departamento_manual": self.var_departamento_manual.get().strip().lower(),
            "monitores":           monitores,
            "impresoras":          impresoras,
            "observaciones":       obs,
        }

    # ── Validación ─────────────────────────────────────────────────────────────
    def validar_payload(self, payload: dict) -> bool:
        faltantes = [nombre for clave, nombre in OBLIGATORIOS.items()
                     if not payload.get(clave)]

        if not any(m.get("marca") or m.get("modelo") or m.get("pulgadas")
                   for m in payload["monitores"]):
            faltantes.append("Al menos un monitor con datos")

        if not any(i.get("tipo") or i.get("marca") or i.get("modelo")
                   for i in payload["impresoras"]):
            faltantes.append("Al menos una impresora con datos")

        if faltantes:
            messagebox.showwarning("Faltan datos",
                "Completa estos campos obligatorios:\n\n- " + "\n- ".join(faltantes))
            return False
        return True

    # ── Resumen ────────────────────────────────────────────────────────────────
    def mostrar_resumen(self) -> None:
        payload = self.construir_payload()
        if not self.validar_payload(payload):
            return
        win = tk.Toplevel(self.root)
        win.title("Resumen del inventario")
        win.geometry("780x640")
        win.configure(bg=PALETA["bg"])
        txt = ScrolledText(win, wrap="word", font=("Consolas", 10),
                           background=PALETA["panel"], relief="flat")
        txt.pack(fill="both", expand=True, padx=12, pady=12)
        txt.insert("1.0", json.dumps(payload, indent=4, ensure_ascii=False))
        txt.config(state="disabled")

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
            url = open(CONFIG_PATH, encoding="utf-8").read().strip()
        except Exception as e:
            messagebox.showerror("Error de configuración",
                                 f"No se encontró config.txt\n\n{e}")
            return

        self.lbl_estado.config(text="Estado: enviando datos…",
                               foreground=PALETA["primario"])
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
                    f"El servidor no devolvió JSON válido.\n\nRespaldo guardado en:\n{ruta}")
                self.lbl_estado.config(text="Estado: error — respuesta no JSON",
                                       foreground=PALETA["peligro"])
                return

            if rj.get("success") is True:
                messagebox.showinfo("Registro exitoso",
                    f"El equipo fue registrado correctamente.\n\n{rj.get('message', '')}")
                self.lbl_estado.config(text="Estado: registrado correctamente ✓",
                                       foreground="#16a34a")
            else:
                ruta = guardar_respaldo(payload, "ERROR_SERVIDOR", resp.text)
                messagebox.showerror("Error del servidor",
                    f"Motivo: {rj.get('message', 'Sin mensaje')}\n\nRespaldo:\n{ruta}")
                self.lbl_estado.config(text="Estado: error del servidor",
                                       foreground=PALETA["peligro"])

        except requests.exceptions.RequestException as e:
            ruta = guardar_respaldo(payload, "ERROR_ENVIO", str(e))
            messagebox.showerror("Error de conexión",
                f"No se pudo conectar con el servidor.\n\n{e}\n\nRespaldo:\n{ruta}")
            self.lbl_estado.config(text="Estado: sin conexión",
                                   foreground=PALETA["peligro"])


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