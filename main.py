import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

"""
Ciudades (15 ciudades no chilenas): 
Seattle, Portland, San Francisco, San José, Los Angeles, Las Vegas,
Salt Lake City, Brigham City, Burley, Twin Falls, Boise, Denver, Rapid City,
Miles City, North Platte.
Criterio único: Distancia en Kilómetros (KM).
"""

# Grafo representado como lista de adyacencia (Diccionario de diccionarios)
# Se agregaron conexiones para asegurar un mínimo de 21 aristas únicas (requerimiento > 20)
grafo_ciudades = {
    "Seattle": {"Portland": 282, "Boise": 794},
    "Portland": {"Seattle": 282, "San Francisco": 1022, "Boise": 692},
    "San Francisco": {"Portland": 1022, "San José": 80, "Las Vegas": 917},
    "San José": {"San Francisco": 80, "Los Angeles": 547, "Las Vegas": 612},
    "Los Angeles": {"San José": 547, "Las Vegas": 435},
    "Las Vegas": {"Los Angeles": 435, "San José": 612, "San Francisco": 917, "Salt Lake City": 676},
    "Salt Lake City": {"Las Vegas": 676, "Brigham City": 97, "Burley": 257, "Denver": 837, "Twin Falls": 351},
    "Brigham City": {"Salt Lake City": 97, "Burley": 193, "Denver": 821, "Twin Falls": 230},
    "Burley": {"Brigham City": 193, "Salt Lake City": 257, "Twin Falls": 64, "Boise": 270},
    "Twin Falls": {"Burley": 64, "Boise": 209, "Salt Lake City": 351, "Brigham City": 230},
    "Boise": {"Seattle": 794, "Portland": 692, "Twin Falls": 209, "Miles City": 1062, "Burley": 270},
    "Denver": {"Salt Lake City": 837, "Brigham City": 821, "North Platte": 426, "Rapid City": 636},
    "North Platte": {"Denver": 426, "Rapid City": 490}, # Conexión extra para consistencia
    "Rapid City": {"Denver": 636, "Miles City": 370, "North Platte": 490},
    "Miles City": {"Rapid City": 370, "Boise": 1062}
}

# Algoritmo de Dijkstra para camino mínimo
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
            if vecino in cola_prioridad and distancia[vecino] > distancia[nodo_menorDist] + Grafo[nodo_menorDist][vecino]:
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

# Renderizado del grafo mediante NetworkX y Matplotlib
def graficar_grafo(Grafo, contenedor, ruta_optima = None):
    for widget in contenedor.winfo_children():
        widget.destroy()
        
    # Usamos Graph() (No dirigido) para respetar la naturaleza de conexiones mutuas del mapa
    G = nx.Graph()

    for nodo, conexiones_nodo in Grafo.items():
        for vecino, peso in conexiones_nodo.items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(9, 6))

    # Dibujar nodos y aristas base
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=800,
        node_color="lightblue",
        font_size=9,
        font_weight="bold",
        edge_color="gray",
        ax=ax
    )

    edge_labels = {(u, v): f"{G[u][v]['weight']} KM" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=8,
        ax=ax
    )
    
    # Resaltar de forma clara la ruta óptima en rojo si existe
    if ruta_optima and len(ruta_optima) > 1:
        aristas_rojas = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
        nx.draw_networkx_edges(
            G, pos, edgelist=aristas_rojas, edge_color="red", width=3.5, ax=ax
        )
        # Opcional: Resaltar los nodos de la ruta elegida
        nx.draw_networkx_nodes(
            G, pos, nodelist=ruta_optima, node_color="orange", node_size=900, ax=ax
        )
    
    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Configuración de Interfaz Gráfica (CustomTkinter)
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.geometry("1200x800")
root.title("Visualizador de Rutas Óptimas entre Ciudades")
    
# Contenedor del mapa 
frame_mapa = ctk.CTkFrame(root, fg_color="white")
frame_mapa.pack(fill="both", expand=True)

# Contenedor de los controles
frame_botones = ctk.CTkFrame(root, width=280, corner_radius=15, border_width=2)
frame_botones.place(relx=0.98, rely=0.5, anchor="ne")
    
lista_ciudades = sorted(list(grafo_ciudades.keys()))

# Elementos del panel 
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

lbl_secuencia = ctk.CTkLabel(frame_botones, text="Recorrido: ---", font=("Arial", 11), text_color="black", wraplength=240)
lbl_secuencia.pack(pady=(5, 15))
    
# Acción del botón
def calcular_y_dibujar():
    origen = combo_origen.get()
    destino = combo_destino.get()
    
    if origen == destino:
        lbl_resultado.configure(text="Elige ciudades distintas", text_color="red")
        lbl_secuencia.configure(text="El origen y el destino son el mismo nodo.", text_color="red")
        graficar_grafo(grafo_ciudades, frame_mapa) # Limpia cualquier ruta roja previa
        return
    
    # Llamamos al algoritmo de Dijkstra 
    ruta, distancia_total = dijkstra(grafo_ciudades, origen, destino)
    
    # Actualizamos los textos de forma correcta
    if ruta:
        lbl_resultado.configure(text=f"Distancia: {distancia_total} KM", text_color="green")
        lbl_secuencia.configure(text=f"Ruta: {' ➔ '.join(ruta)}", text_color="black")
        # Redibujamos el mapa destacando la ruta
        graficar_grafo(grafo_ciudades, frame_mapa, ruta_optima=ruta)
    else:
        lbl_resultado.configure(text="Ruta no encontrada", text_color="red")
        lbl_secuencia.configure(text="No existe un camino disponible.", text_color="red")

btn_calcular = ctk.CTkButton(frame_botones, text="Calcular Ruta", command=calcular_y_dibujar, width=230, height=40)
btn_calcular.pack(pady=(10, 20))

# Ejecución inicial para mostrar el mapa base
graficar_grafo(grafo_ciudades, frame_mapa)

root.mainloop()