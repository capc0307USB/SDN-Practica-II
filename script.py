import requests			# Importa la librería requests de Python que permite establecer e intercambiar información a través de APIs.
import csv 				# Importa la librería csv de Python que permite leer, escribir y modificar un archivo de extensión .csv.
import pprint			# Importa la librería pprint de Python que permite mostrar diccionarios cómodamente en pantalla.

url = "https://api.meraki.com/api/v1/organizations"									# Variable que indica la URL a la cual se realizará el request.
headers = {"X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"}	# Variable que indica los Headers (API-Key) para acceder a la información que se accede a través la URL.

org_list_json = requests.get(url, headers=headers)	# Se envía el GET request para obtener la lista de organizaciones accesibles con el API-Key en formato JSON.
org_list_json.raise_for_status()					# Advierte en el caso de que ocurra un error al realizar el request, indicando su código.
org_list = org_list_json.json()						# Convierte el objeto obtenido por el request en una lista con elementos diccionario.
print("\nLista de organizaciones:\n")				# Muestra en pantalla que se iniciará a mostrar la lista de organizaciones.
pprint.pprint(org_list)								# Imprime en pantalla de forma cómoda la lista de organizaciones como una lista con elementos diccionario.

# ------------------------------------------------------------------------------------------------------------------------------------------

nombre_organizacion = "DeLab"				# Nombre de la organización para ubicar sus equipos.

for organizacion in org_list:							# Búsqueda de la ID de la organización

	if organizacion["name"] == nombre_organizacion:
		id_organizacion = organizacion["id"]
		break

	if (organizacion == org_list[-1]) and (organizacion["name"] != nombre_organizacion):
		print("\nNo existe la organizacion llamada", nombre_organizacion, end=".\n")
		exit()

url = "https://api.meraki.com/api/v1/organizations/{org_id}/devices".format(org_id = id_organizacion)		# Variable que indica la URL a la cual se realizará el request.
campos_inventario = ["Tipo de producto", "Modelo", "Nombre", "Direccion MAC", "Direccion IP Publica", "Direccion IP de LAN", "Numero serial", "Status"]	# Campos a incluir en el inventario.
campos_deseados = ["productType", "model", "name", "mac", "wan1Ip", "lanIp", "serial", "status"]			# Campos obtenidos a través de la API que contienen la información deseada.

equipos_json = requests.get(url, headers=headers)	# Se envía el GET request para obtener una lista de todos los equipos de la organización con el API-Key en formato JSON.
equipos_json.raise_for_status()						# Advierte en el caso de que ocurra un error al realizar el request, indicando su código.
equipos = equipos_json.json()						# Convierte el objeto obtenido por el request en una lista con elementos diccionario.

lista_equipos_WyA = list()							# Crear una lista para guardar equipos de tipo "wireless" y "appliance".
equipo = dict()										# Crear un diccionario temporal para la creación del inventario.
lista_equipos_camp_des = list()						# Crear una lista para guardar equipos de tipo "wireless" y "appliance" con sus campos deseados.

for i in equipos:															# Ubicar los equipos de tipo "wireless" y "appliance" y guardarlos en la lista lista_equipos_WyA.
	if ( i["productType"]=="wireless" or i["productType"]=="appliance" ):
		lista_equipos_WyA.append(i)

for j in lista_equipos_WyA:													# Guardar los equipos con los campos deseados a incluir en el inventario.
	for key,value in j.items():
		if key in campos_deseados:
			equipo[key] = value
	lista_equipos_camp_des.append(dict(equipo))
	equipo.clear()

lista_equipos_WyA.clear()				# Vaciar la lista lista_equipos_WyA.

for k in lista_equipos_camp_des:		# Asignar los equipos con los campos deseados del inventario a la lista_equipos_WyA y agregar un valor vacío a los campos no definidos en los servidores de Meraki.
	equipo["Tipo de producto"] = k.setdefault("productType", '')
	equipo["Modelo"] = k.setdefault("model", '')
	equipo["Nombre"] = k.setdefault("name", '')
	equipo["Direccion MAC"] = k.setdefault("mac", '')
	equipo["Direccion IP Publica"] = k.setdefault("wan1Ip", '')
	equipo["Direccion IP de LAN"] = k.setdefault("lanIp", '')
	equipo["Numero serial"] = k.setdefault("serial", '')
	equipo["Status"] = k.setdefault("status", '')

	lista_equipos_WyA.append(dict(equipo))

with open('equipos_appliance_y_wireless.csv', 'w', newline='') as archivo_csv:	# Manejador de archivos que crea uno en forma de escritura y formato .csv, con la variable archivo_csv para crear el inventario.
	writer = csv.DictWriter(archivo_csv, fieldnames=campos_inventario)			# Crear el escritor de archivos de formado .csv (en formato de diccionario) con los campos especificados en el parámetro fieldnames. 
	writer.writeheader()														# Escribir los campos en la primera líneas del inventario (equipos_appliance_y_wireless.csv).

	for linea in lista_equipos_WyA:												# Escribir el inventario línea por línea.
		writer.writerow(linea)													# Escribir la línea a través de un diccionario.

print("\nFue creado un inventario con lo equipos \"wireless\" y \"appliance\".")	# Anuncio de la creación del inventario.