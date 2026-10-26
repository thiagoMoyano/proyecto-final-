# api_clima.py
# Este archivo se encarga exclusivamente de conectarse con el servidor de Open-Meteo
# y traer los datos del clima en formato crudo (JSON / Diccionario).

import requests

def obtener_datos_clima(latitud, longitud):
    # Definimos la dirección web (URL) del servicio gratuito de Open-Meteo.
    # No requiere contraseña ni clave privada (API Key), lo cual es ideal para aprender.
    url_base = "https://api.open-meteo.com/v1/forecast"

    # Preparamos un diccionario con los parámetros que le enviaremos al servidor.
    # Le indicamos las coordenadas geográficas, qué dato queremos (temperatura a 2 metros del suelo)
    # y que solo nos entregue el pronóstico de 1 día (las próximas 24 horas).
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "hourly": "temperature_2m",
        "forecast_days": 1
    }

    # Usamos un bloque try / except como 'red de seguridad'.
    # Si ocurre un error imprevisto (como quedarnos sin internet), el programa no se detendrá
    # de golpe con una pantalla roja de error, sino que atrapará el fallo de forma controlada.
    try:
        print("-> Conectando con el servicio meteorológico...")
        
        # Realizamos la petición HTTP GET. Es equivalente a cuando escribes una dirección
        # en tu navegador web y presionas Enter para pedir la página.
        respuesta = requests.get(url_base, params=parametros)

        # Verificamos si la respuesta del servidor fue exitosa (código de estado 200).
        # Si el servidor nos devuelve un código de error (como 404 o 500), entrará en el else.
        if respuesta.status_code == 200:
            print("-> ¡Datos recibidos con éxito desde la nube!")
            
            # Convertimos la respuesta de texto plano que viene de la web
            # en un diccionario nativo de Python para que podamos manipularlo fácilmente.
            datos_diccionario = respuesta.json()
            return datos_diccionario
        else:
            # Si el servidor respondió pero con un código de error, mostramos el código.
            print("-> El servidor respondió con un error. Código:", respuesta.status_code)
            return None

    except Exception as error:
        # Si se corta el cable de red, no hay Wi-Fi o la URL está mal escrita,
        # la ejecución salta directo a este bloque.
        print("-> Ocurrió un problema de conexión al intentar obtener el clima.")
        print("-> Detalle técnico del error:", error)
        
        # Devolvemos None para que quien llame a esta función sepa que la operación falló.
        return None
