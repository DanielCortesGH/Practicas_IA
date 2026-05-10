import random

def contar_conflictos(estado, color_propuesto, asignaciones, fronteras):
    """
    Cuenta cuántos vecinos del 'estado' tienen actualmente el 'color_propuesto'.
    Si el número es 0, significa que el color es perfecto.
    """
    conflictos = 0
    for vecino in fronteras.get(estado, []):
        if asignaciones[vecino] == color_propuesto:
            conflictos += 1
    return conflictos

def obtener_estados_en_conflicto(variables, asignaciones, fronteras):
    """Devuelve una lista con todos los estados que están rompiendo las reglas."""
    estados_conflictivos = []
    for estado in variables:
        color_actual = asignaciones[estado]
        if contar_conflictos(estado, color_actual, asignaciones, fronteras) > 0:
            estados_conflictivos.append(estado)
    return estados_conflictivos

def resolver_csp_minimos_conflictos(variables, dominios, fronteras, max_pasos=100):
    """
    TEMA 22: Algoritmo de Mínimos-Conflictos.
    Repara iterativamente una asignación completa pero defectuosa.
    """
    print("--- Iniciando Búsqueda Local: Mínimos-Conflictos ---\n")
    
    # ==========================================
    # SECCIÓN 1: ASIGNACIÓN ALEATORIA INICIAL
    # ==========================================
    asignaciones = {}
    for estado in variables:
        asignaciones[estado] = random.choice(dominios)
        
    print("Estado inicial (Completamente aleatorio y probablemente erróneo):")
    for estado, color in asignaciones.items():
        print(f"  {estado}: {color}")
    print("-" * 30)

    # ==========================================
    # SECCIÓN 2: EL CICLO DE REPARACIÓN
    # ==========================================
    for paso in range(1, max_pasos + 1):
        estados_rotos = obtener_estados_en_conflicto(variables, asignaciones, fronteras)
        
        # PRUEBA DE META: Si la lista de estados rotos está vacía, ¡ganamos!
        if not estados_rotos:
            print(f"\n✅ ¡MAPA ARREGLADO EXITOSAMENTE en el paso {paso-1}!")
            return asignaciones
            
        # 1. Elegimos un estado problemático al azar para repararlo
        estado_a_reparar = random.choice(estados_rotos)
        
        print(f"[Paso {paso}] Reparando '{estado_a_reparar}'...")

        # 2. Buscar el color que minimice los conflictos
        mejor_color = None
        min_conflictos_encontrados = float('inf')
        colores_empatados = []
        
        for color in dominios:
            conflictos = contar_conflictos(estado_a_reparar, color, asignaciones, fronteras)
            
            if conflictos < min_conflictos_encontrados:
                min_conflictos_encontrados = conflictos
                colores_empatados = [color] # Nuevo récord, reiniciamos la lista de empates
            elif conflictos == min_conflictos_encontrados:
                colores_empatados.append(color) # Empate
                
        # Si hay varios colores que causan los mismos conflictos, elegimos uno al azar
        mejor_color = random.choice(colores_empatados)
        
        # 3. Aplicamos la reparación
        color_anterior = asignaciones[estado_a_reparar]
        asignaciones[estado_a_reparar] = mejor_color
        print(f"    -> Cambiando {color_anterior} a {mejor_color} (Causa {min_conflictos_encontrados} conflictos)")

    print(f"\n Se alcanzó el límite de {max_pasos} pasos y no se pudo resolver.")
    return None

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

estados_mexico = ['Jalisco', 'Nayarit', 'Zacatecas', 'Aguascalientes', 'Guanajuato', 'Michoacan', 'Colima']
colores_disponibles = ['Rojo', 'Verde', 'Azul']

fronteras = {
    'Jalisco': ['Nayarit', 'Zacatecas', 'Aguascalientes', 'Guanajuato', 'Michoacan', 'Colima'],
    'Nayarit': ['Jalisco', 'Zacatecas'],
    'Zacatecas': ['Nayarit', 'Jalisco', 'Aguascalientes'],
    'Aguascalientes': ['Zacatecas', 'Jalisco'],
    'Guanajuato': ['Jalisco', 'Michoacan'],
    'Michoacan': ['Jalisco', 'Guanajuato', 'Colima'],
    'Colima': ['Jalisco', 'Michoacan']
}

mapa_resuelto = resolver_csp_minimos_conflictos(estados_mexico, colores_disponibles, fronteras)

if mapa_resuelto:
    print("\n Solución Final:")
    for estado, color in mapa_resuelto.items():
        print(f"  {estado}: {color}")