# ==============================================================================
# ARCHIVO: procesamiento.py
# PROPÓSITO: Transformar el diccionario crudo de Open-Meteo en listas y
#            diccionarios simples para Lunes, Martes, Miércoles, Jueves y Viernes,
#            asignando emoticonos representativos a cada condición climática.
# ==============================================================================


# ==============================================================================
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS
# ==============================================================================
from datetime import datetime


# ==============================================================================
# SECCIÓN 2: FUNCIONES DE EMOTICONOS REPRESENTATIVOS (CONDICIONALES)
# ==============================================================================
def traducir_codigo_a_emoji(codigo):
    # Traduce el código meteorológico WMO a un emoticono y descripción clara
    if codigo == 0:
        return "☀️ Soleado"
    elif codigo == 1:
        return "🌤️ Mayormente Soleado"
    elif codigo == 2:
        return "⛅ Parcialmente Nublado"
    elif codigo == 3:
        return "☁️ Nublado"
    elif codigo == 45 or codigo == 48:
        return "🌫️ Niebla"
    elif codigo >= 51 and codigo <= 57:
        return "🌦️ Llovizna"
    elif (codigo >= 61 and codigo <= 67) or (codigo >= 80 and codigo <= 82):
        return "🌧️ Lluvioso"
    elif codigo >= 71 and codigo <= 77:
        return "❄️ Nieve"
    elif codigo >= 95:
        return "⛈️ Tormenta"
    else:
        return "⛅ Variable"


def obtener_emoji_lluvia(porcentaje):
    # Devuelve un emoticono según la probabilidad de lluvia de esa hora
    if porcentaje >= 70:
        return "⛈️"
    elif porcentaje >= 40:
        return "🌧️"
    elif porcentaje >= 15:
        return "🌦️"
    else:
        return "🌂"


def obtener_emoji_soleado(porcentaje):
    # Devuelve un emoticono según qué tan soleado / despejado esté el cielo
    if porcentaje >= 80:
        return "☀️"
    elif porcentaje >= 50:
        return "🌤️"
    elif porcentaje >= 25:
        return "⛅"
    else:
        return "☁️"


def obtener_emoji_humedad(porcentaje):
    # Devuelve un emoticono según el porcentaje de humedad en el ambiente
    if porcentaje >= 75:
        return "🌊"
    elif porcentaje >= 50:
        return "💧"
    elif porcentaje >= 30:
        return "🍃"
    else:
        return "🏜️"


def generar_recomendaciones_emoji(lluvia_max, sol_promedio, humedad_promedio, temp_max):
    # Crea textos útiles con emoticonos según los valores del día
    if lluvia_max >= 60:
        consejo_lluvia = "☔ ¡Lleva paraguas! Lluvia muy probable"
    elif lluvia_max >= 25:
        consejo_lluvia = "🌦️ Cielo inestable, posible llovizna"
    else:
        consejo_lluvia = "😎 Sin lluvias previstas para este día"

    if sol_promedio >= 75:
        consejo_sol = "🕶️ Día muy soleado (usa protector solar 🧴)"
    elif sol_promedio >= 40:
        consejo_sol = "⛅ Sol intercalado con nubes"
    else:
        consejo_sol = "☁️ Día mayormente gris y nublado"

    if humedad_promedio >= 65:
        consejo_humedad = "💦 Ambiente húmedo y pesado"
    elif humedad_promedio >= 35:
        consejo_humedad = "🍃 Humedad agradable y confortable"
    else:
        consejo_humedad = "🏜️ Clima seco mendocino (toma agua 🥤)"

    if temp_max >= 30:
        consejo_temp = "🥵 Día caluroso"
    elif temp_max >= 20:
        consejo_temp = "😊 Clima templado y agradable"
    else:
        consejo_temp = "🧥 Día fresco, lleva abrigo"

    diccionario_consejos = {
        "lluvia": consejo_lluvia,
        "sol": consejo_sol,
        "humedad": consejo_humedad,
        "temperatura": consejo_temp
    }
    return diccionario_consejos


