def ascension_de_colinas(estado_inicial, funcion_evaluacion, generar_vecinos):
    """
    Algoritmo Hill Climbing.
    Siempre se mueve hacia el vecino con el mayor valor.
    Se detiene cuando ningún vecino es mejor que su posición actual.
    """
    print(f"--- Iniciando Ascensión de Colinas (Punto de partida: {estado_inicial}) ---\n")
    
    # 1. Comenzamos en el estado inicial
    estado_actual = estado_inicial
    valor_actual = funcion_evaluacion(estado_actual)
    
    pasos = 0

    # 2. Ciclo infinito (hasta encontrar la cima)
    while True:
        print(f"[Paso {pasos}] Posición actual: {estado_actual} | Altura: {valor_actual}")
        
        # Obtenemos los vecinos inmediatos
        vecinos = generar_vecinos(estado_actual)
        
        # Buscamos al mejor vecino
        mejor_vecino = None
        mejor_valor_vecino = -float('inf')
        
        for vecino in vecinos:
            valor_vecino = funcion_evaluacion(vecino)
            if valor_vecino > mejor_valor_vecino:
                mejor_valor_vecino = valor_vecino
                mejor_vecino = vecino
                
        # 3. La regla de la Ascensión de Colinas:
        # Si el mejor vecino que encontramos NO es más alto que donde estamos parados...
        # ¡Significa que estamos en una cima! Terminamos.
        if mejor_valor_vecino <= valor_actual:
            print(f"\n✅ ¡Cima alcanzada! Ningún vecino es más alto.")
            print(f"📍 Cima encontrada en: {estado_actual} (Altura: {valor_actual})")
            return estado_actual, valor_actual
            
        # Si el vecino es más alto, damos el paso y repetimos el ciclo
        print(f"    -> ⬆️ Subiendo hacia: {mejor_vecino} (Altura: {mejor_valor_vecino})\n")
        estado_actual = mejor_vecino
        valor_actual = mejor_valor_vecino
        pasos += 1

# ==========================================
# ZONA DE PRUEBAS (El problema de la montaña matemática)
# ==========================================

# Imagina que estamos en un eje X. La "altura" de la montaña está dada por 
# una función matemática sencilla de parábola invertida: f(x) = -(x - 5)^2 + 20
# El punto más alto real de esta montaña está exactamente en x = 5 (Altura = 20)
def evaluar_altura(x):
    return -(x - 5)**2 + 20

# Los vecinos de un punto en X son simplemente dar un paso a la derecha (+1) o a la izquierda (-1)
def mis_vecinos(x):
    return [x - 1, x + 1]

# ¡Te tiran en paracaídas en la posición x = 1!
punto_de_partida = 1 

cima_x, cima_altura = ascension_de_colinas(punto_de_partida, evaluar_altura, mis_vecinos)