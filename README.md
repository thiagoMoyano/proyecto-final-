# Generador de Reportes Meteorológicos Visuales & App Interactiva

## ¿Para qué sirve esta microherramienta?

Esta microherramienta es un **Generador de Reportes Meteorológicos Visuales**. Su objetivo es automatizar la consulta de pronósticos climáticos en tiempo real desde un servicio web, organizar la información del día en una estructura limpia y generar un gráfico claro guardado como imagen local (`clima_hoy.png`), agregando un toque divertido de la comunidad de Python al iniciar.

Además, cuenta con una versión gráfica interactiva (**GUI con Tkinter**) para consultar el pronóstico de hoy o de la semana completa con detalles horarios y emojis ilustrativos.

---

## Descripción general del proyecto

El programa integra cuatro bibliotecas para ejecutar un flujo de datos continuo y comprensible:

1. **antigravity** (módulo nativo de Python): actúa como disparador visual, abriendo automáticamente el icónico cómic de Python en el navegador web al arrancar el script.
2. **requests**: realiza la petición HTTP a la API pública de Open-Meteo para obtener las temperaturas estimadas de las próximas horas en formato JSON.
3. **pandas**: recibe la información cruda del pronóstico y la convierte en un DataFrame (una tabla estructurada con las columnas `Hora` y `Temperatura`).
4. **matplotlib.pyplot**: utiliza los datos de la tabla para diseñar una curva de temperatura personalizada, ajustar títulos y ejes, y exportar la gráfica como `clima_hoy.png`.
5. **tkinter**: proporciona una ventana interactiva de escritorio para navegar visualmente por los pronósticos.

---

## Estructura del Repositorio

```text
proyecto-final-/
├── api_clima.py            # Consulta a Open-Meteo y descarga datos de 24 horas
├── procesamiento.py        # Limpieza de fechas/horas y creación del DataFrame de Pandas
├── graficador.py           # Diseño de la curva de temperatura y exportación a imagen con Matplotlib
├── main.py                 # Orquestador del reporte visual (ejecuta el flujo completo)
├── clima_hoy.png           # Imagen generada con el gráfico de temperatura
├── ejecutar.bat            # Lanzador de doble clic para Windows
├── requirements.txt        # Dependencias externas necesarias
├── .gitignore              # Archivos y carpetas ignorados por Git
└── app_interactiva/        # Versión gráfica interactiva con Tkinter
    ├── api_clima.py        # Consulta de 7 días y traductor de códigos WMO a emojis
    ├── interfaz.py         # Ventana interactiva y navegación entre pantallas
    ├── main.py             # Lanzador de la app gráfica
    └── ejecutar_app.bat    # Acceso directo para iniciar la app con doble clic
```

---

## Instalación y Requisitos

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/thiagoMoyano/proyecto-final-.git
   cd proyecto-final-
   ```

2. Instalar las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

---

## Modo de Uso

### 1. Generador de Reporte Visual (Matplotlib + Pandas)
Ejecuta el script principal desde la terminal:
```bash
python main.py
```
O simplemente haz doble clic en `ejecutar.bat` en Windows.

### 2. Aplicación Gráfica Interactiva (Tkinter)
Navega a la carpeta de la app interactiva y ejecútala:
```bash
cd app_interactiva
python main.py
```
O haz doble clic en `app_interactiva/ejecutar_app.bat`.

---

## Autor
* **Thiago Moyano**
* Escuela Técnica de Informática (ETEC UM)
