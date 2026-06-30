import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import requests
from geopy.geocoders import Nominatim 
import time

"""
Ciudades (15 ciudades no chilenas): 
Seattle, Portland, San Francisco, San José, Los Angeles, Las Vegas,
Salt Lake City, Brigham City, Burley, Twin Falls, Boise, Denver, Rapid City,
Miles City, North Platte.
Criterio único: Distancia en KM automática por texto usando OpenStreetMap + Geopy.
"""

conexiones_base = {
    "Seattle": ["Portland", "Boise"],
    "Portland": ["Seattle", "San Francisco", "Boise"],
    "San Francisco": ["Portland", "San José", "Las Vegas"],
    "San José": ["San Francisco", "Los Angeles", "Las Vegas"],
    "Los Angeles": ["San José", "Las Vegas"],
    "Las Vegas": ["Los Angeles", "San José", "San Francisco", "Salt Lake City"],
    "Salt Lake City": ["Las Vegas", "Brigham City", "Burley", "Denver", "Twin Falls"],
    "Brigham City": ["Salt Lake City", "Burley", "Denver", "Twin Falls"],
    "Burley": ["Brigham City", "Salt Lake City", "Twin Falls", "Boise"],
    "Twin Falls": ["Burley", "Boise", "Salt Lake City", "Brigham City"],
    "Boise": ["Seattle", "Portland", "Twin Falls", "Miles City", "Burley"],
    "Denver": ["Salt Lake City", "Brigham City", "North Platte", "Rapid City"],
    "North Platte": ["Denver", "Rapid City"],
    "Rapid City": ["Denver", "Miles City", "North Platte"],
    "Miles City": ["Rapid City", "Boise"]
}

def construir_grafo_automatico(conexiones):

    geolocator = Nominatim(user_agent="visualizador_rutas_universidad")
    coordenadas_cache = {}
    grafo_real = {}

    print("Obteniendo ubicaciones y calculando distancias... Por favor espera.")

    todas_las_ciudades = set(conexiones.keys())
    for ciudad in todas_las_ciudades:
        try:
            localizacion = geolocator.geocode(f"{ciudad}, USA")
            if localizacion:

                coordenadas_cache[ciudad] = (localizacion.longitude, localizacion.latitude)

        except Exception as e:
            print(f"Error al buscar la ubicación de {ciudad}: {e}")

    for origen, destinos in conexiones.items():
        grafo_real[origen] = {}
        for destino in destinos:
            try:
                if origen in coordenadas_cache and destino in coordenadas_cache:
                    lon1, lat1 = coordenadas_cache[origen]
                    lon2, lat2 = coordenadas_cache[destino]

                    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
                    respuesta = requests.get(url).json()

                    distancia_metros = respuesta['routes'][0]['distance']
                    distancia_km = round(distancia_metros / 1000)

                    grafo_real[origen][destino] = distancia_km
                else:
                    grafo_real[origen][destino] = 500
            except Exception as e:
                print(f"Error al calcular ruta entre {origen} y {destino}: {e}")
                grafo_real[origen][destino] = 500

    print("¡Grafo construido con éxito y sin usar API Keys!")
    return grafo_real

grafo_ciudades = construir_grafo_automatico(conexiones_base)

def dijkstra(Grafo, salida, destino):
    distancia, nodo_anterior = {}, {}
    for vertice in Grafo:
        distancia[vertice] = float("inf")
        nodo_anterior[vertice] = None
    distancia[salida] = 0
    cola_prioridad = [vertice for vertice in Grafo]

    while cola_prioridad:
        nodo_menorDist = min(cola_prioridad, key=distancia.get)
        cola_prioridad.remove(nodo_menorDist)
        if nodo_menorDist == destino:
            break
        for vecino in Grafo[nodo_menorDist]:
            if vecino in cola_prioridad and distancia[vecino] > distancia[nodo_menorDist] + Grafo[nodo_menorDist][
                vecino]:
                distancia[vecino] = distancia[nodo_menorDist] + Grafo[nodo_menorDist][vecino]
                nodo_anterior[vecino] = nodo_menorDist

    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual)
        actual = nodo_anterior[actual]
    if distancia[destino] == float('inf'):
        return [], 0
    return camino, distancia[destino]


