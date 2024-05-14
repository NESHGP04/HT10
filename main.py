import networkx as nx
import numpy as np

def leer_grafo_desde_archivo(file_path, index_tiempo):
    G = nx.Graph()
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
    print("\nSeleccione la condición climática:")
    for i, condicion in enumerate(condiciones):
        print(f"{i + 1}. {condicion}")
    while True:
        try:
            eleccion = int(input("Opción (1-4): "))
            if 1 <= eleccion <= 4:
                return eleccion - 1
            else:
                print("Por favor, ingrese un número entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def calcular_centro_y_matriz(G):
    # Floyd-Warshall
    distance_matrix = nx.floyd_warshall_numpy(G, weight='weight')
    
    # Convertir el resultado a una matriz numpy para mejor visualización
    print("\nMatriz de distancias más cortas entre cada par de nodos:")
    print(np.array(distance_matrix))
    
    # Calcula excentricidad y centro del grafo
    excentricidad = nx.eccentricity(G, sp=dict(nx.floyd_warshall(G, weight='weight')))
    centro = min(excentricidad, key=excentricidad.get)
    return centro, excentricidad[centro], distance_matrix

def modificar_grafo(G):
    print("\nOpciones de modificación:")
    print("a. Interrumpir tráfico entre un par de ciudades")
    print("b. Establecer una nueva conexión entre ciudades")
    print("c. Cambiar los tiempos de viaje entre un par de ciudades para todas las condiciones climáticas")
    opcion = input("Seleccione una opción (a, b, c): ")

    origen = input("Ingrese la ciudad de origen: ")
    destino = input("Ingrese la ciudad de destino: ")

    if opcion == 'a':
        if G.has_edge(origen, destino):
            G.remove_edge(origen, destino)
            print(f"Tráfico interrumpido entre {origen} y {destino}.")
        else:
            print("No existe tal conexión.")

    elif opcion == 'b':
        tiempos = input("Ingrese los tiempos de viaje para las condiciones normal, lluvia, nieve y tormenta separados por espacio: ")
        tiempos = list(map(int, tiempos.split()))
        # Asignamos el tiempo bajo condición normal como el peso por defecto para simplificar
        G.add_edge(origen, destino, weight=tiempos[0], weights=tiempos)
        print(f"Nueva conexión establecida entre {origen} y {destino} con tiempos {tiempos}.")

    elif opcion == 'c':
        if G.has_edge(origen, destino):
            tiempos = input("Ingrese los nuevos tiempos de viaje para las condiciones normal, lluvia, nieve y tormenta separados por espacio: ")
            tiempos = list(map(int, tiempos.split()))
            # Actualizamos los tiempos de viaje, pero mantenemos el peso actual como el tiempo normal
            G[origen][destino]['weights'] = tiempos
            G[origen][destino]['weight'] = tiempos[0]
            print(f"Tiempos de viaje actualizados entre {origen} y {destino} a {tiempos}.")
        else:
            print("No existe conexión entre las ciudades especificadas.")

def main():
    # Leer el archivo y crear el grafo basado en la condición seleccionada
    index_tiempo = seleccionar_condicion()
    G = leer_grafo_desde_archivo('logistica.txt', index_tiempo)

    while True:
        print("\nMenú de opciones:")
        print("1. Mostrar ruta más corta entre ciudades")
        print("2. Mostrar el centro del grafo y matriz de distancias")
        print("3. Modificar el grafo")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            origen = input("Ciudad de origen: ")
            destino = input("Ciudad de destino: ")
            try:
                path = nx.shortest_path(G, source=origen, target=destino, weight='weight')
                length = nx.shortest_path_length(G, source=origen, target=destino, weight='weight')
                print(f"Ruta más corta de {origen} a {destino} es {length} pasando por {path}")
            except (nx.NetworkXNoPath, KeyError):
                print("No hay ruta disponible o una de las ciudades no existe.")
        elif opcion == '2':
            centro, excentricidad_centro, distance_matrix = calcular_centro_y_matriz(G)
            print(f"\nEl centro del grafo es: {centro}, con una excentricidad de {excentricidad_centro}")
        elif opcion == '3':
            modificar_grafo(G)
        elif opcion == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
