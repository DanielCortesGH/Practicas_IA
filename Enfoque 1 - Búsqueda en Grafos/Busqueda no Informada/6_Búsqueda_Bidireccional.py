def busqueda_bidireccional(grafo, inicio, objetivo):
    """
    Busca simultáneamente desde el inicio y el objetivo.
    Se detiene cuando ambas fronteras de búsqueda colisionan.
    """
    if inicio == objetivo:
        return [inicio]

    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN DE LOS DOS EQUIPOS
    # ==========================================
    
    # Dos colas nativas para hacer BFS por turnos
    cola_inicio = [[inicio]]
    cola_objetivo = [[objetivo]]

    # Dos diccionarios nativos. 
    # Llave: El nodo visitado. Valor: El camino para llegar a él.
    # Esto es crucial para poder "pegar" las rutas al final.
    visitados_inicio = {inicio: [inicio]}
    visitados_objetivo = {objetivo: [objetivo]}

    # ==========================================
    # SECCIÓN 2: CICLO DE BÚSQUEDA SIMULTÁNEA
    # ==========================================
    
    # Mientras ambos equipos tengan caminos por explorar
    while len(cola_inicio) > 0 and len(cola_objetivo) > 0:
        
        # --- TURNO DEL EQUIPO 1 (Desde el Inicio) ---
        camino_actual_i = cola_inicio.pop(0) # Extraemos FIFO
        nodo_actual_i = camino_actual_i[-1]

        vecinos_i = grafo.get(nodo_actual_i, [])
        for vecino in vecinos_i:
            if vecino not in visitados_inicio:
                nuevo_camino = list(camino_actual_i)
                nuevo_camino.append(vecino)
                
                # Registramos en memoria
                visitados_inicio[vecino] = nuevo_camino
                cola_inicio.append(nuevo_camino)

                # ¡PRUEBA DE INTERSECCIÓN!
                # ¿El equipo del objetivo ya visitó este nodo?
                if vecino in visitados_objetivo:
                    # ¡Choque! Cosemos las dos mitades
                    ruta_inicio = nuevo_camino
                    ruta_objetivo = visitados_objetivo[vecino]
                    
                    # Como la ruta objetivo está al revés (de Meta a Centro),
                    # usamos [::-1] para invertirla, y [1:] para quitar el 
                    # primer elemento y no repetir el nodo donde chocaron.
                    ruta_final = ruta_inicio + ruta_objetivo[::-1][1:]
                    return ruta_final

        # --- TURNO DEL EQUIPO 2 (Desde el Objetivo hacia atrás) ---
        camino_actual_o = cola_objetivo.pop(0) # Extraemos FIFO
        nodo_actual_o = camino_actual_o[-1]

        vecinos_o = grafo.get(nodo_actual_o, [])
        for vecino in vecinos_o:
            if vecino not in visitados_objetivo:
                nuevo_camino = list(camino_actual_o)
                nuevo_camino.append(vecino)
                
                # Registramos en memoria
                visitados_objetivo[vecino] = nuevo_camino
                cola_objetivo.append(nuevo_camino)

                # ¡PRUEBA DE INTERSECCIÓN!
                # ¿El equipo del inicio ya visitó este nodo?
                if vecino in visitados_inicio:
                    # ¡Choque! Cosemos las dos mitades
                    ruta_objetivo = nuevo_camino
                    ruta_inicio = visitados_inicio[vecino]
                    
                    ruta_final = ruta_inicio + ruta_objetivo[::-1][1:]
                    return ruta_final

    # Si se vacían las colas y no hay colisión, no hay camino posible
    return None

# ==========================================
# SECCIÓN 3: ZONA DE PRUEBAS
# ==========================================

# Un grafo no dirigido (conexiones de ida y vuelta)
grafo_prueba = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'G'],
    'E': ['B', 'H'],
    'F': ['C', 'I'],
    'G': ['D', 'J'],
    'H': ['E', 'K'],
    'I': ['F', 'L'],
    'J': ['G'],
    'K': ['H'],
    'L': ['I']
}

print("--- Ejecutando Búsqueda Bidireccional ---")
resultado = busqueda_bidireccional(grafo_prueba, 'A', 'J')

if resultado:
    print(f" ¡Ruta encontrada por intersección!")
    print(f" Camino: {' -> '.join(resultado)}")
else:
    print(" No se encontró ninguna ruta.")