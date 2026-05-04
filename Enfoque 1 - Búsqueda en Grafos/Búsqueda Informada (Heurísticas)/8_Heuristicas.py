def busqueda_voraz(grafo, heuristica, inicio, objetivo):
    """
    Búsqueda Voraz Primero el Mejor.
    Se guía ÚNICAMENTE por la estimación del GPS (heurística h(n)).
    """
    print(f"--- Iniciando Búsqueda Voraz (Inicio: {inicio}, Objetivo: {objetivo}) ---\n")
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    visitados = set()
    
    # La cola guarda tuplas: (valor_h, nodo_actual, camino_recorrido)
    # Obtenemos la distancia estimada desde el inicio hasta la meta
    h_inicio = heuristica.get(inicio, float('inf'))
    cola = [(h_inicio, inicio, [inicio])]

    # ==========================================
    # SECCIÓN 2: CICLO PRINCIPAL (Busca el menor h(n))
    # ==========================================
    while len(cola) > 0:
        
        # --- BÚSQUEDA DEL MENOR VALOR HEURÍSTICO (SIN LIBRERÍAS) ---
        indice_mejor = 0
        for i in range(1, len(cola)):
            # Comparamos el valor h(n) (índice 0 de la tupla)
            if cola[i][0] < cola[indice_mejor][0]:
                indice_mejor = i
                
        # Extraemos el nodo que "parece" estar más cerca de la meta
        h_actual, nodo_actual, camino = cola.pop(indice_mejor)
        
        if nodo_actual == objetivo:
            return camino

        # ==========================================
        # SECCIÓN 3: EXPANSIÓN Y EVALUACIÓN
        # ==========================================
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            print(f"[+] Visitando: {nodo_actual} (Distancia estimada a meta: {h_actual} km)")
            
            vecinos = grafo.get(nodo_actual, [])
            for vecino in vecinos:
                if vecino not in visitados:
                    
                    # Le preguntamos a nuestro "GPS" qué tan lejos parece estar este vecino
                    h_vecino = heuristica.get(vecino, float('inf'))
                    
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    
                    print(f"    -> ➕ Agregando '{vecino}' con h(n)={h_vecino}")
                    cola.append((h_vecino, vecino, nuevo_camino))
                    
    return None

# ==========================================
# SECCIÓN 4: ZONA DE PRUEBAS (Mapa de México)
# ==========================================

# Grafo de conexiones (quién conecta con quién por carretera)
grafo_mexico = {
    'Tepic': ['Guadalajara', 'Zacatecas'],
    'Zacatecas': ['Tepic', 'San Luis Potosi', 'Aguascalientes'],
    'Guadalajara': ['Tepic', 'Aguascalientes', 'Leon', 'Morelia'],
    'Aguascalientes': ['Zacatecas', 'Guadalajara', 'Leon'],
    'San Luis Potosi': ['Zacatecas', 'Queretaro'],
    'Leon': ['Guadalajara', 'Aguascalientes', 'Queretaro'],
    'Morelia': ['Guadalajara', 'Toluca'],
    'Queretaro': ['Leon', 'San Luis Potosi', 'CDMX'],
    'Toluca': ['Morelia', 'CDMX'],
    'CDMX': [] # Meta
}

# Nuestro "GPS" (h(n)): Estimación en línea recta desde cada ciudad hasta CDMX (en km).
heuristica_cdmx = {
    'Tepic': 640,
    'Zacatecas': 520,
    'Guadalajara': 460,
    'Aguascalientes': 430,
    'San Luis Potosi': 360,
    'Leon': 320,
    'Morelia': 220,
    'Queretaro': 190,
    'Toluca': 60,
    'CDMX': 0 # La meta está a 0 km de sí misma
}

nodo_inicio = 'Guadalajara'
nodo_meta = 'CDMX'

resultado = busqueda_voraz(grafo_mexico, heuristica_cdmx, nodo_inicio, nodo_meta)

if resultado:
    print(f"\n ¡ÉXITO! Meta '{nodo_meta}' encontrada.")
    print(f" Camino final: {' -> '.join(resultado)}")
else:
    print(f"\n La meta '{nodo_meta}' no se pudo alcanzar.")