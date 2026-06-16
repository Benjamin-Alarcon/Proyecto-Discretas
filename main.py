import networkx as nx
import matplotlib.pyplot as plt
"""
Ciudades: 
Seatle, Portland, San Francisco, San José, Los Angeles, Las Vegas,
Salt Lake City, Brigham City, Burley, Twin Falls, Boise, Denver, Rapid City
Miles City, North Platte
"""

#Algoritmo para encontrar el camino con menor distancia
def dijkstra(Grafo, salida):
    distancia, nodo_anterior = {}, {}

    for vertice in Grafo:
        distancia[vertice] = float("inf")
        nodo_anterior[vertice] = None
    distancia[salida] = 0

    cola_prioridad = [vertice for vertice in Grafo]

    while cola_prioridad:
        nodo_menorDist = min(cola_prioridad, key=distancia.get)
        cola_prioridad.remove(nodo_menorDist)

        for vecino in Grafo[nodo_menorDist]:
            if vecino in cola_prioridad and distancia[vecino] > distancia[nodo_menorDist] + Grafo[nodo_menorDist][vecino]:
                distancia[vecino] = distancia[nodo_menorDist] + Grafo[nodo_menorDist][vecino]
                nodo_anterior[vecino] = nodo_menorDist
    return distancia

def graficar_grafo(Grafo):
    G = nx.DiGraph()

    for nodo, vecino in Grafo.items():
        for vecino, peso in vecino.items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=700,
        node_color="lightblue",
        font_size=10,
        font_weight="bold"
    )

    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=10
    )
    
    plt.show()
    
    
#Unidad medida en KM, Ciudades guardadas en una matriz(contiene ciudad proxima y km de distancia
grafo_ciudades = {
    "Seattle": {"Portland": 282, "Boise": 794},
    "Portland": {"Seattle": 282, "San Francisco": 1022, "Boise": 692},
    "San Francisco": {"Portland": 1022, "San José": 80},
    "San José": {"San Francisco": 80, "Los Angeles": 547, "Las Vegas": 612},
    "Los Angeles": {"San José": 547, "Las Vegas": 435},
    "Las Vegas": {"Los Angeles": 435, "San José": 612, "Salt Lake City": 676},
    "Salt Lake City": {"Las Vegas": 676, "Brigham City": 97, "Burley": 257, "Denver": 837, "Twin Falls": 351},
    "Brigham City": {"Salt Lake City": 97, "Burley": 193, "Denver": 821},
    "Burley": {"Brigham City": 193, "Salt Lake City": 257, "Twin Falls": 64},
    "Twin Falls": {"Burley": 64, "Boise": 209, "Salt Lake City": 351},
    "Boise": {"Seattle": 794, "Portland": 692, "Twin Falls": 209, "Miles City": 1062},
    "Denver": {"Salt Lake City": 837, "Brigham City": 821, "North Platte": 426, "Rapid City": 636},
    "North Platte": {"Denver": 426},
    "Rapid City": {"Denver": 636, "Miles City": 370},
    "Miles City": {"Rapid City": 370, "Boise": 1062}
}

recorrido = list(dijkstra(grafo_ciudades, "Salt Lake City"))
print("\nDistancias más cortas a cada nodo: ",dijkstra(grafo_ciudades, "Salt Lake City"))
graficar_grafo(grafo_ciudades)