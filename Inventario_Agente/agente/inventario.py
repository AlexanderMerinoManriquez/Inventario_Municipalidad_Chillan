import socket
import requests
import json
import os
from datetime import datetime

from funciones.permisos import admin
from funciones.usuario import pedir_nombre_completo
from funciones.grupo_trabajo import obtener_grupo_trabajo
from funciones.sistema_operativo import obtener_sistema
from funciones.anydesk import obtener_anydesk
from funciones.cpu import obtener_cpu
from funciones.ram import obtener_ram
from funciones.ip import obtener_ip
from funciones.uuid import obtener_uuid
from funciones.serial import obtener_serial
from funciones.discos.disco  import obtener_disco_principal
from funciones.discos.main import obtener_discos_smart
from funciones.discos.utils import obtener_ruta_smart

def guardar_respaldo(data, estado, respuesta=""):
    try:
        carpeta = os.path.join(os.path.dirname(__file__),"RESPALDOS_FALLIDOS")
        os.makedirs(carpeta, exist_ok=True)
        
        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        fecha_legible = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nombre_pc = str(data.get("nombre_pc", "sin_nombre")).replace(" ", "_")
        
        nombre_archivo = F"ERROR_{fecha_archivo}_{nombre_pc}.txt"
        ruta_respaldo = os.path.join(carpeta, nombre_archivo)
        
        contenido = {
            "fecha": fecha_legible,
            "estado": estado,
            "datos_equipo": data
        }
        
        with open (ruta_respaldo, "w", encoding="utf-8") as f:
            json.dump(contenido, f, ensure_ascii=False, indent=4)
            
        print("\n" + "=" * 60)
        print(" NO SE PUDO GUARDAR EN LA BASE DE DATOS")
        print(f"    RESPALDO CREADO: {ruta_respaldo}")
        print("LOS DATOS DEL EQUIPO FUERON GUARDADOS LOCALMENTE")
        print("-" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR AL INTENTAR CREAR EL RESPALDO LOCAL")
        print("detalle:", e)
        print("-" * 60)

admin()

nombre_pc = socket.gethostname()

usuario = pedir_nombre_completo()
usuario_str = f"{usuario['nombre']} {usuario['apellido1']} {usuario['apellido2']}"

departamento = obtener_grupo_trabajo()

sistema = obtener_sistema()

anydesk = obtener_anydesk()
print("anydesk:", anydesk)

cpu = obtener_cpu()

ram = obtener_ram()

disco_principal = obtener_disco_principal()

ip = obtener_ip()

uuid = obtener_uuid()

serial = obtener_serial()

discos_fisicos = obtener_discos_smart()

print("Discos detectados:", discos_fisicos)

ruta = obtener_ruta_smart()
print("Ruta SMART:", ruta)
print("Preparando datos manuales...")

while True:
    ubicacion = input("Ubicacion del dispositivo:   ").strip().lower()
    if ubicacion:
        break
    print("La ubicacion es obligatoria.")
    
while True:
    departamento_manual = input("departamento del dispositivo:  ").strip().lower()
    if departamento_manual:
        break
    print("El departamento del dispositivo es obligatorio.")
    
while True:
    marca_pantalla = input("Marca de la pantalla: ").strip().lower()
    if marca_pantalla:
        break
    print("La marca de la pantalla debe ser obligatoria.")
    
while True:
    modelo_pantalla = input("Modelo de la pantalla: ").strip().lower()
    if modelo_pantalla:
        break
    print("El modelo de la pantalla es obligatorio.")
    
while True:
    pulgadas_pantalla = input("Pulgadas de la pantalla: ").strip().lower()
    if pulgadas_pantalla:
        break
    print("Las pulgadas de la pantalla son obligatorio.")

    
tipo_impresora = input("Tipo de la impresora (scanner, multifuncional, plotter): ").strip().lower()
marca_impresora = input("Marca de la impresora: ").strip().lower()
modelo_impresora = input("Modelo de la impresora: ").strip().lower()
toner_tinta = input("Toner / tinta de la impresora: ").strip().lower()
ip_impresora = input("IP imprespra: ").strip().lower()
observaciones = input("Observaciones finales: ").strip().lower()
if observaciones == "":
    observaciones = None
    
    
    
data = {
    "nombre_pc": nombre_pc,
    "usuario": usuario_str,
    "departamento": departamento,
    "sistema_operativo": sistema,
    "anydesk": anydesk,
    "cpu": cpu,
    "ram": ram,
    "disco_total": disco_principal,
    "ip": ip,
    "uuid": uuid,
    "serial": serial,
    "discos": discos_fisicos,
    "codigo_inventario": None,
    
    "ubicacion": ubicacion,
    "departamento_manual": departamento_manual,
    
    "marca_pantalla": marca_pantalla,
    "modelo_pantalla": modelo_pantalla,
    "pulgadas_pantalla": pulgadas_pantalla,
    
    "tipo_impresora": tipo_impresora,
    "marca_impresora": marca_impresora,
    "modelo_impresora": modelo_impresora,
    "toner_tinta": toner_tinta,
    "ip_impresora": ip_impresora,
    
    "observaciones": observaciones
}

print("\n===== RESUMEN DEL INVENTARIO =====")
print("Nombre PC:", data.get("nombre_pc", ""))
print("Usuario:", data.get("usuario", ""))
print("Departamento:", data.get("departamento", ""))
print("Sistema operativo:", data.get("sistema_operativo", ""))
print("Anydesk:", data.get("anydesk", ""))
print("CPU:", data.get("cpu", ""))
print("RAM:", data.get("ram", ""))
print("Disco total:", data.get("disco_total", ""))
print("IP:", data.get("ip", ""))
print("UUID:", data.get("uuid", ""))
print("Serial:", data.get("serial", ""))
print("Ubicacion:", data.get("ubicacion", ""))
print("Departamento manual:", data.get("departamento_manual", ""))
print("Marca pantalla:", data.get("marca_pantalla", ""))
print("Modelo pantalla", data.get("modelo_pantalla", ""))
print("Pulgadas_pantalla", data.get("pulgadas_pantalla"))
print("tipo_impresora", data.get("tipo_impresora"))
print("marca_impresora", data.get("marca_impresora"))
print("modelo_impresora", data.get("modelo_impresora"))
print("toner_tinta", data.get("toner_tinta"))
print("ip_impresora", data.get("ip_impresora"))
print("Observaciones:", data.get("observaciones", ""))

print("\nDiscos detectados:")
if data.get("discos"):
    for i, disco in enumerate(data["discos"], start=1):
        print(f"\nDisco {i}:")
        print("  Modelo:", disco.get("modelo", ""))
        print("  Capacidad:", disco.get("capacidad", ""))
        print("  Espacio libre GB:", disco.get("espacio_libre_gb", ""))
        print("  Tipo:", disco.get("tipo", ""))
        print("  Salud:", disco.get("salud", ""))
        print("  Horas:", disco.get("horas", ""))
        print("  Errores:", disco.get("errores", ""))
        print("  Temperatura:", disco.get("temperatura", ""))
    
else:
    print("  No se detectaron discos.")

print("\n===============================")

faltantes = []
for clave, valor in data.items():
    if clave == "discos":
        continue
    if valor in [None, "", "SIN_DEFINIR", "SIN_UUID", "SIN_SERIAL"]:
        faltantes.append(clave)
        
if faltantes:
    print("\n  Campos que podrian faltar o venirr incompletos:")
    for campo in faltantes:
        print("-", campo)
        
confirmar = input("\n¿Confirmas que estos datos son correctos y deseas enviarlos? (S/N): ").strip().lower()

if confirmar != "s":
    print("Envio cancelado por el usuario.")
    input("\nPresiona ENTER para cerrar....")
    exit()

try:
    with open("config.txt", "r", encoding="utf-8") as f:
        url = f.read().strip()
except Exception as e:
    print("Error: no se encontró config.txt")
    print("Detalle:", e)
    input("Presiona ENTER para salir...")
    exit()

print("\nURL destino:", url)
print("\n===== JSON A ENVIAR =====")
print(json.dumps(data, indent=4, ensure_ascii=False))
print("=========================")

try:
    respuesta = requests.post(
        url,
        json=data,
        headers={"ngrok-skip-browser-warning": "true"},
        timeout=60,
    )

    print("\nCódigo HTTP:", respuesta.status_code)
    print("Servidor:", respuesta.text)

    try:
        respuesta_json = respuesta.json()

        if respuesta_json.get("success") is True:
            print("\n El registro llegó correctamente a la base de datos.")
            print("Mensaje:", respuesta_json.get("message", "Sin mensaje"))
        else:
            print("\n El servidor respondió, pero NO guardó el registro.")
            print("Motivo:", respuesta_json.get("message", "Sin mensaje"))
            guardar_respaldo(data, "ERROR_SERVIDOR", respuesta.text)

    except Exception:
        print("\n El servidor respondió, pero no devolvió un JSON válido.")
        guardar_respaldo(data, "RESPUESTA_NO_JSON", respuesta.text)

except requests.exceptions.RequestException as e:
    print("\n Error enviando datos:", e)
    guardar_respaldo(data, "ERROR_ENVIO", str(e))

input("\nPresiona ENTER para cerrar...")