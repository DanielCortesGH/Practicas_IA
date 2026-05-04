def busqueda_online_lrta(entorno_real, heuristica_memoria, inicio, meta, max_pasos=50):
    """
    Algoritmo LRTA* (Learning Real-Time A*).
    Simula un agente físico que descubre el mundo paso a paso 
    y actualiza sus estimaciones (h) basándose en la experiencia.
    """
    print(f"--- Iniciando Búsqueda Online LRTA* (Inicio: {inicio}) ---\n")
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    estado_actual = inicio
    camino_recorrido = [inicio] # El rastro de por dónde ha caminado el robot

    # ==========================================
    # SECCIÓN 2: CICLO DE ACCIÓN (Paso a paso en tiempo real)
    # ==========================================
    for paso in range(1, max_pasos + 1):
        
        if estado_actual == meta:
            print(f"\n✅ ¡Objetivo '{meta}' alcanzado físicamente en {paso-1} pasos!")
            return camino_recorrido

        # El robot "abre los ojos" y ve qué caminos hay desde su posición actual
        # (Esto simula los sensores del robot en el entorno real)
        vecinos_visibles = entorno_real.get(estado_actual, {})

        if not vecinos_visibles:
            print(" ¡Atrapado en un callejón sin salida y sin retorno!")
            break

        # ==========================================
        # SECCIÓN 3: EVALUACIÓN Y APRENDIZAJE
        # ==========================================
        mejor_vecino = None
        menor_costo_estimado = float('inf')

        # Calculamos f(n) = costo_real_del_paso + estimacion_del_vecino
        for vecino, costo_real in vecinos_visibles.items():
            
            # Leemos la libreta. Si no conocemos al vecino, asumimos infinito por seguridad.
            h_vecino = heuristica_memoria.get(vecino, float('inf'))
            costo_total_f = costo_real + h_vecino
            
            if costo_total_f < menor_costo_estimado:
                menor_costo_estimado = costo_total_f
                mejor_vecino = vecino

        # ¡LA MAGIA DEL APRENDIZAJE!
        # Si el robot se da cuenta de que la mejor salida desde donde está 
        # es "peor" de lo que él creía originalmente, actualiza su libreta 
        # para no volver a engañarse en el futuro si tiene que regresar.
        if menor_costo_estimado > heuristica_memoria[estado_actual]:
            print(f"     [Aprendizaje] Actualizando mapa mental de '{estado_actual}': "
                  f"de {heuristica_memoria[estado_actual]} a {menor_costo_estimado}")
            heuristica_memoria[estado_actual] = menor_costo_estimado

        # ==========================================
        # SECCIÓN 4: EJECUCIÓN DEL MOVIMIENTO
        # ==========================================
        print(f"[{paso}]  El robot se mueve físicamente: {estado_actual} -> {mejor_vecino}")
        estado_actual = mejor_vecino
        camino_recorrido.append(estado_actual)

    print("\n El robot agotó su batería (límite de pasos) antes de encontrar la meta.")
    return camino_recorrido

# ==========================================
# ZONA DE PRUEBAS (El laberinto engañoso)
# ==========================================

# Nuestro entorno físico bidireccional (costo 1 por cada movimiento)
# Nota: La rama de la 'B' es una trampa. Parece llevarte lejos, pero 'D' no tiene salida.
mundo_real = {
    'A': {'B': 1, 'C': 1},
    'B': {'A': 1, 'D': 1}, # Camino engañoso
    'D': {'B': 1},         # ¡Callejón sin salida (Pared)!
    'C': {'A': 1, 'E': 1}, # El camino correcto
    'E': {'C': 1}          # Meta
}

# La intuición inicial del robot (su "GPS").
# Fíjate que el robot cree que 'B' (1) está más cerca de la meta que 'C' (3).
# ¡Esa intuición errónea lo meterá directo en la trampa!
libreta_del_robot = {
    'A': 2,
    'B': 1, # Se ve tentador...
    'D': 0, # Parece la meta, pero es una trampa
    'C': 3, # Se ve feo, pero es el camino real
    'E': 0  # Meta real
}

ruta_fisica = busqueda_online_lrta(mundo_real, libreta_del_robot, 'A', 'E')

print(f" Rastro físico final: {' -> '.join(ruta_fisica)}")