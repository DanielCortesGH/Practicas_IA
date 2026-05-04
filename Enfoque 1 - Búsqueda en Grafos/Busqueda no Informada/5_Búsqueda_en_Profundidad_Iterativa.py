# ==========================================
# FUNCIÓN 1: El Freno de Mano modificado
# ==========================================
def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    pila = [[inicio]]
    
    # Esta bandera nos avisará si en algún momento quisimos bajar 
    # pero el 'limite' nos detuvo.
    hubo_corte = False 

    while len(pila) > 0:
        camino_actual = pila.pop()
        nodo_actual = camino_actual[-1]

        if nodo_actual == objetivo:
            return camino_actual, False # Encontrado, no importan los cortes

        profundidad_actual = len(camino_actual) - 1

        if profundidad_actual < limite:
            vecinos = grafo.get(nodo_actual, [])
            for vecino in reversed(vecinos):
                if vecino not in camino_actual:
                    nuevo_camino = list(camino_actual)
                    nuevo_camino.append(vecino)
                    pila.append(nuevo_camino)
        else:
            # Si entramos aquí, significa que queríamos seguir bajando pero el límite 
            # no nos dejó. Activamos la alarma.
            hubo_corte = True 

    # Retorna None (no lo encontró) y el estado de la alarma
    return None, hubo_corte 

# ==========================================
# FUNCIÓN 2: El Algoritmo Iterativo (El motor principal)
# ==========================================
def busqueda_profundidad_iterativa(grafo, inicio, objetivo, limite_maximo=100):
    """
    Ejecuta múltiples búsquedas de profundidad limitada, 
    aumentando el límite en +1 en cada ciclo.
    """
    print(f"Iniciando Búsqueda Iterativa desde '{inicio}' hasta '{objetivo}'\n")

    # El ciclo 'for' va desde 0 hasta el límite máximo de seguridad
    for limite_actual in range(limite_maximo):
        print(f" Intentando con límite de profundidad: {limite_actual}")
        
        # Mandamos al explorador con el límite actual
        resultado, hubo_corte = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite_actual)
        
        if resultado is not None:
            # ¡Éxito! Encontramos la ruta. Rompemos el ciclo y la regresamos.
            return resultado
        
        if not hubo_corte:
            # ¡Atención aquí! Si NO encontramos la meta, y NO hubo corte de límite,
            # significa que el algoritmo revisó el 100% de las ramas del grafo y 
            # concluyó que la meta simplemente no existe. Detenemos todo para no hacer ciclos inútiles.
            print("⚠️ Se exploró todo el grafo posible y no se encontró la meta.")
            break 

    # Si llega hasta el límite_maximo (ej. 100) y no encontró nada
    return None

# ==========================================
# Zona de Pruebas
# ==========================================
grafo_prueba = {
    'A': ['B', 'C'],
    'B': ['D'],
    'D': ['E'],
    'E': ['F'], 
    'C': ['H'],
    'H': ['I'],
    'I': ['J'], 
    'J': []
}

ruta_final = busqueda_profundidad_iterativa(grafo_prueba, 'A', 'J')

if ruta_final:
    print(f"\n ¡Objetivo alcanzado!")
    print(f" Camino: {' -> '.join(ruta_final)}")
else:
    print("\n Fracaso en la búsqueda.")