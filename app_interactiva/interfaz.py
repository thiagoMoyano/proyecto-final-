# app_interactiva/interfaz.py
# Este archivo contiene la interfaz gráfica interactiva creada con Tkinter.

import tkinter as tk
from tkinter import messagebox
from api_clima import obtener_pronostico_semanal

ventana = None
contenedor_principal = None
lista_dias_semana = []

def limpiar_pantalla():
    for widget in contenedor_principal.winfo_children():
        widget.destroy()

def crear_accion_ver_dia(dia_seleccionado):
    def accion():
        mostrar_dia(dia_seleccionado)
    return accion

def ver_pronostico_hoy():
    primer_dia = lista_dias_semana[0]
    mostrar_dia(primer_dia)

def mostrar_menu_principal():
    limpiar_pantalla()

    marco_titulo = tk.Frame(contenedor_principal, bg="#1e3a8a", pady=15)
    marco_titulo.pack(fill="x", pady=(0, 20))

    etiqueta_titulo = tk.Label(
        marco_titulo,
        text="🌦️ Estación Meteorológica",
        font=("Segoe UI", 18, "bold"),
        fg="#ffffff",
        bg="#1e3a8a"
    )
    etiqueta_titulo.pack()

    etiqueta_subtitulo = tk.Label(
        marco_titulo,
        text="Pronóstico interactivo para los próximos 7 días",
        font=("Segoe UI", 10),
        fg="#bfdbfe",
        bg="#1e3a8a"
    )
    etiqueta_subtitulo.pack(pady=(4, 0))

    etiqueta_instruccion = tk.Label(
        contenedor_principal,
        text="¿Qué información deseas consultar hoy?",
        font=("Segoe UI", 12),
        fg="#374151",
        bg="#f3f4f6"
    )
    etiqueta_instruccion.pack(pady=15)

    boton_hoy = tk.Button(
        contenedor_principal,
        text="☀️  Ver pronóstico de HOY",
        font=("Segoe UI", 13, "bold"),
        bg="#2563eb",
        fg="#ffffff",
        activebackground="#1d4ed8",
        activeforeground="#ffffff",
        relief="flat",
        pady=12,
        cursor="hand2",
        command=ver_pronostico_hoy
    )
    boton_hoy.pack(fill="x", padx=30, pady=10)

    boton_semana = tk.Button(
        contenedor_principal,
        text="📅  Ver pronóstico de la SEMANA",
        font=("Segoe UI", 13, "bold"),
        bg="#059669",
        fg="#ffffff",
        activebackground="#047857",
        activeforeground="#ffffff",
        relief="flat",
        pady=12,
        cursor="hand2",
        command=mostrar_semana
    )
    boton_semana.pack(fill="x", padx=30, pady=10)

    etiqueta_pie = tk.Label(
        contenedor_principal,
        text="Datos meteorológicos en tiempo real desde Open-Meteo",
        font=("Segoe UI", 9, "italic"),
        fg="#9ca3af",
        bg="#f3f4f6"
    )
    etiqueta_pie.pack(side="bottom", pady=15)

def mostrar_semana():
    limpiar_pantalla()

    etiqueta_titulo = tk.Label(
        contenedor_principal,
        text="📅 Pronóstico para la Semana",
        font=("Segoe UI", 16, "bold"),
        fg="#1f2937",
        bg="#f3f4f6"
    )
    etiqueta_titulo.pack(pady=(5, 5))

    etiqueta_instruccion = tk.Label(
        contenedor_principal,
        text="Haz clic en cualquier día para ver su detalle horario:",
        font=("Segoe UI", 10),
        fg="#4b5563",
        bg="#f3f4f6"
    )
    etiqueta_instruccion.pack(pady=(0, 10))

    for dia in lista_dias_semana:
        texto_dia = dia["nombre_dia"] + " (" + dia["fecha"] + ")   |   " + str(dia["temp_promedio"]) + "°C   |   " + dia["emoji_predominante"]
        accion_para_este_dia = crear_accion_ver_dia(dia)

        boton_dia = tk.Button(
            contenedor_principal,
            text=texto_dia,
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#1f2937",
            activebackground="#e0e7ff",
            relief="solid",
            bd=1,
            pady=8,
            cursor="hand2",
            command=accion_para_este_dia
        )
        boton_dia.pack(fill="x", padx=15, pady=4)

    boton_volver = tk.Button(
        contenedor_principal,
        text="⬅  Volver al Menú Principal",
        font=("Segoe UI", 11, "bold"),
        bg="#6b7280",
        fg="#ffffff",
        activebackground="#4b5563",
        activeforeground="#ffffff",
        relief="flat",
        pady=8,
        cursor="hand2",
        command=mostrar_menu_principal
    )
    boton_volver.pack(fill="x", padx=15, pady=(15, 5))

