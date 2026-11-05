# ==============================================================================
# ARCHIVO: api_clima.py
# PROPÓSITO: Conectarse al servidor gratuito de Open-Meteo y descargar los datos
#            meteorológicos crudos (en formato diccionario JSON) para Mendoza.
# ==============================================================================


# ==============================================================================
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS
# ==============================================================================
import requests


# ==============================================================================
# SECCIÓN 2: CONFIGURACIÓN DE COORDENADAS POR DEFECTO (MENDOZA, ARGENTINA)
# ==============================================================================
LATITUD_MENDOZA = -32.8895
LONGITUD_MENDOZA = -68.8458


# ==============================================================================
# SECCIÓN 3: FUNCIÓN DE CONSULTA A LA API METEOROLÓGICA
# ==============================================================================
def obtener_datos_crudos_clima(latitud=LATITUD_MENDOZA, longitud=LONGITUD_MENDOZA):
    # Dirección web del servicio meteorológico gratuito Open-Meteo
    url_base = "https://api.open-meteo.com/v1/forecast"

    # Diccionario con los parámetros que pedimos al servidor:
    # - Datos diarios: código de clima, temperatura máxima y mínima
    # - Datos por hora (24h x 7 días): temperatura, probabilidad de lluvia,
    #   nubosidad (para calcular qué tan soleado estará) y humedad relativa.
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "hourly": "temperature_2m,precipitation_probability,cloud_cover,relative_humidity_2m,weather_code",
        "forecast_days": 7,
        "timezone": "auto"
    }

    # Red de seguridad por si no hay conexión a internet
    try:
        print("-> Conectando con el servidor de Open-Meteo (Mendoza)...")
        respuesta = requests.get(url_base, params=parametros, timeout=10)

        # Si el código es 200 significa que la descarga fue exitosa
        if respuesta.status_code == 200:
            print("-> ¡Datos meteorológicos descargados con éxito!")
            datos_diccionario = respuesta.json()
            return datos_diccionario
        else:
            print("-> El servidor respondió con error. Código:", respuesta.status_code)
            return None

    except Exception as error:
        print("-> Error de conexión al consultar el clima:", error)
        return None
