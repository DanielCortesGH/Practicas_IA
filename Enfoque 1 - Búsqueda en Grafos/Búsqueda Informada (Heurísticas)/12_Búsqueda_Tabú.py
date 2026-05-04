def busqueda_tabu(estado_inicial, evaluar, obtener_vecinos, tamaño_tabu, max_iteraciones):
    """
    Algoritmo de Búsqueda Tabú.
    Permite movimientos hacia abajo para escapar de máximos locales,
    usando una memoria a corto plazo (Lista Tabú) para no repetir errores recientes.
    """
    print(f"--- Iniciando Búsqueda Tabú (Punto de partida: {estado_inicial}) ---\n")
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    estado_actual = estado_inicial
    
    # A diferencia de Hill Climbing, aquí vagaremos por el mapa, 
    # así que debemos guardar la MEJOR cima que hayamos visto en todo el viaje.
    mejor_global = estado_actual
    valor_mejor_global = evaluar(estado_actual)
    
    # Nuestra memoria a corto plazo (una lista estándar)
    lista_tabu = []

    # ==========================================
    # SECCIÓN 2: CICLO DE EXPLORACIÓN
    # ==========================================
    for iteracion in range(max_iteraciones):
        valor_actual = evaluar(estado_actual)
        print(f"[Iteración {iteracion}] Posición: {estado_actual} | Altura: {valor_actual}")
        
        vecinos = obtener_vecinos(estado_actual)
        
        # Filtramos a los vecinos: Solo podemos ir a los que NO están prohibidos
        vecinos_permitidos = []
        for v in vecinos:
            if v not in lista_tabu:
                vecinos_permitidos.append(v)
                
        if len(vecinos_permitidos) == 0:
            print("🛑 Atrapado: Todos los vecinos están en la Lista Tabú.")
            break

        # ==========================================
        # SECCIÓN 3: ELEGIR EL MEJOR VECINO PERMITIDO
        # ==========================================
        # Buscamos el mejor vecino (incluso si su altura es MENOR que la nuestra)
        mejor_vecino = vecinos_permitidos[0]
        mejor_valor_vecino = evaluar(mejor_vecino)
        
        for v in vecinos_permitidos[1:]:
            val = evaluar(v)
            if val > mejor_valor_vecino:
                mejor_valor_vecino = val
                mejor_vecino = v
                
        # Damos el paso, sea para arriba o para abajo
        estado_actual = mejor_vecino
        
        # Si este nuevo lugar es el más alto que hemos visto en toda la historia, lo guardamos
        if evaluar(estado_actual) > valor_mejor_global:
            mejor_global = estado_actual
            valor_mejor_global = evaluar(estado_actual)
            print(f"    🌟 ¡NUEVO RÉCORD GLOBAL ENCONTRADO! Altura: {valor_mejor_global}")

        # ==========================================
        # SECCIÓN 4: ACTUALIZAR LA LISTA TABÚ
        # ==========================================
        # Prohibimos regresar al lugar del que acabamos de venir
        lista_tabu.append(estado_actual)
        
        # Si la lista se llena, olvidamos el recuerdo más viejo (FIFO)
        if len(lista_tabu) > tamaño_tabu:
            lista_tabu.pop(0)

    print(f"\n✅ Búsqueda terminada tras {max_iteraciones} iteraciones.")
    return mejor_global, valor_mejor_global

# ==========================================
# ZONA DE PRUEBAS (El mapa engañoso)
# ==========================================

# Nuestro terreno es una lista de alturas.
# Índices:   0  1  2  3  4  5  6  7  8   9  10
terreno =   [2, 4, 7, 4, 2, 1, 3, 6, 10, 8, 5]
# Fíjate que en el índice 2 hay una cima de altura 7.
# Pero en el índice 8 está la verdadera montaña de altura 10.

def evaluar_terreno(posicion):
    return terreno[posicion]

def vecinos_terreno(posicion):
    vecinos = []
    # Podemos dar un paso a la izquierda o a la derecha, sin salirnos de la lista
    if posicion > 0:
        vecinos.append(posicion - 1)
    if posicion < len(terreno) - 1:
        vecinos.append(posicion + 1)
    return vecinos

# ¡Aterrizamos en el índice 1!
punto_de_partida = 1 
limite_tabu = 2 # Recordará los últimos 2 pasos
intentos = 10

mejor_posicion, mejor_altura = busqueda_tabu(
    punto_de_partida, 
    evaluar_terreno, 
    vecinos_terreno, 
    limite_tabu, 
    intentos
)

print(f"\n El punto más alto descubierto fue el índice {mejor_posicion} con una altura de {mejor_altura}.")