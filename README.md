# README (LÉEME)

<p>
Universidad Simón Bolívar<br>
Trimestre Abril-Julio 2022.<br>
Asignatura: Redes Definidas por Software.<br>
Profesora: Emma Di Battista.<br>
Alumno: César A. Pineda Carrero.<br>
Carnet: 15-11136.
</p>

# Práctica II de la asignatura Redes Definidas por Software (SDN).

# Cómo obtener las librerías de Python

En este proyecto se utiliza una librería estándar de Python llamada *pprint*, la cual viene instalada con él, y otra librería llamada *requests*, la cual se puede instalar utilizando el sistema de gestión de paquetes PIP (viene instalado con Python). Para eso, se debe abrir el CMD (en un sistema de Windows) o la terminal (en un sistema de Linux), ubicarse en la carpeta donde se guardó el archivo *requirements.txt* del proyecto (utilizando el comando *cd*) y correr el comando:

```bash
pip install -r requirements.txt
```
# Obtener una lista de organizaciones a través de la API de la empresa Meraki

Para obtener una lista de organanizaciones de Meraki asociadas a una API-Key se debe ejecutar el script de Python del proyecto llamado *script.py*. En este script se emplea la librería de *requests*, para poder acceder a la información que los servidores de Meraki a través de una API-Key, y la librería *pprint*, para mostrar las organizaciones de una forma agradable para la vista humana.

#### Script *script.py*:

```python
import requests
import pprint

url = "https://api.meraki.com/api/v1/organizations"
headers = {"X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"}

org_list_json = requests.get(url, headers=headers)
org_list = org_list_json.json()
print("\nLista de organizaciones:\n")
pprint.pprint(org_list)
```

Con el keyword *import* se importan librerías instaladas para que se puedan utilizar sus funciones y métodos (como .get() y .json() de la librería *requests* y .pprint() de la librería *pprint*).

La función .get() envía un request GET a la págia web de Meraki para que le permita, a través de la API, obtener la información de Meraki (en este caso, una lista de organizaciones asociados a la API-Key) correspondiente a unos parámetros especificados en los Headers en forma de archivo JSON. Dicha función necesita como parámetro el URL de la página de Meraki, la cual permite acceder a la información deseada, y los Headers, los cuales se incluyen la información fundamental que se necesita para obtener un acceso a dicha información que almacena Meraki en sus servidores.

Con el método .json() se convierte el archivo JSON en una lista con elementos diccionario de Python y la función .pprint() permite mostrar en pantalla la información guardada en la lista, la cual es del conjunto de organizaciones asociados a la API-Key.