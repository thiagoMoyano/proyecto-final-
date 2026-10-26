# app_interactiva/api_clima.py
# Este archivo contiene las funciones para comunicarse con la API de Open-Meteo,
# procesar y agrupar los datos de la semana en diccionarios, y convertir códigos en emojis.

from datetime import datetime
import requests

def traducir_codigo_a_emoji(codigo):
    # Convertimos el código numérico WMO a texto y emoji con if/elif/else
    if codigo == 0:
        return "☀️ Soleado"
    elif codigo == 1 or codigo == 2 or codigo == 3:
        return "⛅ Nublado"
    elif codigo == 45 or codigo == 48:
        return "🌫️ Niebla"
    elif (codigo >= 51 and codigo <= 67) or (codigo >= 80 and codigo <= 82):
        return "🌧️ Lluvioso"
    elif codigo >= 71 and codigo <= 77:
        return "❄️ Nieve"
    elif codigo >= 95:
        return "🌩️ Tormenta"
    else:
        return "⛅ Variable"

def obtener_pronostico_semanal(latitud=-34.6037, longitud=-58.3816):
    url_base = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "hourly": "temperature_2m,weather_code",
        "forecast_days": 7,
        "timezone": "auto"
    }

    try:
        respuesta = requests.get(url_base, params=parametros)
        if respuesta.status_code == 200:
            datos_json = respuesta.json()
        else:
            return None
    except Exception:
        return None

    datos_diarios = datos_json["daily"]
    datos_horarios = datos_json["hourly"]

    nombres_dias = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
    ]

    lista_semana_procesada = []

    for indice_dia in range(7):
        fecha_texto = datos_diarios["time"][indice_dia]
        objeto_fecha = datetime.strptime(fecha_texto, "%Y-%m-%d")
        numero_dia_semana = objeto_fecha.weekday()
        nombre_dia = nombres_dias[numero_dia_semana]

        temp_maxima = datos_diarios["temperature_2m_max"][indice_dia]
        temp_minima = datos_diarios["temperature_2m_min"][indice_dia]
        codigo_dia = datos_diarios["weather_code"][indice_dia]
        emoji_predominante = traducir_codigo_a_emoji(codigo_dia)

        indice_inicio_horas = indice_dia * 24
        suma_temperaturas = 0.0
        for hora in range(24):
            posicion_actual = indice_inicio_horas + hora
            suma_temperaturas = suma_temperaturas + datos_horarios["temperature_2m"][posicion_actual]
        
        temp_promedio = round(suma_temperaturas / 24, 1)

        pos_manana = indice_inicio_horas + 8
        temp_manana = datos_horarios["temperature_2m"][pos_manana]
        emoji_manana = traducir_codigo_a_emoji(datos_horarios["weather_code"][pos_manana])

        pos_tarde = indice_inicio_horas + 14
        temp_tarde = datos_horarios["temperature_2m"][pos_tarde]
        emoji_tarde = traducir_codigo_a_emoji(datos_horarios["weather_code"][pos_tarde])

        pos_noche = indice_inicio_horas + 20
        temp_noche = datos_horarios["temperature_2m"][pos_noche]
        emoji_noche = traducir_codigo_a_emoji(datos_horarios["weather_code"][pos_noche])

        diccionario_dia = {
            "nombre_dia": nombre_dia,
            "fecha": fecha_texto,
            "temp_maxima": temp_maxima,
            "temp_minima": temp_minima,
            "temp_promedio": temp_promedio,
            "emoji_predominante": emoji_predominante,
            "horas_clave": {
                "manana": {
                    "etiqueta": "Mañana (08:00)",
                    "temperatura": temp_manana,
                    "emoji": emoji_manana
                },
                "tarde": {
                    "etiqueta": "Tarde (14:00)",
                    "temperatura": temp_tarde,
                    "emoji": emoji_tarde
                },
                "noche": {
                    "etiqueta": "Noche (20:00)",
                    "temperatura": temp_noche,
                    "emoji": emoji_noche
                }
            }
        }
        lista_semana_procesada.append(diccionario_dia)

    return lista_semana_procesada
