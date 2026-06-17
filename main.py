import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
"""
Ciudades: 
Seatle, Portland, San Francisco, San José, Los Angeles, Las Vegas,
Salt Lake City, Brigham City, Burley, Twin Falls, Boise, Denver, Rapid City
Miles City, North Platte
"""
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


#Algoritmo para encontrar el camino con menor distancia
def dijkstra(Grafo, salida,destino): # Se añade destino para detener el calulo de distancia 
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
        camino.insert(0,actual)
        actual = nodo_anterior[actual]
        
    if distancia[destino] == float('inf') or salida == destino:
        return [],0
    return camino, distancia[destino]

def graficar_grafo(Grafo,contenedor,ruta_optima = None):
    
    for widget in contenedor.winfo_children():
        widget.destroy()
    G = nx.DiGraph()

    for nodo, vecino in Grafo.items():
        for vecino, peso in vecino.items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G,seed=42)
    fig,ax = plt.subplots(figsize=(10,7))

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
        font_size=10,
        ax=ax
    )
    if ruta_optima and len(ruta_optima)>1:
        aristas_rojas=[(ruta_optima[i],ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
        nx.draw_networkx_edges(
            G,pos,edgelist= aristas_rojas,edge_color="red",width=3,arrowsize=20, ax = ax
        )
    
    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both",expand=True)
    
    
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.geometry("1200x800")
root.title("Vizualizador de Rutas optimas")
    
    # contenedor del mapa 
frame_mapa= ctk.CTkFrame(root,fg_color="white")
frame_mapa.pack(fill= "both",expand = True)
    # contenedor de los botones 
frame_botones = ctk.CTkFrame(root,width=280,corner_radius=15,border_width=2)
frame_botones.place(relx=0.98,rely=0.02,anchor="ne")
    
lista_ciudades = sorted(list(grafo_ciudades.keys()))
    #elementos del panel 
lbl_titulo = ctk.CTkLabel(frame_botones,text= "Seleccion de ciudades",font=("Arial",16,"bold"))
lbl_titulo.pack(pady=(15,10))
    
lbl_origen = ctk.CTkLabel(frame_botones,text="origen")
lbl_origen.pack()
combo_origen = ctk.CTkOptionMenu(frame_botones,values=lista_ciudades,width=230)
combo_origen.set("Seattle")
combo_origen.pack(pady=(0,10))
    
lbl_destino=ctk.CTkLabel(frame_botones, text= "Destino:")
lbl_destino.pack()
combo_destino = ctk.CTkOptionMenu(frame_botones,values=lista_ciudades,width=230)
combo_destino.set("Denver")
combo_destino.pack(pady=(0,15))
    
lbl_resultado = ctk.CTkLabel(frame_botones,text="Distancia: -- KM",font=("Arial",14,"bold"),text_color="Blue")
lbl_resultado.pack(pady=5)
    
#Accion del boton
def calcular_y_dibujar():
    origen = combo_origen.get()
    destino = combo_destino.get()
    
    if origen== destino:
        lbl_resultado.configure(text="Elige ciudades distintas",text_color= "red")
        return
    
    # llamamos al algoorimo de dijkstra 
    ruta,distancia = dijkstra(grafo_ciudades,origen,destino)
    
    #actualizamos el texto
    lbl_resultado.configure(text=f"Distancia:{distancia} KM",text_color="green")
    
    # redibujamos el mapa 
    graficar_grafo(grafo_ciudades,frame_mapa,ruta_optima=ruta)
    
btn_calcular = ctk.CTkButton(frame_botones,text="Calcular Ruta", command=calcular_y_dibujar,width=230,height=40)
btn_calcular.pack(pady=(10,20))
    #Ejecucion inicial para mostrar el mapa en blanco
graficar_grafo(grafo_ciudades,frame_mapa)

root.mainloop()
    

    
    
    

 

