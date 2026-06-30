# Visualizador de Rutas Óptimas entre Ciudades 🗺️🚀

Este proyecto es una aplicación interactiva desarrollada en Python que modela una red de transporte interurbano utilizando la **Teoría de Grafos Ponderados**. A través de una interfaz gráfica moderna, la aplicación implementa el **Algoritmo de Dijkstra** para resolver el problema del camino mínimo, hallando la ruta más eficiente entre una ciudad de origen y una de destino basándose en distancias reales de conducción en kilómetros (KM), obtenidas en tiempo real desde servicios geoespaciales de código abierto.

Proyecto final desarrollado para la asignatura de **Matemática Discreta** de la **Universidad Católica de Temuco**.

## 👥 Integrantes

- Benjamín Alarcón
- Benito Carbonell
- Miguel Torres
- Kevin Martin

**Profesor:** Elliott Jamil Mardones Arias

---

## 📑 Características Clave

- **Modelamiento Formal:** Representación abstracta del mapa mediante un grafo dirigido y ponderado $G = (V, E, w)$ compuesto por 15 ciudades (vértices) y 35 conexiones viales (aristas), donde $w: E \to \mathbb{R}^+$ asigna a cada arista su distancia real de conducción en KM.
- **Geolocalización Automatizada:** Integración con `geopy` (servidor Nominatim de OpenStreetMap) para obtener dinámicamente las coordenadas de latitud y longitud de cada ciudad, sin necesidad de API keys.
- **Distancias Viales Reales:** Cálculo de distancias de conducción reales mediante peticiones HTTP al motor de enrutamiento **OSRM** (Open Source Routing Machine), usadas como función de ponderación del grafo.
- **Algoritmo de Dijkstra Nativo:** Implementación propia en Python (sin librerías de pathfinding) que aplica el proceso de relajación de aristas para encontrar el camino mínimo, con complejidad temporal $\mathcal{O}((V + E)\log V)$.
- **Interfaz Gráfica Reactiva:** Diseñada con `customtkinter` y un lienzo dinámico embebido de `matplotlib` (vía `FigureCanvasTkAgg`) que resalta en tiempo real la ruta óptima en color rojo, junto con los nodos del recorrido en naranjo.

---

## 🛠️ Requisitos del Sistema

Para ejecutar este proyecto, necesitas tener instalado **Python 3.8 o superior** en tu sistema. Las dependencias externas necesarias se encuentran en el archivo `requirements.txt`:

- `customtkinter` (Capa de presentación e interfaz de usuario)
- `networkx` (Motor matemático y manipulador de grafos)
- `matplotlib` (Rasterización y renderizado del mapa visual)
- `geopy` (Geocodificación de ciudades vía Nominatim/OpenStreetMap)
- `requests` (Peticiones HTTP al motor de enrutamiento OSRM)

> ⚠️ **Nota:** La aplicación requiere conexión a internet al iniciarse, ya que calcula las coordenadas y distancias reales de las 15 ciudades de forma dinámica antes de mostrar la interfaz. Este proceso puede tardar algunos segundos debido al límite de 1 solicitud por segundo de Nominatim.

---

## 🚀 Instalación y Ejecución

Sigue estos sencillos pasos para clonar el repositorio y ejecutar la aplicación de forma local:

### 1. Clonar el repositorio

Abre tu terminal o consola de comandos y ejecuta:

```bash
git clone https://github.com/Benjamin-Alarcon/Proyecto-Discretas
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar aplicación

```bash
python main.py
```

---

## 🧮 Fundamento Matemático

El sistema se modela formalmente como:

$$G = (V, E, w)$$

- $V$: conjunto de 15 ciudades de EE.UU. (Seattle, Portland, San Francisco, San José, Los Ángeles, Las Vegas, Salt Lake City, Brigham City, Burley, Twin Falls, Boise, Denver, North Platte, Rapid City, Miles City).
- $E$: conjunto de 35 pares ordenados que representan las conexiones viales habilitadas.
- $w: E \to \mathbb{R}^+$: función de ponderación que devuelve la distancia en KM calculada dinámicamente vía OSRM (ej: $w(\text{Seattle, Boise}) = 793 \text{ KM}$).

El objetivo es hallar, para un origen $s$ y un destino $t$, el camino $P^* = (s, v_1, v_2, \dots, t)$ que minimiza la suma de pesos de sus aristas:

$$\sum_{(u,v) \in P^*} w(u, v) = \min_{P \in \mathcal{C}(s,t)} \left( \sum_{(u,v) \in P} w(u, v) \right)$$

donde $\mathcal{C}(s,t)$ es el conjunto de todos los caminos posibles entre $s$ y $t$. El algoritmo de Dijkstra resuelve esta ecuación de forma exacta gracias a que todos los pesos del grafo son estrictamente positivos.

---

## 🧪 Casos de Prueba Incluidos

Puedes validar la exactitud matemática del algoritmo utilizando los siguientes casos de prueba documentados en el informe técnico:

1. **Twin Falls ➔ Seattle:** Ruta transversal por el corredor noroeste vía Boise (`Twin Falls ➔ Boise ➔ Seattle`) con un costo total de **998 KM**.
2. **San José ➔ Miles City:** Ruta de larga distancia que recorre el corredor costero y central (`San José ➔ San Francisco ➔ Portland ➔ Boise ➔ Miles City`) con un costo total de **3.020 KM**.
3. **Burley ➔ North Platte:** Ruta sureste a través de la zona montañosa de Denver (`Burley ➔ Brigham City ➔ Denver ➔ North Platte`) con un costo total de **1.495 KM**.

> Los valores en KM pueden variar levemente entre ejecuciones, ya que las distancias se recalculan dinámicamente en cada inicio mediante el servicio OSRM.

---

## 🔭 Mejoras Futuras

- Visualizar rutas alternativas (no óptimas) con flechas grises para comparar trayectos.
- Incorporar un comparador visual de distancias entre distintas rutas posibles.
- Permitir más opciones de personalización en la interfaz gráfica para el usuario final.
