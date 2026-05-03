def busqueda_costo_uniforme(grafo, inicio, objetivo):
    """
    Encuentra el camino más barato en un grafo ponderado 
  
    """
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    
    # Llevamos el registro de los nodos ya evaluados para no procesarlos en bucle.
    visitados = set()
    
    # Usamos una lista normal de Python. 
    # Guardará tuplas: (costo_acumulado, nodo_actual, camino_recorrido)
    cola = []
    
    # Insertamos el estado inicial: costo 0, nodo de inicio, y el camino inicial.
    cola.append((0, inicio, [inicio]))

    # ==========================================
    # SECCIÓN 2: CICLO PRINCIPAL Y BÚSQUEDA DEL MÍNIMO
    # ==========================================
    
    while len(cola) > 0:
        
       
        # Como no tenemos una cola de prioridad que se ordene sola, 
        # debemos iterar por toda la lista para encontrar el índice 
        # de la tupla con el costo más bajo.
        indice_menor_costo = 0
        for i in range(1, len(cola)):
            # Comparamos el costo (índice 0 de la tupla)
            if cola[i][0] < cola[indice_menor_costo][0]:
                indice_menor_costo = i
                
        # Extraemos (eliminamos y leemos) el elemento más barato de la lista
        costo_actual, nodo_actual, camino_actual = cola.pop(indice_menor_costo)
        # ---------------------------------

        # Si el nodo extraído (el más barato) es nuestra meta, terminamos la búsqueda.
        if nodo_actual == objetivo:
            return costo_actual, camino_actual

        # ==========================================
        # SECCIÓN 3: EXPANSIÓN DE NODOS
        # ==========================================
        
        if nodo_actual not in visitados:
            # Lo marcamos como procesado
            visitados.add(nodo_actual)

            # Obtenemos el diccionario de vecinos y sus costos
            vecinos = grafo.get(nodo_actual, {})

            for vecino, costo_hacia_vecino in vecinos.items():
                
                if vecino not in visitados:
                    # Sumamos el costo acumulado más el costo de este nuevo salto
                    nuevo_costo = costo_actual + costo_hacia_vecino
                    
                    # Clonamos el camino y añadimos el nuevo paso
                    nuevo_camino = list(camino_actual)
                    nuevo_camino.append(vecino)
                    
                    # Simplemente lo agregamos al final de nuestra lista. 
                    # El bucle 'for' de arriba se encargará de encontrarlo cuando sea su turno.
                    cola.append((nuevo_costo, vecino, nuevo_camino))

    # Retorna None si se agotan las opciones sin llegar a la meta
    return None, None

# ==========================================
# SECCIÓN 4: ZONA DE PRUEBAS
# ==========================================

grafo_ponderado = {
    'S': {'A': 1, 'B': 4},
    'A': {'B': 2, 'C': 5, 'G': 12},
    'B': {'C': 2},
    'C': {'G': 3},
    'G': {}
}

print("--- Búsqueda de Costo Uniforme (Sin Librerías) ---")
costo_final, ruta_final = busqueda_costo_uniforme(grafo_ponderado, 'S', 'G')

if ruta_final:
    print(f"✅ ¡Ruta óptima encontrada!")
    print(f"📍 Camino: {' -> '.join(ruta_final)}")
    print(f"💰 Costo Total: {costo_final}")
else:
    print("❌ No se encontró ninguna ruta.")