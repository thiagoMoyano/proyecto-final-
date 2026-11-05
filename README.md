# 🏔️ Clima MDZ — Sistema de Reporte Meteorológico Interactivo 🌦️

Aplicación interactiva en Python que consulta el pronóstico real de **Mendoza** desde **Open-Meteo** y presenta un menú de **Lunes a Viernes** con **emoticonos representativos** y **3 gráficos horarios en tiempo real** navegables mediante un índice superior estilo hojas de Excel.

---

## 📂 Estructura del Proyecto

Todos los archivos de la infraestructura están separados por responsabilidad dentro de la misma carpeta y divididos internamente en secciones visuales claras:

1. **`api_clima.py`**: Conexión HTTP con Open-Meteo (`requests`) para descargar temperatura, probabilidad de lluvia, nubosidad y humedad de las 24 horas de cada día.
2. **`procesamiento.py`**: Limpieza de horas, cálculo de nivel de sol (`100 - nubosidad`), traducción de condiciones a **emoticonos representativos** y organización de los días **Lunes, Martes, Miércoles, Jueves y Viernes** usando únicamente listas, diccionarios, condicionales y bucles `for`.
3. **`graficador.py`**: Generación de los **3 gráficos horarios** con `matplotlib.pyplot`:
   - `🌧️ Hoja 1 (Básico por defecto)`: **Probabilidad de Lluvia (%)** cada hora.
   - `☀️ Hoja 2`: **Qué tan Soleado Estará el Día (%)** cada hora.
   - `💧 Hoja 3`: **Porcentaje de Humedad (%)** cada hora.
4. **`interfaz.py`**: Interfaz gráfica en `tkinter` con menú de botones de **Lunes a Viernes**, índice superior estilo pestañas de **Excel** para alternar entre los 3 gráficos en tiempo real, y tira horaria de emoticonos.
5. **`main.py`**: Director de orquesta que conecta `api_clima.py` -> `procesamiento.py` -> `interfaz.py`.
6. **`ejecutar.bat`**: Lanzador directo con doble clic para Windows.

---

## ▶️ Instalación y Ejecución

1. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar la aplicación haciendo doble clic en `ejecutar.bat` o desde la terminal:
   ```bash
   python main.py
   ```

---

## Autor
* **Thiago Moyano**
* Escuela Técnica de Informática (ETEC UM)
