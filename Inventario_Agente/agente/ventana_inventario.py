import socket
import requests
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from funciones.permisos import admin
from funciones.grupo_trabajo import obtener_grupo_trabajo
from funciones.sistema_operativo import obtener_sistema
from funciones.anydesk import obtener_anydesk
from funciones.cpu import obtener_cpu
from funciones.ram import obtener_ram
from funciones.ip import obtener_ip
from funciones.uuid import obtener_uuid
from funciones.serial import obtener_serial
from funciones.discos.disco import obtener_disco_principal
from funciones.discos.main import obtener_discos_smart
from funciones.discos.utils import obtener_ruta_smart


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.txt")
RESPALDOS_DIR = os.path.join(BASE_DIR, "RESPALDOS_FALLIDOS")


def guardar_respaldo(data, estado, respuesta=""):
    try:
        os.makedirs(RESPALDOS_DIR, exist_ok=True)

        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        fecha_legible = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nombre_pc = str(data.get("nombre_pc", "sin_nombre")).replace(" ", "_")

        nombre_archivo = f"ERROR_{fecha_archivo}_{nombre_pc}.json"
        ruta_respaldo = os.path.join(RESPALDOS_DIR, nombre_archivo)

        contenido = {
            "fecha": fecha_legible,
            "estado": estado,
            "respuesta_servidor": respuesta,
            "datos_equipo": data,
        }

        with open(ruta_respaldo, "w", encoding="utf-8") as f:
            json.dump(contenido, f, ensure_ascii=False, indent=4)

        return ruta_respaldo
    except Exception as e:
        return f"ERROR_AL_CREAR_RESPALDO: {e}"


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario")
        self.root.geometry("980x760")
        self.root.minsize(900, 680)

        self.datos_auto = {}
        self.discos_fisicos = []

        self.var_usuario = tk.StringVar()
        self.var_ubicacion = tk.StringVar()
        self.var_departamento_manual = tk.StringVar()
        self.var_marca_pantalla = tk.StringVar()
        self.var_modelo_pantalla = tk.StringVar()
        self.var_pulgadas_pantalla = tk.StringVar()

        self.var_tipo_impresora = tk.StringVar()
        self.var_marca_impresora = tk.StringVar()
        self.var_modelo_impresora = tk.StringVar()
        self.var_toner_tinta = tk.StringVar()
        self.var_ip_impresora = tk.StringVar()

        self._configurar_estilo()
        self._construir_interfaz()
        self._cargar_datos_automaticos()

    def _configurar_estilo(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _construir_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=12)
        contenedor.pack(fill="both", expand=True)

        header = ttk.Frame(contenedor)
        header.pack(fill="x", pady=(0, 10))

        ttk.Label(header, text="Inventario", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="sistema de invetario",
            style="Subtitle.TLabel",
        ).pack(anchor="w")

        cuerpo = ttk.Frame(contenedor)
        cuerpo.pack(fill="both", expand=True)

        izquierda = ttk.Frame(cuerpo)
        izquierda.pack(side="left", fill="both", expand=True, padx=(0, 6))

        derecha = ttk.Frame(cuerpo)
        derecha.pack(side="left", fill="both", expand=True, padx=(6, 0))

        auto_frame = ttk.LabelFrame(
            izquierda,
            text="Datos detectados automáticamente",
            style="Section.TLabelframe",
        )
        auto_frame.pack(fill="x", pady=(0, 10))

        self.labels_auto = {}
        campos_auto = [
            ("nombre_pc", "Nombre PC"),
            ("departamento", "Departamento PC"),
            ("sistema_operativo", "Sistema operativo"),
            ("anydesk", "Anydesk"),
            ("cpu", "Procesador"),
            ("ram", "RAM"),
            ("disco_total", "Disco total"),
            ("ip", "IP"),
            ("uuid", "UUID"),
            ("serial", "N°Serie"),
        ]

        for fila, (clave, texto) in enumerate(campos_auto):
            ttk.Label(auto_frame, text=f"{texto}:").grid(
                row=fila, column=0, sticky="w", padx=8, pady=4
            )
            lbl = ttk.Label(auto_frame, text="Cargando...", wraplength=320)
            lbl.grid(row=fila, column=1, sticky="w", padx=8, pady=4)
            self.labels_auto[clave] = lbl

        auto_frame.columnconfigure(1, weight=1)

        discos_frame = ttk.LabelFrame(
            izquierda,
            text="Discos detectados",
            style="Section.TLabelframe",
        )
        discos_frame.pack(fill="both", expand=True)

        columnas = ("modelo", "capacidad", "tipo", "salud", "temperatura")
        self.tree_discos = ttk.Treeview(
            discos_frame, columns=columnas, show="headings", height=9
        )
        for col in columnas:
            self.tree_discos.heading(col, text=col.capitalize())
            self.tree_discos.column(col, width=120, anchor="w")
        self.tree_discos.pack(fill="both", expand=True, padx=8, pady=8)

        manual_frame = ttk.LabelFrame(
            derecha,
            text="Datos manuales",
            style="Section.TLabelframe",
        )
        manual_frame.pack(fill="x", pady=(0, 10))

        self._crear_campo(manual_frame, "Funcionario:", self.var_usuario, 0)
        self._crear_campo(manual_frame, "Ubicación:", self.var_ubicacion, 1)
        self._crear_campo(
            manual_frame, "Departamento de trabajo:", self.var_departamento_manual, 2
        )
        self._crear_campo(manual_frame, "Marca pantalla:", self.var_marca_pantalla, 3)
        self._crear_campo(manual_frame, "Modelo pantalla:", self.var_modelo_pantalla, 4)
        self._crear_campo(
            manual_frame, "Pulgadas pantalla:", self.var_pulgadas_pantalla, 5
        )

        impresora_frame = ttk.LabelFrame(
            derecha,
            text="Datos de impresora",
            style="Section.TLabelframe",
        )
        impresora_frame.pack(fill="x", pady=(0, 10))

        self._crear_campo(
            impresora_frame, "Tipo impresora:", self.var_tipo_impresora, 0
        )
        self._crear_campo(
            impresora_frame, "Marca impresora:", self.var_marca_impresora, 1
        )
        self._crear_campo(
            impresora_frame, "Modelo impresora:", self.var_modelo_impresora, 2
        )
        self._crear_campo(
            impresora_frame, "Toner / tinta:", self.var_toner_tinta, 3
        )
        self._crear_campo(
            impresora_frame, "IP impresora:", self.var_ip_impresora, 4
        )

        obs_frame = ttk.LabelFrame(
            derecha,
            text="Observaciones",
            style="Section.TLabelframe",
        )
        obs_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.txt_observaciones = ScrolledText(
            obs_frame, height=8, wrap="word", font=("Segoe UI", 10)
        )
        self.txt_observaciones.pack(fill="both", expand=True, padx=8, pady=8)

        acciones = ttk.Frame(derecha)
        acciones.pack(fill="x")

        ttk.Button(acciones, text="Ver resumen", command=self.mostrar_resumen).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(acciones, text="Enviar", command=self.enviar_datos).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(acciones, text="Salir", command=self.root.destroy).pack(side="right")

        self.lbl_estado = ttk.Label(derecha, text="Estado: listo", anchor="w")
        self.lbl_estado.pack(fill="x", pady=(10, 0))

    def _crear_campo(self, parent, texto, variable, fila):
        ttk.Label(parent, text=texto).grid(
            row=fila, column=0, sticky="w", padx=8, pady=6
        )
        entry = ttk.Entry(parent, textvariable=variable, width=40)
        entry.grid(row=fila, column=1, sticky="ew", padx=8, pady=6)
        parent.columnconfigure(1, weight=1)
        return entry

    def _cargar_datos_automaticos(self):
        self.lbl_estado.config(text="Estado: cargando datos automáticos...")
        self.root.update_idletasks()

        errores = []
        self.datos_auto = {}

        try:
            admin()
        except Exception as e:
            errores.append(f"admin(): {e}")

        try:
            self.datos_auto["nombre_pc"] = socket.gethostname()
        except Exception as e:
            self.datos_auto["nombre_pc"] = "ERROR"
            errores.append(f"socket.gethostname(): {e}")

        try:
            self.datos_auto["departamento"] = obtener_grupo_trabajo()
        except Exception as e:
            self.datos_auto["departamento"] = "ERROR"
            errores.append(f"obtener_grupo_trabajo(): {e}")

        try:
            self.datos_auto["sistema_operativo"] = obtener_sistema()
        except Exception as e:
            self.datos_auto["sistema_operativo"] = "ERROR"
            errores.append(f"obtener_sistema(): {e}")

        try:
            self.datos_auto["anydesk"] = obtener_anydesk()
        except Exception as e:
            self.datos_auto["anydesk"] = "ERROR"
            errores.append(f"obtener_anydesk(): {e}")

        try:
            self.datos_auto["cpu"] = obtener_cpu()
        except Exception as e:
            self.datos_auto["cpu"] = "ERROR"
            errores.append(f"obtener_cpu(): {e}")

        try:
            self.datos_auto["ram"] = obtener_ram()
        except Exception as e:
            self.datos_auto["ram"] = "ERROR"
            errores.append(f"obtener_ram(): {e}")

        try:
            self.datos_auto["disco_total"] = obtener_disco_principal()
        except Exception as e:
            self.datos_auto["disco_total"] = "ERROR"
            errores.append(f"obtener_disco_principal(): {e}")

        try:
            self.datos_auto["ip"] = obtener_ip()
        except Exception as e:
            self.datos_auto["ip"] = "ERROR"
            errores.append(f"obtener_ip(): {e}")

        try:
            self.datos_auto["uuid"] = obtener_uuid()
        except Exception as e:
            self.datos_auto["uuid"] = "ERROR"
            errores.append(f"obtener_uuid(): {e}")

        try:
            self.datos_auto["serial"] = obtener_serial()
        except Exception as e:
            self.datos_auto["serial"] = "ERROR"
            errores.append(f"obtener_serial(): {e}")

        try:
            _ = obtener_ruta_smart()
            self.discos_fisicos = obtener_discos_smart()
        except Exception as e:
            self.discos_fisicos = []
            errores.append(f"obtener_discos_smart()/obtener_ruta_smart(): {e}")

        for clave, valor in self.datos_auto.items():
            if clave in self.labels_auto:
                self.labels_auto[clave].config(text=str(valor))

        for item in self.tree_discos.get_children():
            self.tree_discos.delete(item)

        for disco in self.discos_fisicos:
            self.tree_discos.insert(
                "",
                "end",
                values=(
                    disco.get("modelo", ""),
                    disco.get("capacidad", ""),
                    disco.get("tipo", ""),
                    disco.get("salud", ""),
                    disco.get("temperatura", ""),
                ),
            )

        if errores:
            self.lbl_estado.config(text="Estado: carga parcial con errores")
            messagebox.showwarning(
                "Carga parcial",
                "La ventana abrió, pero algunos datos automáticos fallaron:\n\n"
                + "\n".join(errores),
            )
        else:
            self.lbl_estado.config(text="Estado: datos automáticos cargados")

    def construir_payload(self):
        observaciones = self.txt_observaciones.get("1.0", "end").strip().lower()
        if observaciones == "":
            observaciones = None

        return {
            **self.datos_auto,
            "usuario": self.var_usuario.get().strip().lower(),
            "discos": self.discos_fisicos,
            "codigo_inventario": None,
            "ubicacion": self.var_ubicacion.get().strip().lower(),
            "departamento_manual": self.var_departamento_manual.get().strip().lower(),
            "marca_pantalla": self.var_marca_pantalla.get().strip().lower(),
            "modelo_pantalla": self.var_modelo_pantalla.get().strip().lower(),
            "pulgadas_pantalla": self.var_pulgadas_pantalla.get().strip().lower(),
            "tipo_impresora": self.var_tipo_impresora.get().strip().lower() or None,
            "marca_impresora": self.var_marca_impresora.get().strip().lower() or None,
            "modelo_impresora": self.var_modelo_impresora.get().strip().lower() or None,
            "toner_tinta": self.var_toner_tinta.get().strip().lower() or None,
            "ip_impresora": self.var_ip_impresora.get().strip().lower() or None,
            "observaciones": observaciones,
        }

    def validar_payload(self, payload):
        obligatorios = {
            "usuario": "Funcionario",
            "ubicacion": "Ubicación",
            "departamento_manual": "Departamento del dispositivo",
            "marca_pantalla": "Marca de pantalla",
            "modelo_pantalla": "Modelo de pantalla",
            "pulgadas_pantalla": "Pulgadas de pantalla",
        }

        faltantes = [
            nombre for clave, nombre in obligatorios.items() if not payload.get(clave)
        ]
        if faltantes:
            messagebox.showwarning(
                "Faltan datos",
                "Completa estos campos obligatorios:\n\n- " + "\n- ".join(faltantes),
            )
            return False

        return True

    def mostrar_resumen(self):
        payload = self.construir_payload()
        if not self.validar_payload(payload):
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Resumen del inventario")
        ventana.geometry("760x620")

        txt = ScrolledText(ventana, wrap="word", font=("Consolas", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("1.0", json.dumps(payload, indent=4, ensure_ascii=False))
        txt.config(state="disabled")

    def enviar_datos(self):
        payload = self.construir_payload()
        if not self.validar_payload(payload):
            return

        confirmar = messagebox.askyesno(
            "Confirmar envío",
            "¿Deseas enviar este inventario a la base de datos?",
        )
        if not confirmar:
            return

        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                url = f.read().strip()
        except Exception as e:
            messagebox.showerror("Error", f"No se encontró config.txt\n\nDetalle: {e}")
            return

        self.lbl_estado.config(text="Estado: enviando datos...")
        self.root.update_idletasks()

        try:
            respuesta = requests.post(
                url,
                json=payload,
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=60,
            )

            try:
                respuesta_json = respuesta.json()
            except Exception:
                ruta = guardar_respaldo(payload, "RESPUESTA_NO_JSON", respuesta.text)
                messagebox.showerror(
                    "Respuesta inválida",
                    f"El servidor respondió, pero no devolvió JSON válido.\n\nRespaldo: {ruta}",
                )
                self.lbl_estado.config(text="Estado: error, respuesta no JSON")
                return

            if respuesta_json.get("success") is True:
                messagebox.showinfo(
                    "Éxito",
                    f"Registro guardado correctamente.\n\nMensaje: {respuesta_json.get('message', 'Sin mensaje')}",
                )
                self.lbl_estado.config(text="Estado: guardado correctamente")
            else:
                ruta = guardar_respaldo(payload, "ERROR_SERVIDOR", respuesta.text)
                messagebox.showerror(
                    "No se guardó",
                    f"El servidor respondió, pero no guardó el registro.\n\nMotivo: {respuesta_json.get('message', 'Sin mensaje')}\n\nRespaldo: {ruta}",
                )
                self.lbl_estado.config(text="Estado: error de servidor")

        except requests.exceptions.RequestException as e:
            ruta = guardar_respaldo(payload, "ERROR_ENVIO", str(e))
            messagebox.showerror(
                "Error de envío",
                f"No se pudo enviar el registro.\n\nDetalle: {e}\n\nRespaldo: {ruta}",
            )
            self.lbl_estado.config(text="Estado: fallo de envío")


def main():
    try:
        root = tk.Tk()
        app = InventarioApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print("ERROR AL INICIAR LA VENTANA:")
        print(traceback.format_exc())
        input("Presiona ENTER para salir...")


if __name__ == "__main__":
    main()