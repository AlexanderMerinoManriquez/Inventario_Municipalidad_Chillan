Primeros pasos del proyecto:

* Ejecutar en la consola el comando "Python -m venv venv" (Sirve para la creacion del entorno virtual en la carpeta raiz de lo que se ejecutara,
lo más recomendable en este proyecto es crear un entorno virtual en cada uno "Inventario_Agente" y "Inventario_AgenteWeb".)

* Activar el entorno virtual que en el caso de vscode con la consola de powershell es cosa de dirigirse a la ruta "../.venv\Scripts\activate.bat" 
(Teniendo en cuenta que esta dentro de las ruta de cada aplicacion hablada anteriormente, repetir el proceso por cada una.)

* En este punto la consola deberia salir algo como "(.venv) ../rutacorrespondiente:". En este punto solo queda estar en la misma ruta que el archivo
"requirements.txt" y escribir en la consola "pip install -r requirements.tx.t"

* Datos en caso de algun error con "pip install". Es raro pero hay algunos casos de conflictos con la version de python o pip instalado a pesar de
estar en el entorno virtal ya activado, en este es mejor instlar en el equipo propio las versiones de python correspondientes y luego por consola
instalar pip para luego volver a intentar, tratar de verificar siempre las librerias instaladas dentro de ".venv" para evitar cualquier inconveniente.

* Tener en cuenta que esto esta hecho en un servidor local y en "laragon 6.0", si se desea hacer con un servidor propio solo modificar los datos pertinentes en config.

* El proyecto ocupa "Smartctl.exe" como dependencia para poder sacar algunas especificaciones tecnicas de los discos duros.

* El proyecto al estar de forma local para pequeñas pruebas se hizo las pruebas a mayor escala utilizando "ngrok" como lan virtual compartiendo la carpeta
del proyecto y abriendo los puertos pertinentes, en el caso de seguir utilizando lo mismo solo modificar el archivo "C:\laragon\www\Inventario_Agente\agente\inventario.py"
fila 68 para poder enviar de forma correcta a la url que te derivo ngrok en tu computadora.

* Los .bat del inicio son solo para facilitar el trabajo, ya que es cosa de abrirlos de forma manual simplemente.

* En el caso de querer subir los datos a la BDD solo ejecutar por primera vez el archivo "inventario.py" de la carpeta "Inventario_AgenteWeb" ya que,
en este se crean las tablas pertinentes y se insertan datos. El "inventario.py" de la carpeta "Inventario_Agente" solo hace inserciones, cosa de solo ejecutarlo
en otros equipos y no tener tanta informacion, solo enviarla.

* En caso de querer crear un ejecutable siempre tener en la misma carpeta "Smartctl.exe" para asi evitar algun error.

* Recordar que al crear el ejecutable es recomendable ejecutar los comando dentro mismo entorno virtual para asi evitar errores.

----------------------------------------------- DATOS PENSADOS PARA EJECUTARSE A FUTURO -------------------------------------------------------------------

* Se desea en una proxima actualizacion hacer que funcione en segundo plano cosa que cada 6 horas o el plazo de tiempo que el admin guste haga una consulta el agente a
la web en el caso de ser positivo se hara automaticamente la actualizacion de datos. (Esto se tiene pensado para cualquier cambio que haya con el equipo, tanto IP como otro
de los campos que tiene este script.)

* Se debe implementar una nueva columna de la columna perifericos en BDD para luego hacer la insercion como "JSON" en un campo txt en la BDD tal y como se hizo con el campo
discos y sus detalles. El modulo de impresoras por el momento solo esta de bonito, botones funcionales y buena interfaz pero sin un funcionamiento real. 