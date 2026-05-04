def busqueda_a_estrella(grafo, heuristica, inicio, objetivo):
    """
    Algoritmo A* (A-Star).
    Encuentra la ruta óptima equilibrando el costo real (g) y la estimación (h).
    """
    print(f"--- Iniciando A* (Inicio: {inicio}, Objetivo: {objetivo}) ---\n")
    
    visitados = set()
    
    # La cola guarda tuplas: (valor_f, valor_g, nodo_actual, camino_recorrido)
    g_inicio = 0
    h_inicio = heuristica.get(inicio, float('inf'))
    f_inicio = g_inicio + h_inicio
    
    cola = [(f_inicio, g_inicio, inicio, [inicio])]

    while len(cola) > 0:
        
        # --- BÚSQUEDA DEL MENOR VALOR f(n) ---
        indice_mejor = 0
        for i in range(1, len(cola)):
            if cola[i][0] < cola[indice_mejor][0]:
                indice_mejor = i
                
        # Extraemos el nodo con el menor f(n)
        f_actual, g_actual, nodo_actual, camino = cola.pop(indice_mejor)
        
        if nodo_actual == objetivo:
            return camino, g_actual

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            print(f"[+] Visitando: {nodo_actual}")
            print(f"    g(costo real): {g_actual} | h(estimado): {f_actual - g_actual} | f(total): {f_actual}")
            
            # Obtener vecinos (diccionario con sus costos reales)
            vecinos = grafo.get(nodo_actual, {})
            for vecino, costo_real_hacia_vecino in vecinos.items():
                
                if vecino not in visitados:
                    # 1. Calculamos el nuevo g(n) -> Lo que llevamos gastado + el nuevo peaje
                    nuevo_g = g_actual + costo_real_hacia_vecino
                    
                    # 2. Obtenemos el h(n) del vecino -> Lo que falta según el GPS
                    h_vecino = heuristica.get(vecino, float('inf'))
                    
                    # 3. Calculamos el f(n) total
                    nuevo_f = nuevo_g + h_vecino
                    
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    
                    cola.append((nuevo_f, nuevo_g, vecino, nuevo_camino))
                    
    return None, None

# ==========================================
# ZONA DE PRUEBAS (Mapa de México con COSTOS REALES)
# ==========================================

# Grafo de conexiones con costo real de viaje (ej. horas o gasolina)
grafo_mexico_costos = {
    'Tepic': {'Guadalajara': 2.5, 'Zacatecas': 4},
    'Zacatecas': {'Tepic': 4, 'San Luis Potosi': 2, 'Aguascalientes': 1.5},
    'Guadalajara': {'Tepic': 2.5, 'Aguascalientes': 3, 'Leon': 4, 'Morelia': 5},
    'Aguascalientes': {'Zacatecas': 1.5, 'Guadalajara': 3, 'Leon': 2},
    'San Luis Potosi': {'Zacatecas': 2, 'Queretaro': 2.5},
    'Leon': {'Guadalajara': 4, 'Aguascalientes': 2, 'Queretaro': 2.5},
    'Morelia': {'Guadalajara': 5, 'Toluca': 3},
    'Queretaro': {'Leon': 2.5, 'San Luis Potosi': 2.5, 'CDMX': 3},
    'Toluca': {'Morelia': 3, 'CDMX': 1.5},
    'CDMX': {} # Meta
}

# Nuestro "GPS" (h(n)): Estimación en línea recta a CDMX (ajustada a la misma escala de costo)
heuristica_cdmx_ajustada = {
    'Tepic': 7,
    'Zacatecas': 6,
    'Guadalajara': 5.5,
    'Aguascalientes': 5,
    'San Luis Potosi': 4,
    'Leon': 3.5,
    'Morelia': 2.5,
    'Queretaro': 2,
    'Toluca': 1,
    'CDMX': 0 
}

nodo_inicio = 'Guadalajara'
nodo_meta = 'CDMX'

ruta, costo_total = busqueda_a_estrella(grafo_mexico_costos, heuristica_cdmx_ajustada, nodo_inicio, nodo_meta)

if ruta:
    print(f"\n ¡ÉXITO! Meta '{nodo_meta}' encontrada por A*.")
    print(f" Camino óptimo: {' -> '.join(ruta)}")
    print(f" Costo Total Real: {costo_total}")
else:
    print(f"\n La meta '{nodo_meta}' no se pudo alcanzar.")