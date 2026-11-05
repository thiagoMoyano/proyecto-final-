# ==============================================================================
# ARCHIVO: graficador.py
# PROPÓSITO: Generar en tiempo real los 3 gráficos horarios con Matplotlib
#            (1. Probabilidad de Lluvia, 2. Nivel de Sol, 3. Humedad)
#            y guardarlos como imagen PNG para mostrarlos en la interfaz.
# ==============================================================================


# ==============================================================================
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS
# ==============================================================================
import matplotlib.pyplot as plt


# ==============================================================================
# SECCIÓN 2: GRÁFICO 1 - PROBABILIDAD DE LLUVIA CADA HORA (GRÁFICO BÁSICO)
# ==============================================================================
def generar_grafico_lluvia(datos_dia, ruta_salida="grafico_actual.png"):
    horas = datos_dia["horas"]
    valores_lluvia = datos_dia["datos_lluvia"]
    titulo = "Probabilidad de Lluvia por Hora - " + datos_dia["nombre_dia"] + " (" + datos_dia["fecha_corta"] + ")"

    plt.figure(figsize=(7.6, 3.5), facecolor="#ffffff")

    # Barras suaves de fondo + línea con marcadores para lectura profesional
    plt.bar(horas, valores_lluvia, color="#bfdbfe", edgecolor="#93c5fd", width=0.65)
    plt.plot(
        horas,
        valores_lluvia,
        color="#1d4ed8",
        marker="o",
        linewidth=2.2,
         markersize=5,
        linestyle="-"
    )

    plt.title(titulo, fontsize=12, fontweight="bold", color="#1e3a8a", pad=12)
    plt.xlabel("Hora del Día (00:00 a 23:00 hs)", fontsize=10, color="#334155")
    plt.ylabel("Probabilidad de Lluvia (%)", fontsize=10, color="#1e3a8a")
    plt.ylim(0, 105)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=100)
    plt.close()


# ==============================================================================
# SECCIÓN 3: GRÁFICO 2 - QUÉ TAN SOLEADO ESTARÁ EL DÍA CADA HORA
# ==============================================================================
def generar_grafico_soleado(datos_dia, ruta_salida="grafico_actual.png"):
    horas = datos_dia["horas"]
    valores_sol = datos_dia["datos_soleado"]
    titulo = "Nivel de Sol (Cielo Despejado) por Hora - " + datos_dia["nombre_dia"] + " (" + datos_dia["fecha_corta"] + ")"

    plt.figure(figsize=(7.6, 3.5), facecolor="#ffffff")

    # Barras cálidas doradas + línea naranja solar
    plt.bar(horas, valores_sol, color="#fef08a", edgecolor="#fde047", width=0.65)
    plt.plot(
        horas,
        valores_sol,
        color="#d97706",
        marker="o",
        linewidth=2.2,
        markersize=5,
        linestyle="-"
    )

    plt.title(titulo, fontsize=12, fontweight="bold", color="#92400e", pad=12)
    plt.xlabel("Hora del Día (00:00 a 23:00 hs)", fontsize=10, color="#334155")
    plt.ylabel("Qué tan Soleado Estará (%)", fontsize=10, color="#92400e")
    plt.ylim(0, 105)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=100)
    plt.close()


# ==============================================================================
# SECCIÓN 4: GRÁFICO 3 - PORCENTAJE DE HUMEDAD CADA HORA
# ==============================================================================
def generar_grafico_humedad(datos_dia, ruta_salida="grafico_actual.png"):
    horas = datos_dia["horas"]
    valores_humedad = datos_dia["datos_humedad"]
    titulo = "Porcentaje de Humedad Relativa por Hora - " + datos_dia["nombre_dia"] + " (" + datos_dia["fecha_corta"] + ")"

    plt.figure(figsize=(7.6, 3.5), facecolor="#ffffff")

    # Barras celestes agua + línea turquesa intensa
    plt.bar(horas, valores_humedad, color="#a5f3fc", edgecolor="#67e8f9", width=0.65)
    plt.plot(
        horas,
        valores_humedad,
        color="#0e7490",
        marker="o",
        linewidth=2.2,
        markersize=5,
        linestyle="-"
    )

    plt.title(titulo, fontsize=12, fontweight="bold", color="#155e75", pad=12)
    plt.xlabel("Hora del Día (00:00 a 23:00 hs)", fontsize=10, color="#334155")
    plt.ylabel("Porcentaje de Humedad (%)", fontsize=10, color="#155e75")
    plt.ylim(0, 105)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=100)
    plt.close()
