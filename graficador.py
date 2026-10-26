# graficador.py
# Este archivo recibe la tabla estructurada (DataFrame) y se encarga del diseño visual:
# dibuja la línea de temperatura, define títulos, ejes, cuadrícula y exporta la imagen a disco.

import matplotlib.pyplot as plt

def generar_grafico_temperatura(dataframe_clima, ruta_salida="clima_hoy.png"):
    # Creamos un lienzo o figura nueva para dibujar nuestro gráfico.
    # El parámetro figsize=(12, 6) define el tamaño en pulgadas: 12 de ancho por 6 de alto.
    plt.figure(figsize=(12, 6))

    # Dibujamos la línea de temperatura pasando la columna 'Hora' al eje X y 'Temperatura' al eje Y.
    # Le asignamos un color azul acero ('steelblue'), marcadores redondos ('o') en cada hora
    # y un grosor de línea de 2 píxeles para que se vea claro y profesional.
    plt.plot(
        dataframe_clima["Hora"],
        dataframe_clima["Temperatura"],
        color="royalblue",
        marker="o",
        linewidth=2,
        linestyle="-"
    )

    # Agregamos un título principal en la parte superior del gráfico con fuente destacada.
    plt.title("Pronóstico de Temperatura para las Próximas 24 Horas", fontsize=15, pad=15)

    # Colocamos nombres descriptivos a cada eje para que cualquier persona entienda el gráfico.
    plt.xlabel("Hora del Día", fontsize=11)
    plt.ylabel("Temperatura (°C)", fontsize=11)

    # Rotamos las etiquetas del eje horizontal (X) a 45 grados.
    # Al haber 24 horas, si estuvieran horizontales se encimarían y serían ilegibles.
    plt.xticks(rotation=45)

    # Agregamos una cuadrícula de fondo punteada ('--') con transparencia (alpha=0.6).
    # Esto facilita seguir visualmente qué temperatura hace a determinada hora.
    plt.grid(True, linestyle="--", alpha=0.6)

    # Usamos tight_layout() para que matplotlib ajuste automáticamente los márgenes.
    # Esto evita que los textos de las horas o los títulos queden cortados en la imagen final.
    plt.tight_layout()

    # Guardamos el gráfico generado en un archivo de imagen PNG en el disco de tu computadora.
    # El parámetro dpi=150 asegura una buena resolución visual sin que el archivo pese demasiado.
    plt.savefig(ruta_salida, dpi=150)

    # Cerramos la figura para liberar memoria RAM en la computadora.
    # Si fuéramos a crear muchos gráficos seguidos, esto evitaría que el programa consuma memoria de más.
    plt.close()

    print("-> ¡Gráfico generado exitosamente y guardado como:", ruta_salida, "!")
