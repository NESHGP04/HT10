import networkx as nx
import numpy as np

def leer_grafo_desde_archivo(file_path, index_tiempo):
    G = nx.DiGraph()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            origen, destino = parts[0], parts[1]
            tiempos = list(map(int, parts[2:]))
            peso = tiempos[index_tiempo]  # Seleccionar el tiempo basado en el input del usuario
            G.add_edge(origen, destino, weight=peso)
    return G

def seleccionar_condicion():
    condiciones = ['Normal', 'Lluvia', 'Nieve', 'Tormenta']
    for i, condicion in enumerate(condiciones):
        print(f"{i + 1}. {condicion}")
    while True:
        try:
            eleccion = int(input("Seleccione la condición climática (1-4): "))
            if 1 <= eleccion <= 4:
                return eleccion - 1
            else:
                print("Por favor, ingrese un número entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

# Leer el archivo y crear el grafo basado en la condición seleccionada
index_tiempo = seleccionar_condicion()
G = leer_grafo_desde_archivo('logistica.txt', index_tiempo)

print("Nodos:", G.nodes())
print("Aristas:", G.edges(data=True))

# Floyd-Warshall
distance_matrix = nx.floyd_warshall_numpy(G, weight='weight')

# Convertir el resultado a una matriz numpy para mejor visualización
print("Matriz de distancias más cortas entre cada par de nodos:")
print(np.array(distance_matrix))