def mostrar_dia(datos_del_dia):
    limpiar_pantalla()

    texto_encabezado = "Reporte: " + datos_del_dia["nombre_dia"] + " (" + datos_del_dia["fecha"] + ")"
    etiqueta_titulo = tk.Label(
        contenedor_principal,
        text=texto_encabezado,
        font=("Segoe UI", 15, "bold"),
        fg="#1f2937",
        bg="#f3f4f6"
    )
    etiqueta_titulo.pack(pady=(5, 5))

    etiqueta_emoji_grande = tk.Label(
        contenedor_principal,
        text=datos_del_dia["emoji_predominante"],
        font=("Segoe UI", 20, "bold"),
        fg="#2563eb",
        bg="#f3f4f6"
    )
    etiqueta_emoji_grande.pack(pady=(0, 10))

    marco_resumen = tk.Frame(contenedor_principal, bg="#ffffff", bd=1, relief="solid", padx=15, pady=10)
    marco_resumen.pack(fill="x", padx=20, pady=5)

    texto_max = "🔥 Temperatura Máxima: " + str(datos_del_dia["temp_maxima"]) + " °C"
    label_max = tk.Label(marco_resumen, text=texto_max, font=("Segoe UI", 10), bg="#ffffff", fg="#b91c1c")
    label_max.pack(anchor="w", pady=2)

    texto_min = "❄️ Temperatura Mínima: " + str(datos_del_dia["temp_minima"]) + " °C"
    label_min = tk.Label(marco_resumen, text=texto_min, font=("Segoe UI", 10), bg="#ffffff", fg="#1d4ed8")
    label_min.pack(anchor="w", pady=2)

    texto_prom = "📊 Temperatura Promedio: " + str(datos_del_dia["temp_promedio"]) + " °C"
    label_prom = tk.Label(marco_resumen, text=texto_prom, font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#374151")
    label_prom.pack(anchor="w", pady=2)

    etiqueta_seccion_horas = tk.Label(
        contenedor_principal,
        text="⏰ Desglose por Momentos Clave del Día",
        font=("Segoe UI", 12, "bold"),
        fg="#1f2937",
        bg="#f3f4f6"
    )
    etiqueta_seccion_horas.pack(pady=(12, 5))

    marco_horas = tk.Frame(contenedor_principal, bg="#ffffff", bd=1, relief="solid", padx=15, pady=8)
    marco_horas.pack(fill="x", padx=20, pady=5)

    horas = datos_del_dia["horas_clave"]
    
    texto_manana = "🌅 " + horas["manana"]["etiqueta"] + ":  " + str(horas["manana"]["temperatura"]) + " °C   |   " + horas["manana"]["emoji"]
    label_manana = tk.Label(marco_horas, text=texto_manana, font=("Segoe UI", 10), bg="#ffffff", fg="#1f2937")
    label_manana.pack(anchor="w", pady=3)

    texto_tarde = "☀️ " + horas["tarde"]["etiqueta"] + ":  " + str(horas["tarde"]["temperatura"]) + " °C   |   " + horas["tarde"]["emoji"]
    label_tarde = tk.Label(marco_horas, text=texto_tarde, font=("Segoe UI", 10), bg="#ffffff", fg="#1f2937")
    label_tarde.pack(anchor="w", pady=3)

    texto_noche = "🌙 " + horas["noche"]["etiqueta"] + ":  " + str(horas["noche"]["temperatura"]) + " °C   |   " + horas["noche"]["emoji"]
    label_noche = tk.Label(marco_horas, text=texto_noche, font=("Segoe UI", 10), bg="#ffffff", fg="#1f2937")
    label_noche.pack(anchor="w", pady=3)

    marco_botones = tk.Frame(contenedor_principal, bg="#f3f4f6")
    marco_botones.pack(fill="x", padx=20, pady=(15, 5))

    boton_ver_semana = tk.Button(
        marco_botones,
        text="📅  Ver otros días",
        font=("Segoe UI", 10, "bold"),
        bg="#059669",
        fg="#ffffff",
        activebackground="#047857",
        relief="flat",
        pady=8,
        cursor="hand2",
        command=mostrar_semana
    )
    boton_ver_semana.pack(side="left", expand=True, fill="x", padx=(0, 5))

    boton_menu = tk.Button(
        marco_botones,
        text="🏠  Menú Principal",
        font=("Segoe UI", 10, "bold"),
        bg="#6b7280",
        fg="#ffffff",
        activebackground="#4b5563",
        relief="flat",
        pady=8,
        cursor="hand2",
        command=mostrar_menu_principal
    )
    boton_menu.pack(side="right", expand=True, fill="x", padx=(5, 0))

def iniciar_interfaz():
    global ventana, contenedor_principal, lista_dias_semana

    ventana = tk.Tk()
    ventana.title("Estación Meteorológica - Reporte Interactivo")
    ventana.geometry("520x620")
    ventana.configure(bg="#f3f4f6")
    ventana.resizable(False, False)

    contenedor_principal = tk.Frame(ventana, bg="#f3f4f6")
    contenedor_principal.pack(fill="both", expand=True, padx=15, pady=15)

    etiqueta_cargando = tk.Label(
        contenedor_principal,
        text="⏳ Conectando con Open-Meteo...\nPor favor, espera unos segundos.",
        font=("Segoe UI", 13),
        fg="#4b5563",
        bg="#f3f4f6"
    )
    etiqueta_cargando.pack(expand=True)
    ventana.update()

    lista_dias_semana = obtener_pronostico_semanal()

    if lista_dias_semana == None or len(lista_dias_semana) == 0:
        messagebox.showerror(
            "Error de Conexión",
            "No se pudieron descargar los datos meteorológicos.\nVerifica tu conexión a internet e intenta nuevamente."
        )
        ventana.destroy()
        return

    mostrar_menu_principal()
    ventana.mainloop()
