import subprocess
import json
import math

def _limpiar_texto_wmi(lista):
    if not lista:
        return: ""
    try:
        return "".join(chr(x) for x in lista if x != 0).strip()
    except Exception:
        return ""
    
def calcular_porcentaje(ancho_cm, alto_cm):
    try:
        ancho = float(ancho_cm)
        alto = float(alto_cm)
        if ancho <= 0 or alto <= 0:
            return ""
        diagonal_cm = math.sqrt((ancho_cm ** 2) + (alto_cm ** 2))
        return round(diagonal_cm / 2.54, 1)
    except Exception:
        return ""
    
def obtener_monitores():
    """
    
    devuelve una lista de monitores detectados en windows.
    Intenta obtener:
    -fabricante
    -nombre/modelo
    -serial
    -pulgadas aproximadas
    """
    
    script = r´´´{
        $ids = Get-CimInstance -namespace root\wmi -Classname WmiMonitorID
        $params = Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams
        
        $resultado = @()
        
        foreach ($m in $ids) {
            $param = $params | Where-Object { $_.InstanceName -eq $m.InstanceName } | Select-Object -First 1
            
            $obj = [PSCustomObject] @{
                InstanceName = $m.InstanceName
                ManuFacturerName = $m.ManufacturerName
                UserFriendlyName = $m.UserFriendlyName
                SerialNumberID = $m.SerialNumberID
                MaximunHorizontalImageSize = if ($param) { $param.MaxHorizontalImageSize } else {0}
                MaximunVerticalImageSize = if ($param) { $param.MaxVerticalImageSize } else {0}   
        }
            
            $resultado += $obj
    }
        
        $resultado | ConvertTo-Json -Depth 3
        ´´´
        
    try:
        proceso = subprocess.run(
            ["powerShell", "-Noprofile", "ExecutionPolicy", "Bypass", "-Command", script],
            capture_output=True,
            text=True,
            timeout=20
            
        )
        if proceso.returncode != 0:
            return[]
            
        salida = proceso.stdout.strip()
        if not salida:
            return[]
            
        datos = json.loads(salida)
        
        if isinstance(datos, dict):
            datos = [datos]
            
        monitores = []
        
        for item in datos:
            fabricante = limpiar_texto_wmi(item.get("ManufacturerName", []))
            modelo = _limpiar_texto_wmi(item.get("UserFriendlyName", []))
            serial = _limpiar_texto_wmi(item.get("SerialNumberID", []))
            
            ancho_cm = item.get("MaxHorizontalImageSize", 0) or 0
            alto_cm = 
    