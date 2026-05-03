def busqueda_en_profundidad(grafo, inicio, objetivo):
    """
    Encuentra un camino entre un nodo de inicio y un objetivo 
    utilizando el algoritmo de Búsqueda en Profundidad (DFS).
    """
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    
    # El set nativo 'visitados' evita que entremos en bucles infinitos.
    visitados = set()
    
    # Nuestra Pila (Stack) es una lista normal. 
    # Aquí insertamos el camino inicial.
    pila = [[inicio]]

    # ==========================================
    # SECCIÓN 2: CICLO PRINCIPAL (LIFO)
    # ==========================================
    
    while len(pila) > 0:
        # ¡LA DIFERENCIA CLAVE CON BFS ESTÁ AQUÍ!
        # Usamos pop() sin ningún índice. En Python, esto extrae el ÚLTIMO 
        # elemento que fue agregado a la lista (LIFO). 
        # Esto nos obliga a explorar lo más profundo primero.
        camino_actual = pila.pop()
        
        # El nodo que estamos evaluando es el último de este camino
        nodo_actual = camino_actual[-1]

        # Verificamos si hemos llegado a la meta
        if nodo_actual == objetivo:
            return camino_actual

        # ==========================================
        # SECCIÓN 3: EXPANSIÓN Y RETROCESO (BACKTRACKING)
        # ==========================================
        
        if nodo_actual not in visitados:
            # Marcamos el nodo como visitado al momento de expandirlo
            visitados.add(nodo_actual)

            # Obtenemos los vecinos. Si no hay, devuelve una lista vacía.
            vecinos = grafo.get(nodo_actual, [])

            # TRUCO: Iteramos sobre los vecinos en reversa usando reversed() (función nativa).
            # Como la pila extrae el último elemento agregado, si queremos explorar
            # el vecino "izquierdo" (el primero en la lista) antes que el "derecho", 
            # debemos meter el izquierdo al final.
            for vecino in reversed(vecinos):
                if vecino not in visitados:
                    # Creamos una copia de la ruta actual
                    nuevo_camino = list(camino_actual)
                    nuevo_camino.append(vecino)
                    
                    # Agregamos la nueva ruta al final de la pila
                    pila.append(nuevo_camino)

    # Si se vacía la pila sin encontrar el objetivo
    return None

# ==========================================
# SECCIÓN 4: ZONA DE PRUEBAS
# ==========================================

grafo_prueba = {
    'A': ['B', 'C'],
    'B': ['D', 'E' ],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': ['I'],
    'F': [],
    'G': ['J'],
    'H': [],
    'I': [],
    'J': [] # Nodo meta
}

print("--- Ejecutando Búsqueda en Profundidad (Sin librerías) ---")
resultado = busqueda_en_profundidad(grafo_prueba, 'A', 'J')

if resultado:
    print(f" ¡Ruta encontrada!")
    print(f" Camino: {' -> '.join(resultado)}")
else:
    print(" No se encontró ninguna ruta.")