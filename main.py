# ==============================================================================
# ARCHIVO: main.py
# PROPÓSITO: Punto de entrada principal ("director de orquesta" de Clima MDZ).
#            Coordina la descarga de datos, el procesamiento de Lunes a Viernes
#            con emoticonos y el inicio de la ventana interactiva con gráficos.
# ==============================================================================


# ==============================================================================
# SECCIÓN 1: IMPORTACIÓN DE MÓDULOS DEL PROYECTO
# ==============================================================================
from api_clima import obtener_datos_crudos_clima
from procesamiento import procesar_pronostico_semana
from interfaz import iniciar_interfaz_clima


# ==============================================================================
# SECCIÓN 2: FUNCIÓN ORQUESTADORA PRINCIPAL
# ==============================================================================
def ejecutar_programa():
    print("==========================================================")
    print("      CLIMA MDZ - SISTEMA METEOROLOGICO INTERACTIVO       ")
    print("==========================================================")

    # PASO 1: Consultar los datos meteorológicos en la nube (Open-Meteo)
    datos_crudos = obtener_datos_crudos_clima()

    if datos_crudos == None:
        print("-> No se pudo iniciar la aplicacion por falta de datos.")
        return

    # PASO 2: Procesar y organizar los datos de Lunes a Viernes con emoticonos
    print("-> Procesando pronostico horario (Lunes a Viernes)...")
    lista_lunes_a_viernes = procesar_pronostico_semana(datos_crudos)

    # PASO 3: Iniciar el menú interactivo y el visor de los 3 gráficos en Tkinter
    print("-> Abriendo interfaz grafica interactiva...")
    iniciar_interfaz_clima(lista_lunes_a_viernes)


# ==============================================================================
# SECCIÓN 3: PUNTO DE ARRANQUE DEL SISTEMA
# ==============================================================================
if __name__ == "__main__":
    ejecutar_programa()
