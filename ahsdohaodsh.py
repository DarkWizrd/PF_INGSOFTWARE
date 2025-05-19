

import requests

# URI: La URL de la API a la que se hace la solicitud
url = "https://api.clima.com/ciudad?nombre=Barcelona"

# Encabezado: Definir los encabezados de la solicitud, como la autorización y el tipo de contenido
headers = {
    "Authorization": "TOKEN BEARER AQUI",  # Token de autorización para acceder a la API
    "Content-Type": "application/json"       # El tipo de contenido que esperamos y enviamos es JSON
}

# Verbo de la solicitud: En este caso estamos utilizando el verbo GET para obtener información
response = requests.get(url, headers=headers)  # Solicitud GET a la API con los encabezados definidos

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Cuerpo de la respuesta: La respuesta viene en formato JSON, por lo que la parseamos
    data = response.json()  # Convertir la respuesta en formato JSON a un diccionario de Python
    print("Temperatura actual:", data["temperatura"], "°C")  # Imprimir la temperatura obtenida de la respuesta
else:
    # Si no se obtuvo una respuesta exitosa, mostrar el código de error
    print("Error al obtener datos del clima. Código:", response.status_code)






