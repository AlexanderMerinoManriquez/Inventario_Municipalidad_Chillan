import os
import sys
import shutil

def obtener_ruta_smart():

    # 🟢 PRIORIDAD: junto al ejecutable
    ruta_exe = os.path.join(os.path.dirname(sys.executable), "smartctl.exe")
    if os.path.exists(ruta_exe):
        return ruta_exe

    # 🟡 Desarrollo (ruta relativa)
    ruta_local = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "herramientas", "smartctl.exe")
    )
    if os.path.exists(ruta_local):
        return ruta_local

    # 🔵 Sistema
    ruta_path = shutil.which("smartctl")
    if ruta_path:
        return ruta_path

    print("❌ smartctl no encontrado en ninguna ruta")
    return None