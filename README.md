# Visualizador de Rutas Óptimas entre Ciudades 🗺️🚀

Este proyecto es una aplicación interactiva desarrollada en Python que modela una red de transporte interurbano utilizando la **Teoría de Grafos Ponderados**. A través de una interfaz gráfica moderna, la aplicación implementa el **Algoritmo de Dijkstra** para resolver el problema del camino mínimo, aislando la ruta más eficiente entre una ciudad de origen y una de destino basándose en distancias reales en kilómetros (KM).

Proyecto final desarrollado para la asignatura de **Matemática Discreta** de la **Universidad Católica de Temuco**.

## 👥 Integrantes
* Benjamín Alarcón
* Benito Carbonell
* Miguel Torres
* Kevin Martin

**Profesor:** Elliott Jamil Mardones Arias

---

## 📑 Características Clave
* **Modelamiento Formal:** Representación abstracta del mapa mediante un grafo no dirigido $G = (V, E, w)$ compuesto por 15 ciudades (vértices) y 21 conexiones viales reales (aristas).
* **Algoritmo de Dijkstra Optimizado:** Inclusión de un criterio de parada anticipada (*break*) para detener la búsqueda en el momento exacto en que se alcanza el nodo de destino, reduciendo el costo computacional.
* **Estructura Eficiente:** Uso de listas de adyacencia mapeadas mediante diccionarios anidados de Python, garantizando búsquedas de vecindades en tiempo constante $\mathcal{O}(1)$.
* **Interfaz Gráfica Reactiva:** Diseñada con `customtkinter` y con un lienzo dinámico embebido de `matplotlib` que limpia la memoria y resalta en tiempo real la ruta óptima en color rojo.

---

## 🛠️ Requisitos del Sistema

Para ejecutar este proyecto, necesitas tener instalado **Python 3.8 o superior** en tu sistema. Las dependencias externas necesarias se encuentran en el archivo `requirements.txt`:
* `customtkinter` (Capa de presentación e interfaz de usuario)
* `networkx` (Motor matemático y manipulador de grafos)
* `matplotlib` (Rasterización y renderizado del mapa visual)

---

## 🚀 Instalación y Ejecución

Sigue estos sencillos pasos para clonar el repositorio y ejecutar la aplicación de forma local:

## 1. Clonar el repositorio
Abre tu terminal o consola de comandos y ejecuta:

git clone [https://github.com/Benjamin-Alarcon/Proyecto-Discretas]

## 2. Instalar dependencias

pip install -r requirements.txt

## 3. Ejecutar aplicación 

python main.py


## 🧪 Casos de Prueba Incluidos
Puedes validar la exactitud matemática del algoritmo utilizando los siguientes casos de prueba documentados en el informe técnico:

1. Burley ➔ Denver: Ruta local óptima a través de Brigham City con un costo total de 1014 KM.

2. Twin Falls ➔ Seattle: Ruta transversal por el corredor noroeste vía Boise con un costo total de 1003 KM.

3. Burley ➔ North Platte: Ruta de larga distancia cruzando múltiples estados (Burley ➔ Brigham City ➔ Denver ➔ North Platte) con un costo de 1440 KM.
