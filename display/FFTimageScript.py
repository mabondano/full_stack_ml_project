import requests
import base64

# URL de tu API FastAPI
url = "http://127.0.0.1:9090/calculate_fft?wc=0.5&M=30"

# Hacer la solicitud GET
response = requests.get(url)
if response.status_code == 200:
    # Decodificar la imagen
    image_data = base64.b64decode(response.json()["image"])

    # Guardar la imagen en un archivo local
    with open("fft_result.png", "wb") as img_file:
        img_file.write(image_data)
    print("Imagen guardada como fft_result.png")
else:
    print("Error al hacer la solicitud:", response.status_code)
