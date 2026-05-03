def busqueda_en_anchura(grafo, inicio, objetivo):
    # Usamos un set nativo de Python para llevar el registro de visitados
    visitados = set()
    
    # Nuestra cola ahora es una simple lista de listas
    cola = [[inicio]]

    if inicio == objetivo:
        return [inicio]

    # Ciclo principal: mientras la lista 'cola' tenga elementos
    while len(cola) > 0:
        # Extraemos el primer elemento usando pop(0). 
        # El índice 0 indica que sacamos el elemento del inicio de la lista (FIFO).
        camino_actual = cola.pop(0)
        
        nodo_actual = camino_actual[-1]

        if nodo_actual not in visitados:
            # Diccionarios nativos soportan .get()
            vecinos = grafo.get(nodo_actual, [])

            for vecino in vecinos:
                # Copiamos la lista nativa usando list()
                nuevo_camino = list(camino_actual)
                nuevo_camino.append(vecino)
                
                if vecino == objetivo:
                    return nuevo_camino
                
                # Agregamos al final de la lista
                cola.append(nuevo_camino)

            visitados.add(nodo_actual)

    return None

# ==========================================
# Zona de Pruebas
# ==========================================
grafo_prueba = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B', 'H'],
    'F': ['C'],
    'G': ['C', 'I'],
    'H': ['E'],
    'I': ['G']
}

resultado = busqueda_en_anchura(grafo_prueba, 'A', 'G')

if resultado:
    print(f"Ruta encontrada: {' -> '.join(resultado)}")
else:
    print("No se encontró ruta.")