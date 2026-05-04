def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    """
    Realiza una Búsqueda en Profundidad pero se detiene 
    al alcanzar una profundidad máxima especificada.
    """
    
    # Nuestra Pila que guarda los caminos por explorar
    pila = [[inicio]]

    # Ciclo principal (LIFO - Saca el último)
    while len(pila) > 0:
        camino_actual = pila.pop()
        nodo_actual = camino_actual[-1]

        # Prueba de Meta
        if nodo_actual == objetivo:
            return camino_actual

        # ==========================================
        # EL FRENO DE MANO (Límite de Profundidad)
        # ==========================================
        # Calculamos a qué profundidad estamos. 
        # Si el camino es ['A'], la longitud es 1, profundidad 0 (Inicio).
        # Si el camino es ['A', 'B'], la longitud es 2, profundidad 1.
        profundidad_actual = len(camino_actual) - 1

        # Solo expandimos vecinos si NO hemos llegado al límite
        if profundidad_actual < limite:
            
            vecinos = grafo.get(nodo_actual, [])

            for vecino in reversed(vecinos):
                # Para evitar bucles infinitos (como A -> B -> A),
                # solo aseguramos que el vecino no esté ya en nuestro camino actual.
                if vecino not in camino_actual:
                    
                    nuevo_camino = list(camino_actual)
                    nuevo_camino.append(vecino)
                    
                    pila.append(nuevo_camino)

    # Si se agota la pila y nunca encontramos el objetivo dentro del límite
    return None

# ==========================================
# Zona de Pruebas: El efecto del Límite
# ==========================================

# Un grafo donde la meta (J) está profunda por la rama C (Profundidad 3)
# Pero B tiene una rama trampa casi infinita (D -> E -> F -> G...)
grafo_prueba = {
    'A': ['B', 'C'],
    'B': ['D'],
    'D': ['E'],
    'E': ['F'],
    'F': ['G'], # ... Rama inútil y profunda
    'C': ['H'],
    'H': ['I'],
    'I': ['J'], # <- Meta real (Profundidad 3 desde A)
    'J': []
}

nodo_inicio = 'A'
nodo_meta = 'J'

print("--- Ejecutando Búsqueda en Profundidad Limitada ---")

# PRUEBA 1: Límite muy corto (se rinde antes de llegar)
limite_corto = 2
resultado_1 = busqueda_profundidad_limitada(grafo_prueba, nodo_inicio, nodo_meta, limite_corto)
print(f"\nCon límite {limite_corto}:")
if resultado_1:
    print(f" Encontrado: {' -> '.join(resultado_1)}")
else:
    print(" No se encontró (El algoritmo fue detenido por el límite).")

# PRUEBA 2: Límite exacto/suficiente
limite_correcto = 4
resultado_2 = busqueda_profundidad_limitada(grafo_prueba, nodo_inicio, nodo_meta, limite_correcto)
print(f"\nCon límite {limite_correcto}:")
if resultado_2:
    print(f" Encontrado: {' -> '.join(resultado_2)}")
else:
    print(" No se encontró.")