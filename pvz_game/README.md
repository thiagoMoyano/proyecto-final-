# 🌻 Plantas vs Zombies - Réplica en Python (Pygame-CE) 🧟

Una réplica completa, pulida y fiel del clásico **Plants vs. Zombies**, desarrollada en Python con gráficos cartoon procedurales, animaciones dinámicas, sistema de oleadas aleatorias progresivas, audio auténtico y menú interactivo de sonido y dificultad.

---

## 🎮 Características del Juego

### 🌿 Las 4 Plantas Básicas
1. **Girasol (Sunflower)** *(Costo: 50 soles | Recarga: 7.5s)*
   - Produce soles luminosos cada 20 segundos con una animación suave de salto.
   - Esencial para financiar las defensas de tu jardín.
2. **Lanzaguisantes (Peashooter)** *(Costo: 100 soles | Recarga: 7.5s)*
   - Detecta zombis en su fila y dispara guisantes verdes cada 1.4 segundos.
   - Daño de impacto con animación de retroceso y partículas de impacto.
3. **Nuez (Wall-nut)** *(Costo: 50 soles | Recarga: 20s)*
   - Gran resistencia con 4000 puntos de salud.
   - Cambia de expresión facial y muestra grietas visibles según el daño recibido (Saludable, Dañada, Agrietada con lágrimas).
4. **Papapum (Potato Mine)** *(Costo: 25 soles | Recarga: 20s)*
   - Se planta bajo tierra con una antena LED parpadeante mientras se arma (~10s).
   - Al armarse, emerge lista para la acción. Cuando un zombi la pisa: ¡**SPUDOW**! Causa 1800 de daño masivo en su casilla.

---

### 🧟 Variedad de Zombis
- **Zombi Común**: Zombi estándar con traje marrón, corbata roja torcida y apetito voraz.
- **Zombi Caracono (Conehead)**: Porta un cono de tráfico resistente que absorbe 360 puntos de daño extra antes de caerse.
- **Zombi Caracubo (Buckethead)**: Tanque blindado con un cubo metálico que absorbe 900 puntos de daño extra.
- **Zombi Atleta (Runner)**: Viste ropa deportiva y cinta roja, corriendo al doble de velocidad.

---

### 🌊 Sistema de Oleadas Aleatorias Progresivas
- Las oleadas se vuelven más difíciles progresivamente a través de un sistema de presupuesto de amenaza.
- **Oleadas Normales**: Spawns espaciados en filas aleatorias.
- **Gran Horda (Cada 4 oleadas)**: Aviso sonoro y visual en pantalla (*"¡SE ACERCA UNA GRAN HORDA DE ZOMBIES!"*), oleada masiva con caraconos y caracubos.
- **Barra de Progreso**: Muestra en tiempo real el avance de la oleada con el icono de cabeza de zombi.

---

### ⚙️ Menú de Ajustes (Audio y Dificultad)
Accesible con el botón superior **"AJUSTES / PAUSA"** o pulsando la tecla `ESC`:
- **Controles de Audio**:
  - Control deslizante de Volumen General (Master).
  - Control deslizante de Efectos de Sonido (SFX).
  - Control deslizante de Música de Fondo (PvZ Grasswalk Loop).
  - Botón de Silencio (Mute on/off).
- **Selector de Dificultad**:
  - **Fácil**: Zombis con menor velocidad y vida (-15%), soles más frecuentes (valor: 50 soles), papapum se arma más rápido.
  - **Normal**: Ritmo clásico equilibrado de PvZ (valor: 50 soles).
  - **Difícil**: Zombis rápidos (+20% velocidad y vida), más caracubos, soles de 25, spawns más densos.

---

### 🎯 Tablero y Mecánicas de Plantación
- **Tablero Jugable de 5 Filas y 8 Columnas** con césped ajedrezado verde, patio de adoquines y acera.
- **Podadoras de Césped**: 5 podadoras (una por fila). Si un zombi llega al patio, la podadora se activa a toda velocidad arrasando la fila.
- **Sistema de Cooldown**: Cada paquete de semillas muestra un sombreado oscuro que se vacía progresivamente según su tiempo de recarga.
- **Plantación con Cursor**:
  - Al tocar una planta disponible, su silueta translúcida **sigue al puntero del mouse**.
  - La casilla se ilumina en **Verde** (vacía y válida) o en **Rojo** (ocupada o inválida).
  - **Regla Estricta**: No se puede plantar más de una planta por casilla.
  - Soporta tanto clic-y-colocar como arrastrar-y-soltar (drag & drop).
  - Clic derecho o tecla `ESC` cancela la selección.
- **Herramienta Pala**: Ubicada en la barra superior para desenterrar plantas si deseas reorganizar tu jardín.

---

## 🚀 Cómo Ejecutar el Juego

### Opción 1: Desde la terminal
```bash
cd C:\Users\Alumno\.gemini\antigravity\scratch\pvz_game
python main.py
```

### Opción 2: Doble clic
Ejecuta el archivo `run_game.bat` ubicado en la carpeta del juego.

---

## ⌨️ Atajos de Teclado
- `1`: Seleccionar Girasol
- `2`: Seleccionar Lanzaguisantes
- `3`: Seleccionar Nuez
- `4`: Seleccionar Papapum
- `ESC`: Cancelar selección / Abrir Menú de Ajustes y Pausa
- `Clic Derecho`: Cancelar planta seleccionada