# ==============================================================================
# SECCIÓN 3: PROCESAMIENTO Y ORGANIZACIÓN DE DATOS (LISTAS Y DICCIONARIOS)
# ==============================================================================
def procesar_pronostico_semana(datos_crudos):
    # Extraemos las secciones principales del diccionario crudo de la API
    datos_diarios = datos_crudos["daily"]
    datos_horarios = datos_crudos["hourly"]

    nombres_dias_semana = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
    ]

    lista_todos_los_dias = []

    # Recorremos los 7 días recibidos para organizar sus 24 horas
    for indice_dia in range(7):
        fecha_completa = datos_diarios["time"][indice_dia]
        partes_fecha = fecha_completa.split("-")
        fecha_corta = partes_fecha[2] + "/" + partes_fecha[1]

        objeto_fecha = datetime.strptime(fecha_completa, "%Y-%m-%d")
        numero_dia = objeto_fecha.weekday()
        nombre_dia = nombres_dias_semana[numero_dia]

        temp_maxima = datos_diarios["temperature_2m_max"][indice_dia]
        temp_minima = datos_diarios["temperature_2m_min"][indice_dia]
        codigo_clima_dia = datos_diarios["weather_code"][indice_dia]
        emoji_general = traducir_codigo_a_emoji(codigo_clima_dia)

        # Listas paralelas para almacenar los valores de las 24 horas del día
        lista_horas = []
        lista_prob_lluvia = []
        lista_nivel_soleado = []
        lista_porcentaje_humedad = []
        lista_temperaturas = []

        # Variables acumuladoras para calcular promedios y máximos del día
        suma_sol = 0.0
        suma_humedad = 0.0
        suma_temperatura = 0.0
        maxima_lluvia_dia = 0

        indice_inicio = indice_dia * 24

        # Iteramos por cada una de las 24 horas del día actual
        for hora in range(24):
            posicion = indice_inicio + hora

            # 1. Limpiamos la hora (de "2026-11-04T14:00" nos quedamos con "14:00")
            texto_fecha_hora = datos_horarios["time"][posicion]
            partes_hora = texto_fecha_hora.split("T")
            hora_limpia = partes_hora[1]
            lista_horas.append(hora_limpia)

            # 2. Extraemos la probabilidad de lluvia (%)
            valor_lluvia = datos_horarios["precipitation_probability"][posicion]
            if valor_lluvia == None:
                valor_lluvia = 0
            lista_prob_lluvia.append(valor_lluvia)

            if valor_lluvia > maxima_lluvia_dia:
                maxima_lluvia_dia = valor_lluvia

            # 3. Calculamos qué tan soleado estará el día (%) como (100 - nubosidad)
            valor_nubosidad = datos_horarios["cloud_cover"][posicion]
            if valor_nubosidad == None:
                valor_nubosidad = 0
            valor_soleado = 100 - valor_nubosidad
            lista_nivel_soleado.append(valor_soleado)
            suma_sol = suma_sol + valor_soleado

            # 4. Extraemos el porcentaje de humedad relativa (%)
            valor_humedad = datos_horarios["relative_humidity_2m"][posicion]
            if valor_humedad == None:
                valor_humedad = 0
            lista_porcentaje_humedad.append(valor_humedad)
            suma_humedad = suma_humedad + valor_humedad

            # 5. Extraemos la temperatura horaria (°C)
            valor_temp = datos_horarios["temperature_2m"][posicion]
            if valor_temp == None:
                valor_temp = 0.0
            lista_temperaturas.append(valor_temp)
            suma_temperatura = suma_temperatura + valor_temp

        # Calculamos los promedios del día redondeados
        promedio_sol = round(suma_sol / 24, 1)
        promedio_humedad = round(suma_humedad / 24, 1)
        promedio_temperatura = round(suma_temperatura / 24, 1)

        # Obtenemos los emoticonos resumen para cada categoría
        emoji_lluvia_dia = obtener_emoji_lluvia(maxima_lluvia_dia)
        emoji_sol_dia = obtener_emoji_soleado(promedio_sol)
        emoji_humedad_dia = obtener_emoji_humedad(promedio_humedad)

        consejos_dia = generar_recomendaciones_emoji(
            maxima_lluvia_dia,
            promedio_sol,
            promedio_humedad,
            temp_maxima
        )

        # Guardamos toda la información estructurada del día en un diccionario
        diccionario_dia = {
            "nombre_dia": nombre_dia,
            "fecha_corta": fecha_corta,
            "fecha_completa": fecha_completa,
            "temp_maxima": temp_maxima,
            "temp_minima": temp_minima,
            "temp_promedio": promedio_temperatura,
            "lluvia_maxima": maxima_lluvia_dia,
            "sol_promedio": promedio_sol,
            "humedad_promedio": promedio_humedad,
            "emoji_general": emoji_general,
            "emoji_lluvia": emoji_lluvia_dia,
            "emoji_sol": emoji_sol_dia,
            "emoji_humedad": emoji_humedad_dia,
            "consejos": consejos_dia,
            "horas": lista_horas,
            "datos_lluvia": lista_prob_lluvia,
            "datos_soleado": lista_nivel_soleado,
            "datos_humedad": lista_porcentaje_humedad,
            "datos_temperatura": lista_temperaturas
        }

        lista_todos_los_dias.append(diccionario_dia)

    # ==========================================================================
    # SECCIÓN 4: FILTRADO Y ORDENAMIENTO DE LUNES A VIERNES
    # ==========================================================================
    dias_habiles_ordenados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    lista_lunes_a_viernes = []

    for nombre_buscado in dias_habiles_ordenados:
        for dia_procesado in lista_todos_los_dias:
            if dia_procesado["nombre_dia"] == nombre_buscado:
                lista_lunes_a_viernes.append(dia_procesado)

    return lista_lunes_a_viernes
