# README (LÉEME)

<p>
Universidad Simón Bolívar.<br>
Trimestre Abril-Julio 2022.<br>
Asignatura: Redes Definidas por Software.<br>
Profesora: Emma Di Battista.<br>
Alumno: César A. Pineda Carrero.<br>
Carnet: 15-11136.
</p>

# Práctica II de la asignatura Redes Definidas por Software (SDN).

# Cómo obtener las librerías de Python

En este proyecto se utiliza algunas librerías estándares de Python (*pprint* y *csv*), las cuales vienen instaladas con él, y otra librería llamada *requests*, la cual se puede instalar utilizando el sistema de gestión de paquetes PIP (viene instalado con Python). Para eso, se debe abrir el CMD (en un sistema de Windows) o la terminal (en un sistema de Linux), ubicarse en la carpeta donde se guardó el archivo *requirements.txt* del proyecto (utilizando el comando *cd*) y correr el comando:

```bash
pip install -r requirements.txt
```
# Obtener una lista de organizaciones a través de la API de la empresa Meraki

Para obtener una lista de organanizaciones de Meraki asociadas a una API-Key se debe ejecutar el script de Python del proyecto llamado *script.py*. En este script se emplea la librería de *requests*, para poder acceder a la información que los servidores de Meraki a través de una API-Key; la librería *pprint*, para mostrar las organizaciones de una forma agradable para la vista humana; y la librería *csv* para crear un inventario en un archivo con extensión .csv.

#### Script *script.py* (Parte I):

```python
import requests
import csv
import pprint

url = "https://api.meraki.com/api/v1/organizations"
headers = {"X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"}

org_list_json = requests.get(url, headers=headers)
org_list_json.raise_for_status()
org_list = org_list_json.json()
print("\nLista de organizaciones:\n")
pprint.pprint(org_list)
```

Con el keyword *import* se importan librerías instaladas para que se puedan utilizar sus funciones y métodos (como .get() y .json() de la librería *requests*, .pprint() de la librería *pprint* y .DictWriter(), .writeheader() y .writerow()).

La función .get() envía un request GET a la págia web de Meraki para que le permita, a través de la API, obtener la información de Meraki (en este caso, una lista de organizaciones asociados a la API-Key) correspondiente a unos parámetros especificados en los Headers en forma de archivo JSON. Dicha función necesita como parámetro el URL de la página de Meraki, la cual permite acceder a la información deseada, y los Headers, los cuales se incluyen la información fundamental que se necesita para obtener un acceso a dicha información que almacena Meraki en sus servidores. Luego, el método .raise_for_status() advierte en el caso de que ocurra un error al realizar el request, indicando su código.

Con el método .json() se convierte el archivo JSON en una lista con elementos diccionario de Python y la función .pprint() permite mostrar en pantalla la información guardada en la lista, la cual es del conjunto de organizaciones asociados a la API-Key.

# Crear un inventario (en formato .csv) de equipos de una organización a través de la API de la empresa Meraki

Para poder realizar un inventario de equipos de tipo específico, se debe encontrar la ID de la organización asociada a la API-Key. En este caso, se desea realizar un inventario de la organización **DeLab**, la cual se debe especificar en el script.

#### Script *script.py* (Parte II):

```python
nombre_organizacion = "DeLab"

for organizacion in org_list:

	if organizacion["name"] == nombre_organizacion:
		id_organizacion = organizacion["id"]
		break

	if (organizacion == org_list[-1]) and (organizacion["name"] != nombre_organizacion):
		print("\nNo existe la organizacion llamada", nombre_organizacion, end=".\n")
		exit()
```

Mediante un ciclo *for*, se empieza a buscar la organización en la información de la lista de organizaciones encontrada anteriormente. En caso de que se encuentre la organización deseada, se obtiene la ID de la misma y detiene la búsqueda. En el caso contrario, se sigue buscando hasta que se comprueba que la última organización no es la buscada y, confirmado esto, se anuncia en pantalla que no existe la organización buscada.

#### Script *script.py* (Parte III):

```python
url = "https://api.meraki.com/api/v1/organizations/{org_id}/devices/statuses".format(org_id = id_organizacion)
campos_inventario = ["Tipo de producto", "Modelo", "Nombre", "Direccion MAC", "Direccion IP Publica", "Direccion IP de LAN", "Numero serial", "Status"]
campos_deseados = ["productType", "model", "name", "mac", "publicIp", "lanIp", "serial", "status"]

equipos_json = requests.get(url, headers=headers)
equipos_json.raise_for_status()
equipos = equipos_json.json()

lista_equipos_WyA = list()
equipo = dict()
lista_equipos_camp_des = list()
```

Para hallar la información de los equipos de una organización específica de una lista de organizaciones, se debe hacer un segundo request GET a la página web de Meraki (mediante otro recurso) utilizando la ID de la organización hallada previamente para obtener la URL y, junto a la API-Key (almacenada en los Headers), obtener la información almacenada en los servidores de Meraki, a través de la API, sobre dichos equipos. Para realizar esto, se utilizó la función .get() para obtener acceso a la información de los equipos, en forma de archivo JSON. Con el método .raise_for_status() advierte en el caso de que ocurra un error al realizar el request, indicando su código. Luego, con el método .json(), se convierte la información obtenida en formato de archivo JSON en una lista con elementos diccionario de Python para su manipulación y, de esa forma, realizar el inventario.

