# main.py
# Este archivo es el punto de entrada principal (el 'director de orquesta' del proyecto).
# Su función es coordinar el flujo de datos: llama a cada módulo en el orden correcto
# y le pasa la información de un paso al siguiente.

# Al importar antigravity, Python ejecuta una famosa broma interna (Easter Egg)
# de la comunidad: abrirá automáticamente en tu navegador el cómic de xkcd sobre Python.
import antigravity

# Importamos las funciones que creamos en nuestros otros 3 archivos auxiliares.
# Observa cómo el nombre del archivo se vuelve el módulo del que traemos la función.
from api_clima import obtener_datos_clima
from procesamiento import procesar_datos_clima
from graficador import generar_grafico_temperatura

def ejecutar_programa():
    print("==================================================")
    print("      GENERADOR DE REPORTES METEOROLÓGICOS        ")
    print("==================================================")

    # Definimos las coordenadas geográficas de la ciudad que queremos consultar.
    # Por ejemplo, usamos las coordenadas de Buenos Aires (Latitud: -34.6037, Longitud: -58.3816).
    # Puedes cambiar estos valores numéricos por los de tu propia ciudad.
    latitud_ciudad = -34.6037
    longitud_ciudad = -58.3816

    # PASO 1: Descargar los datos desde internet usando api_clima.
    # Le pasamos las coordenadas y guardamos el diccionario devuelto en una variable.
    datos_crudos = obtener_datos_clima(latitud_ciudad, longitud_ciudad)

    # Validamos si la descarga tuvo éxito.
    # Si ocurrió un error en la conexión, api_clima nos devolvió None.
    if datos_crudos == None:
        print("-> No se pudo continuar con el reporte porque falló la descarga de datos.")
        return

    # PASO 2: Transformar y limpiar los datos usando procesamiento.
    # Le pasamos el diccionario crudo y recibimos de vuelta un DataFrame bien estructurado.
    print("-> Limpiando y estructurando los datos en una tabla...")
    tabla_clima = procesar_datos_clima(datos_crudos)

    # Mostramos en consola las primeras 5 filas de la tabla para verificar visualmente que todo esté bien.
    # El método .head() nos permite echar un vistazo rápido a los datos sin imprimir las 24 horas completas.
    print("\n--- Vista previa de los datos procesados ---")
    print(tabla_clima.head())
    print("--------------------------------------------\n")

    # PASO 3: Generar y guardar la imagen con el gráfico usando graficador.
    # Le pasamos la tabla y el nombre del archivo de imagen que queremos crear.
    print("-> Dibujando y exportando el reporte visual...")
    nombre_archivo_grafico = "clima_hoy.png"
    generar_grafico_temperatura(tabla_clima, nombre_archivo_grafico)

    # Mensaje final de despedida para confirmar que todo el flujo concluyó con éxito.
    print("==================================================")
    print("  ¡Reporte finalizado! Revisa el archivo generado.")
    print("==================================================")

# Esta línea ejecuta nuestra función principal para iniciar todo el programa al correr este archivo.
ejecutar_programa()
