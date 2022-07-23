import requests			# Importa la librería requests de Python que permite establecer e intercambiar información a través de APIs.
import pprint			# Importa la librería pprint de Python que permite mostrar diccionarios cómodamente en pantalla.

url = "https://api.meraki.com/api/v1/organizations"									# Variable que indica la URL a la cual se realizará el request.
headers = {"X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"}	# Variable que indica los Headers (API-Key) para acceder a la información que se accede a través la URL.

org_list_json = requests.get(url, headers=headers)	# Se envía el GET request para obtener la lista de organizaciones accesibles con el API-Key en formato JSON.
org_list = org_list_json.json()						# Convierte el objeto obtenido por el request en una lista con elementos diccionario.
print("\nLista de organizaciones:\n")				# Muestra en pantalla que se iniciará a mostrar la lista de organizaciones.
pprint.pprint(org_list)								# Imprime en pantalla de forma cómoda la lista de organizaciones como una lista con elementos diccionario.