def graficar_grafo(Grafo, contenedor, ruta_optima=None):
    for widget in contenedor.winfo_children():
        widget.destroy()
    G = nx.Graph()
    for nodo, conexiones_nodo in Grafo.items():
        for vecino, peso in conexiones_nodo.items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(9, 6))

    nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", font_size=9, font_weight="bold",
            edge_color="gray", ax=ax)
    edge_labels = {(u, v): f"{G[u][v]['weight']} KM" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

    if ruta_optima and len(ruta_optima) > 1:
        aristas_rojas = [(ruta_optima[i], ruta_optima[i + 1]) for i in range(len(ruta_optima) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_rojas, edge_color="red", width=3.5, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=ruta_optima, node_color="orange", node_size=900, ax=ax)

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# Configuración de Interfaz Gráfica (CustomTkinter)
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.geometry("1200x800")
root.title("Visualizador de Rutas Óptimas")

frame_mapa = ctk.CTkFrame(root, fg_color="white")
frame_mapa.pack(fill="both", expand=True)

frame_botones = ctk.CTkFrame(root, width=280, corner_radius=15, border_width=2)
frame_botones.place(relx=0.98, rely=0.5, anchor="ne")

lista_ciudades = sorted(list(grafo_ciudades.keys()))

lbl_titulo = ctk.CTkLabel(frame_botones, text="Selección de Ciudades", font=("Arial", 16, "bold"))
lbl_titulo.pack(pady=(15, 10))

lbl_origen = ctk.CTkLabel(frame_botones, text="Origen:")
lbl_origen.pack()
combo_origen = ctk.CTkOptionMenu(frame_botones, values=lista_ciudades, width=230)
combo_origen.set("Seattle")
combo_origen.pack(pady=(0, 10))

lbl_destino = ctk.CTkLabel(frame_botones, text="Destino:")
lbl_destino.pack()
combo_destino = ctk.CTkOptionMenu(frame_botones, values=lista_ciudades, width=230)
combo_destino.set("Denver")
combo_destino.pack(pady=(0, 15))

lbl_resultado = ctk.CTkLabel(frame_botones, text="Distancia: -- KM", font=("Arial", 14, "bold"), text_color="blue")
lbl_resultado.pack(pady=5)

lbl_secuencia = ctk.CTkLabel(frame_botones, text="Recorrido: ---", font=("Arial", 11), text_color="black",
                             wraplength=240)
lbl_secuencia.pack(pady=(5, 15))


def calcular_y_dibujar():
    origen = combo_origen.get()
    destino = combo_destino.get()

    if origen == destino:
        lbl_resultado.configure(text="Elige ciudades distintas", text_color="red")
        lbl_secuencia.configure(text="El origen y el destino son el mismo nodo.", text_color="red")
        graficar_grafo(grafo_ciudades, frame_mapa)
        return

    ruta, distancia_total = dijkstra(grafo_ciudades, origen, destino)

    if ruta:
        lbl_resultado.configure(text=f"Distancia: {distancia_total} KM", text_color="green")
        lbl_secuencia.configure(text=f"Ruta: {' ➔ '.join(ruta)}", text_color="black")
        graficar_grafo(grafo_ciudades, frame_mapa, ruta_optima=ruta)
    else:
        lbl_resultado.configure(text="Ruta no encontrada", text_color="red")
        lbl_secuencia.configure(text="No existe un camino disponible.", text_color="red")


btn_calcular = ctk.CTkButton(frame_botones, text="Calcular Ruta", command=calcular_y_dibujar, width=230, height=40)
btn_calcular.pack(pady=(10, 20))

graficar_grafo(grafo_ciudades, frame_mapa)
root.mainloop()