Además, se especificó cuáles son los valores que se desean que se muestren en el inventario (en la variable *campos_inventario*) y como se obtienen se obtienen a través de la API (*campos_deseados*) y se crearon dos listas (*lista_equipos_WyA* y *lista_equipos_camp_des*), para la manipulación y seleccionamiento de datos; y un diccionario (*equipo*), para manipulación de datos.

#### Script *script.py* (Parte IV):

```python
for i in equipos:
	if ( i["productType"]=="wireless" or i["productType"]=="appliance" ):
		lista_equipos_WyA.append(i)

```

Se filtraron los equipos (obtenidos en la lista con diccionarios que contienen su información: *equipos*) que son de tipo "wireless" o "appliance" y se copiaron en una lista llamada *lista_equipos_WyA*.

#### Script *script.py* (Parte V):

```python
for j in lista_equipos_WyA:
	for key,value in j.items():
		if key in campos_deseados:
			equipo[key] = value
	lista_equipos_camp_des.append(dict(equipo))
	equipo.clear()

```

Se descartó la información (campos) de los equipos que no son de interés. La información requerida de los equipos se encuentra enlistada en *campos_deseados*. Analizando equipo por equipo, se almacena la información de interés en un diccionario temporal (llamado *equipos*) y, después de haber filtrado todos los campos, dicho diccionario se almacena como elemento en una lista llamada *lista_equipos_camp_des*. Luego, se vacía el diccionario temporal y se vuelve a repetir el ciclo hasta haber analizado toda la información de los equipos obtenida.

#### Script *script.py* (Parte VI):

```python
lista_equipos_WyA.clear()

for k in lista_equipos_camp_des:
	equipo["Tipo de producto"] = k.setdefault("productType", '')
	equipo["Modelo"] = k.setdefault("model", '')
	equipo["Nombre"] = k.setdefault("name", '')
	equipo["Direccion MAC"] = k.setdefault("mac", '')
	equipo["Direccion IP Publica"] = k.setdefault("publicIp", '')
	equipo["Direccion IP de LAN"] = k.setdefault("lanIp", '')
	equipo["Numero serial"] = k.setdefault("serial", '')
	equipo["Status"] = k.setdefault("status", '')

	lista_equipos_WyA.append(dict(equipo))

```

Se vacía la lista *lista_equipos_WyA* para utilizarla nuevamente con el objetivo de guardar en ella los diccionarios como elementos que contienen los campos deseados, pero con con los nombres de los campos que se desean para el inventario. Para los campos no definidos en algunos equipos, se les asigna ningún valor.

#### Script *script.py* (Parte VII):

```python
with open('equipos_appliance_y_wireless.csv', 'w', newline='') as archivo_csv:
	writer = csv.DictWriter(archivo_csv, fieldnames=campos_inventario)
	writer.writeheader()

	for linea in lista_equipos_WyA:
		writer.writerow(linea)

print("\nFue creado un inventario con lo equipos \"wireless\" y \"appliance\".")
```

Utilizando un manejador de archivos, se crea un archivo en modo de escritura (será referido como *archivo_csv*) para crear el inventario llamado *equipos_appliance_y_wireless.csv*.

Para escribir en dicho archivo en formato .csv, se necesita crear un escritor (llamado *writer*) mediante la función .DictWriter() con el nombre de referencia del archivo y los campos especificados que poseerá el inventario (*campos_inventarios*) como parámetros. Con el método .writeheader() se coloca en la primera línea del inventario (*equipos_appliance_y_wireless.csv*) dichos campos especificados. Luego, con el método .writerow() se escribe los campos de un equipo, el cual se encuentra como elemento diccionario en la lista *lista_equipos_WyA*, línea por línea, en el inventario.

Finalmente, se anuncia en pantalla que el inventario con los equipos de tipo "wireless" y "appliance" ha sido creado.

# Visualizar el inventario obtenido (archivo *equipos_appliance_y_wireless.csv*)

La mayoría de editores de texto (como Sublime Text 3, Notepad++, VS Code, entre otros) podrán visualizar el inventario abriendo el archivo *equipos_appliance_y_wireless.csv* con dichos softwares.

#### Ejemplo de primeras líneas del inventario:

```csv
Tipo de producto,Modelo,Nombre,Direccion MAC,Direccion IP Publica,Direccion IP de LAN,Numero serial,Status
wireless,MR84,Alex's MR84 - 1,e0:55:3d:10:56:8a,75.187.61.126,,Q2EK-2LYB-PCZP,dormant
wireless,MR84,Vegas Living Room MR84,e0:55:3d:10:5a:ca,71.222.80.198,192.168.0.20,Q2EK-3UBE-RRUY,dormant
wireless,MR84,,e0:55:3d:10:5b:d8,,,Q2EK-ACGE-URXL,dormant
```