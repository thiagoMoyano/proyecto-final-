# ==============================================================================
# ARCHIVO: interfaz.py
# PROPÓSITO: Construir la ventana interactiva en Tkinter con:
#            1. Menú simple de Lunes a Viernes con botones y emoticonos.
#            2. Vista de cada día con índice superior estilo hojas de Excel
#               para cambiar en tiempo real entre los 3 gráficos (iniciando
#               siempre en el gráfico básico de Probabilidad de Lluvia).
# ==============================================================================


# ==============================================================================
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS Y MÓDULOS PROPIOS
# ==============================================================================
import tkinter as tk
from tkinter import messagebox

from graficador import (
    generar_grafico_lluvia,
    generar_grafico_soleado,
    generar_grafico_humedad
)
from procesamiento import (
    obtener_emoji_lluvia,
    obtener_emoji_soleado,
    obtener_emoji_humedad
)


# ==============================================================================
# SECCIÓN 2: VARIABLES GLOBALES DE ESTADO DE LA INTERFAZ
# ==============================================================================
ventana = None
contenedor_principal = None
lista_dias_habiles = []
imagen_grafico_tk = None
RUTA_IMAGEN_TEMPORAL = "grafico_actual.png"


# ==============================================================================
# SECCIÓN 3: FUNCIONES AUXILIARES DE NAVEGACIÓN Y BOTONES
# ==============================================================================
def limpiar_contenedor(marco):
    # Elimina todos los elementos visuales dentro de un contenedor para redibujar
    for elemento in marco.winfo_children():
        elemento.destroy()


def crear_accion_abrir_dia(datos_dia):
    # Al entrar a cualquier día, se muestra por defecto el gráfico de 'lluvia'
    def accion():
        mostrar_pantalla_dia(datos_dia, "lluvia")
    return accion


def crear_accion_cambiar_hoja(datos_dia, nombre_hoja):
    # Permite cambiar de hoja en el índice superior estilo Excel en tiempo real
    def accion():
        mostrar_pantalla_dia(datos_dia, nombre_hoja)
    return accion


# ==============================================================================
# SECCIÓN 4: PANTALLA 1 - MENÚ PRINCIPAL SIMPLE (LUNES A VIERNES)
# ==============================================================================
def mostrar_menu_principal():
    limpiar_contenedor(contenedor_principal)

    # --- Encabezado superior ---
    marco_encabezado = tk.Frame(contenedor_principal, bg="#1e3a8a", pady=14, padx=20)
    marco_encabezado.pack(fill="x", pady=(0, 12))

    etiqueta_titulo = tk.Label(
        marco_encabezado,
        text="🏔️ Clima MDZ — Reporte Meteorológico Interactivo 🌦️",
        font=("Segoe UI", 17, "bold"),
        fg="#ffffff",
        bg="#1e3a8a"
    )
    etiqueta_titulo.pack()

    etiqueta_subtitulo = tk.Label(
        marco_encabezado,
        text="📍 Mendoza, Argentina  |  Selecciona un día hábil (Lunes a Viernes) para explorar sus 3 gráficos horarios",
        font=("Segoe UI", 10),
        fg="#bfdbfe",
        bg="#1e3a8a"
    )
    etiqueta_subtitulo.pack(pady=(4, 0))

    # --- Instrucción central ---
    etiqueta_instruccion = tk.Label(
        contenedor_principal,
        text="📅 Menú de Pronóstico Semanal (Lunes a Viernes) — Haz clic en un día:",
        font=("Segoe UI", 12, "bold"),
        fg="#1e293b",
        bg="#f1f5f9"
    )
    etiqueta_instruccion.pack(pady=(4, 10))

    # --- Contenedor de los 5 botones (Lunes, Martes, Miércoles, Jueves, Viernes) ---
    marco_lista_dias = tk.Frame(contenedor_principal, bg="#f1f5f9")
    marco_lista_dias.pack(fill="both", expand=True, padx=25)

    for dia in lista_dias_habiles:
        # Construimos el texto descriptivo rico en emoticonos para cada botón
        texto_boton = (
            "📆 " + dia["nombre_dia"] + " (" + dia["fecha_corta"] + ")    |    "
            + dia["emoji_general"] + "    |    "
            + "🔥 Máx: " + str(dia["temp_maxima"]) + "°C   ❄️ Mín: " + str(dia["temp_minima"]) + "°C    |    "
            + dia["emoji_lluvia"] + " Lluvia: " + str(dia["lluvia_maxima"]) + "%   "
            + dia["emoji_sol"] + " Sol: " + str(dia["sol_promedio"]) + "%   "
            + dia["emoji_humedad"] + " Humedad: " + str(dia["humedad_promedio"]) + "%"
        )

        accion_boton = crear_accion_abrir_dia(dia)

        boton_dia = tk.Button(
            marco_lista_dias,
            text=texto_boton,
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#0f172a",
            activebackground="#dbeafe",
            activeforeground="#1e3a8a",
            relief="solid",
            bd=1,
            pady=14,
            padx=15,
            cursor="hand2",
            command=accion_boton
        )
        boton_dia.pack(fill="x", pady=6)

    # --- Pie de página con referencia de emoticonos ---
    marco_pie = tk.Frame(contenedor_principal, bg="#e2e8f0", pady=8, padx=15)
    marco_pie.pack(fill="x", side="bottom", pady=(10, 0))

    etiqueta_pie = tk.Label(
        marco_pie,
        text="💡 Guía de Emoticonos:  ☀️ Soleado   🌤️ Poco Nublado   ⛅ Nubosidad Variable   ☁️ Nublado   🌧️ Lluvia   ⛈️ Tormenta   💧 Humedad   ☔ Paraguas",
        font=("Segoe UI", 9),
        fg="#334155",
        bg="#e2e8f0"
    )
    etiqueta_pie.pack()


