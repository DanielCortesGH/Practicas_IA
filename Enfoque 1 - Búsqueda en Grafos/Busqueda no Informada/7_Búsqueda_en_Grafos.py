def busqueda_en_grafos(grafo, inicio, objetivo):
    """
    Demostración visual de la Búsqueda en Grafos.
    Utiliza una memoria para evitar regresar por donde vino y caer en ciclos.
    """
    print(f"--- Iniciando Búsqueda en Grafos (Inicio: {inicio}, Objetivo: {objetivo}) ---\n")
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    # 1. Cola para guardar el estado (nodo_actual, camino_recorrido)
    cola = [(inicio, [inicio])]
    
    # 2. El conjunto de memoria
    visitados = set()

    # ==========================================
    # SECCIÓN 2: CICLO PRINCIPAL
    # ==========================================
    while len(cola) > 0:
        nodo_actual, camino = cola.pop(0)

        # Si llegamos a la meta, terminamos y devolvemos la ruta
        if nodo_actual == objetivo:
            return camino

        # ==========================================
        # SECCIÓN 3: EXPANSIÓN Y MEMORIA
        # ==========================================
        # ¿Ya estuve aquí?
        if nodo_actual not in visitados:
            
            # Lo marcamos como visitado (lo anotamos en la memoria)
            visitados.add(nodo_actual)
            print(f"[+] Explorando nodo nuevo: {nodo_actual}")
            
            # Revisamos a sus vecinos
            vecinos = grafo.get(nodo_actual, [])
            for vecino in vecinos:
                
                # Si el vecino ya está en nuestra memoria, lo ignoramos para evitar ciclos
                if vecino in visitados:
                    print(f"    -> 🚫 Ignorando '{vecino}' (Ya está en la memoria/visitados)")
                else:
                    # Si es nuevo, lo agregamos a la cola para explorarlo después
                    print(f"    -> ➕ Agregando '{vecino}' a la cola")
                    cola.append((vecino, camino + [vecino]))
                    
    # Si la cola se vacía y no llegamos, devolvemos None
    return None

# ==========================================
# SECCIÓN 4: ZONA DE PRUEBAS
# ==========================================

# El grafo que hemos usado a lo largo del chat (con ciclos)
grafo_prueba = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'G', 'H'],
    'E': ['B', 'I'],
    'F': ['C', 'J', 'K'],
    'G': ['D', 'L'],
    'H': ['D'],
    'I': ['E', 'M', 'N'],
    'J': ['F'],
    'K': ['F', 'O'],
    'L': ['G', 'P'],
    'M': ['I'],
    'N': ['I', 'Q'],
    'O': ['K'],
    'P': ['L'],
    'Q': ['N', 'R'],
    'R': ['Q']
}

nodo_inicio = 'A'
nodo_meta = 'I'

resultado = busqueda_en_grafos(grafo_prueba, nodo_inicio, nodo_meta)

if resultado:
    print(f"\n ¡ÉXITO! Meta '{nodo_meta}' encontrada.")
    print(f" Camino final: {' -> '.join(resultado)}")
else:
    print(f"\n La meta '{nodo_meta}' no se pudo alcanzar.")