# procesamiento.py
# Este archivo toma el diccionario crudo que nos dio la API, limpia las cadenas de texto
# de las horas y organiza todo dentro de una tabla de dos dimensiones (DataFrame de pandas).

import pandas as pd

def procesar_datos_clima(diccionario_clima):
    # La API nos devuelve un diccionario anidado. Dentro de la clave 'hourly'
    # hay dos listas paralelas: una con las fechas/horas y otra con los valores de temperatura.
    datos_horarios = diccionario_clima["hourly"]
    lista_horas_cruda = datos_horarios["time"]
    lista_temperaturas = datos_horarios["temperature_2m"]

    # Creamos una lista vacía donde iremos guardando únicamente la hora limpia (ej: "14:00").
    # Usaremos una variable temporal y el método .append() dentro de un bucle tradicional.
    lista_horas_limpias = []

    # Recorremos cada elemento de la lista cruda.
    # El formato original viene como texto completo, por ejemplo: "2026-10-26T14:00".
    for texto_fecha_hora in lista_horas_cruda:
        # El método .split("T") corta el texto en dos partes usando la letra 'T' como tijera.
        # Nos queda una lista de 2 elementos: ["2026-10-26", "14:00"].
        partes = texto_fecha_hora.split("T")
        
        # Tomamos la segunda parte (índice 1), que corresponde a la hora y minutos.
        solo_hora = partes[1]
        
        # Agregamos esta hora limpia al final de nuestra nueva lista.
        lista_horas_limpias.append(solo_hora)

    # Ahora que tenemos las dos listas limpias y del mismo tamaño, armamos un diccionario común.
    # Las claves ("Hora" y "Temperatura") serán los nombres de las columnas en nuestra tabla.
    diccionario_para_tabla = {
        "Hora": lista_horas_limpias,
        "Temperatura": lista_temperaturas
    }

    # Convertimos nuestro diccionario en un DataFrame de pandas.
    # Un DataFrame es básicamente una planilla de cálculo (filas y columnas) en memoria.
    dataframe_clima = pd.DataFrame(diccionario_para_tabla)

    # Devolvemos el DataFrame listo para ser consumido por el módulo graficador.
    return dataframe_clima