# ==============================================================================
# SECCIÓN 5: PANTALLA 2 - DETALLE DEL DÍA + ÍNDICE SUPERIOR ESTILO EXCEL
# ==============================================================================
def mostrar_pantalla_dia(datos_dia, hoja_activa):
    global imagen_grafico_tk

    limpiar_contenedor(contenedor_principal)

    # --------------------------------------------------------------------------
    # 5.1 BARRA SUPERIOR: TÍTULO DEL DÍA Y BOTÓN DE VOLVER AL MENÚ
    # --------------------------------------------------------------------------
    marco_superior = tk.Frame(contenedor_principal, bg="#1e3a8a", pady=10, padx=18)
    marco_superior.pack(fill="x")

    boton_volver = tk.Button(
        marco_superior,
        text="⬅ 🏠 Menú (Lunes a Viernes)",
        font=("Segoe UI", 9, "bold"),
        bg="#3b82f6",
        fg="#ffffff",
        activebackground="#2563eb",
        activeforeground="#ffffff",
        relief="flat",
        padx=12,
        pady=5,
        cursor="hand2",
        command=mostrar_menu_principal
    )
    boton_volver.pack(side="left")

    texto_titulo_dia = (
        "📅 " + datos_dia["nombre_dia"] + " " + datos_dia["fecha_corta"]
        + "   —   " + datos_dia["emoji_general"]
        + "   |   🔥 Máx: " + str(datos_dia["temp_maxima"]) + "°C"
        + "   ❄️ Mín: " + str(datos_dia["temp_minima"]) + "°C"
        + "   🌡️ Prom: " + str(datos_dia["temp_promedio"]) + "°C"
    )

    etiqueta_titulo_dia = tk.Label(
        marco_superior,
        text=texto_titulo_dia,
        font=("Segoe UI", 12, "bold"),
        fg="#ffffff",
        bg="#1e3a8a"
    )
    etiqueta_titulo_dia.pack(side="left", padx=18)

    # --------------------------------------------------------------------------
    # 5.2 TARJETA DE EMOTICONOS Y CONSEJOS ÚTILES DEL DÍA
    # --------------------------------------------------------------------------
    marco_consejos = tk.Frame(
        contenedor_principal,
        bg="#ffffff",
        bd=1,
        relief="solid",
        padx=12,
        pady=6
    )
    marco_consejos.pack(fill="x", padx=18, pady=(8, 8))

    consejos = datos_dia["consejos"]
    texto_resumen_emojis = (
        consejos["lluvia"] + "     |     "
        + consejos["sol"] + "     |     "
        + consejos["humedad"] + "     |     "
        + consejos["temperatura"]
    )

    etiqueta_consejos = tk.Label(
        marco_consejos,
        text=texto_resumen_emojis,
        font=("Segoe UI", 9, "bold"),
        fg="#1e293b",
        bg="#ffffff"
    )
    etiqueta_consejos.pack()

    # --------------------------------------------------------------------------
    # 5.3 ÍNDICE EN LA PARTE SUPERIOR ESTILO HOJAS DE EXCEL (PESTAÑAS)
    # --------------------------------------------------------------------------
    marco_contenedor_excel = tk.Frame(contenedor_principal, bg="#f1f5f9")
    marco_contenedor_excel.pack(fill="both", expand=True, padx=18)

    marco_indice_hojas = tk.Frame(marco_contenedor_excel, bg="#cbd5e1")
    marco_indice_hojas.pack(fill="x")

    etiqueta_icono_excel = tk.Label(
        marco_indice_hojas,
        text="📑 Hojas de Gráficos:",
        font=("Segoe UI", 9, "bold"),
        fg="#334155",
        bg="#cbd5e1",
        padx=10,
        pady=6
    )
    etiqueta_icono_excel.pack(side="left")

    # Definimos las 3 hojas disponibles (Lluvia es la hoja básica inicial)
    lista_definicion_hojas = [
        {
            "clave": "lluvia",
            "texto": "🌧️ Hoja 1: Probabilidad de Lluvia (%) " + datos_dia["emoji_lluvia"],
            "color_activo": "#1d4ed8"
        },
        {
            "clave": "soleado",
            "texto": "☀️ Hoja 2: Qué tan Soleado Estará (%) " + datos_dia["emoji_sol"],
            "color_activo": "#d97706"
        },
        {
            "clave": "humedad",
            "texto": "💧 Hoja 3: Porcentaje de Humedad (%) " + datos_dia["emoji_humedad"],
            "color_activo": "#0e7490"
        }
    ]

    # Creamos cada pestaña del índice superior imitando las hojas de Excel
    for hoja in lista_definicion_hojas:
        clave_hoja = hoja["clave"]
        accion_hoja = crear_accion_cambiar_hoja(datos_dia, clave_hoja)

        if clave_hoja == hoja_activa:
            # Estilo de pestaña activa (fondo blanco conectado al gráfico y texto destacado)
            boton_pestana = tk.Button(
                marco_indice_hojas,
                text=hoja["texto"],
                font=("Segoe UI", 10, "bold"),
                bg="#ffffff",
                fg=hoja["color_activo"],
                activebackground="#ffffff",
                activeforeground=hoja["color_activo"],
                relief="solid",
                bd=1,
                padx=14,
                pady=6,
                cursor="hand2",
                command=accion_hoja
            )
            boton_pestana.pack(side="left", padx=(4, 2), pady=(4, 0))
        else:
            # Estilo de pestaña inactiva (gris suave estilo hoja en segundo plano)
            boton_pestana = tk.Button(
                marco_indice_hojas,
                text=hoja["texto"],
                font=("Segoe UI", 9),
                bg="#e2e8f0",
                fg="#475569",
                activebackground="#f8fafc",
                activeforeground="#0f172a",
                relief="flat",
                padx=12,
                pady=5,
                cursor="hand2",
                command=accion_hoja
            )
            boton_pestana.pack(side="left", padx=2, pady=(6, 2))

    # --------------------------------------------------------------------------
    # 5.4 GENERACIÓN Y VISUALIZACIÓN DEL GRÁFICO EN TIEMPO REAL
    # --------------------------------------------------------------------------
    if hoja_activa == "lluvia":
        generar_grafico_lluvia(datos_dia, RUTA_IMAGEN_TEMPORAL)
        titulo_barra_emojis = "☔ Evolución de Emoticonos de Lluvia durante el Día:"
    elif hoja_activa == "soleado":
        generar_grafico_soleado(datos_dia, RUTA_IMAGEN_TEMPORAL)
        titulo_barra_emojis = "🕶️ Evolución de Emoticonos de Sol / Nubosidad durante el Día:"
    else:
        generar_grafico_humedad(datos_dia, RUTA_IMAGEN_TEMPORAL)
        titulo_barra_emojis = "💧 Evolución de Emoticonos de Humedad durante el Día:"

    marco_lienzo_grafico = tk.Frame(
        marco_contenedor_excel,
        bg="#ffffff",
        bd=1,
        relief="solid",
        padx=6,
        pady=4
    )
    marco_lienzo_grafico.pack(fill="both", expand=True)

    imagen_grafico_tk = tk.PhotoImage(file=RUTA_IMAGEN_TEMPORAL)
    etiqueta_imagen = tk.Label(
        marco_lienzo_grafico,
        image=imagen_grafico_tk,
        bg="#ffffff"
    )
    etiqueta_imagen.pack(pady=2)

    # --------------------------------------------------------------------------
    # 5.5 TIRA HORARIA DE EMOTICONOS REPRESENTATIVOS PARA EL GRÁFICO ACTIVO
    # --------------------------------------------------------------------------
    marco_tira_horaria = tk.Frame(
        marco_lienzo_grafico,
        bg="#f8fafc",
        bd=1,
        relief="solid",
        padx=8,
        pady=6
    )
    marco_tira_horaria.pack(fill="x", padx=8, pady=(2, 4))

    etiqueta_sub_emojis = tk.Label(
        marco_tira_horaria,
        text=titulo_barra_emojis,
        font=("Segoe UI", 9, "bold"),
        fg="#334155",
        bg="#f8fafc"
    )
    etiqueta_sub_emojis.pack(anchor="w", pady=(0, 4))

    marco_celdas_horas = tk.Frame(marco_tira_horaria, bg="#f8fafc")
    marco_celdas_horas.pack(fill="x")

    # Mostramos 8 momentos clave del día (cada 3 horas) con su emoji específico
    horas_destacadas = [0, 3, 6, 9, 12, 15, 18, 21]
    iconos_reloj = ["🌙", "🌌", "🌅", "🏙️", "☀️", "🌤️", "🌇", "🌠"]

    for indice in range(8):
        hora_idx = horas_destacadas[indice]
        icono_momento = iconos_reloj[indice]
        texto_hora = datos_dia["horas"][hora_idx]
        temp_hora = datos_dia["datos_temperatura"][hora_idx]

        if hoja_activa == "lluvia":
            valor_metrica = datos_dia["datos_lluvia"][hora_idx]
            emoji_metrica = obtener_emoji_lluvia(valor_metrica)
        elif hoja_activa == "soleado":
            valor_metrica = datos_dia["datos_soleado"][hora_idx]
            emoji_metrica = obtener_emoji_soleado(valor_metrica)
        else:
            valor_metrica = datos_dia["datos_humedad"][hora_idx]
            emoji_metrica = obtener_emoji_humedad(valor_metrica)

        texto_celda = (
            icono_momento + " " + texto_hora + "\n"
            + emoji_metrica + " " + str(valor_metrica) + "%\n"
            + "🌡️ " + str(temp_hora) + "°C"
        )

        celda_hora = tk.Label(
            marco_celdas_horas,
            text=texto_celda,
            font=("Segoe UI", 8, "bold"),
            fg="#1e293b",
            bg="#ffffff",
            bd=1,
            relief="solid",
            padx=6,
            pady=4
        )
        celda_hora.pack(side="left", expand=True, fill="x", padx=2)


# ==============================================================================
# SECCIÓN 6: FUNCIÓN DE ARRANQUE DE LA VENTANA PRINCIPAL
# ==============================================================================
def iniciar_interfaz_clima(datos_lunes_a_viernes):
    global ventana, contenedor_principal, lista_dias_habiles

    lista_dias_habiles = datos_lunes_a_viernes

    ventana = tk.Tk()
    ventana.title("🏔️ Clima MDZ — Pronóstico Interactivo (Lunes a Viernes)")
    ventana.geometry("900x680")
    ventana.configure(bg="#f1f5f9")
    ventana.resizable(False, False)

    contenedor_principal = tk.Frame(ventana, bg="#f1f5f9")
    contenedor_principal.pack(fill="both", expand=True)

    if lista_dias_habiles == None or len(lista_dias_habiles) == 0:
        messagebox.showerror(
            "Error de Conexión",
            "No se pudieron obtener los datos meteorológicos.\nVerifica tu conexión a internet."
        )
        ventana.destroy()
        return

    mostrar_menu_principal()
    ventana.mainloop()
