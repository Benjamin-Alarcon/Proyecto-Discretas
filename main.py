import customtkinter as ctk
"""
Ciudades: 
Seatle, Portland, San Francisco, San José, Los Angeles, Las Vegas,
Salt Lake City, Brigham City, Burley, Twin Falls, Boise, Denver, Rapid City
Miles City, North Platte
"""

#Unidad medida en KM 
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
"rico"

#Creacion Ventana
root = ctk.CTk()

#Ajustes de tamaño en Px y titulo del programa
root.geometry("800x800")
root.title("Ruta óptima entre ciudades mediante grafos ponderas")


#Bucle para mantener la ventana abierta
root.mainloop()


# grafico del video copiado

def graficar_grafo(grafo):
    G = nx.Digraph()

    for nodo, vecino in grafo.item():
        for vecino, peso in vecino.item():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.string_layout(G)
    plt.figure(figsize(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=700,
        node_color="lightblue",
        font_size=10
        font_weight="bold"
    )

    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=10
    )

plt.title("Grafo con pesos")
plt.show
