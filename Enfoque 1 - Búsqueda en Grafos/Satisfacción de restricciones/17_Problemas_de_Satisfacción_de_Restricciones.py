def es_color_valido(estado, color_propuesto, asignaciones_actuales, grafo_vecinos):
    """
    Verifica las restricciones (Constraints).
    Revisa si alguno de los vecinos del estado ya tiene el color propuesto.
    """
    vecinos = grafo_vecinos.get(estado, [])
    
    for vecino in vecinos:
        # Si el vecino ya está pintado Y tiene el mismo color, rompimos la regla
        if vecino in asignaciones_actuales and asignaciones_actuales[vecino] == color_propuesto:
            return False
            
    # Si ningún vecino tiene ese color, es un movimiento válido
    return True

def resolver_csp_backtracking(variables, dominios, grafo_vecinos, asignaciones={}):
    """
    Algoritmo de Backtracking para Satisfacción de Restricciones.
    Utiliza recursividad para ir asignando valores y retroceder si se equivoca.
    """
    # 1. PRUEBA DE META: Si ya asignamos color a todas las variables, ¡ganamos!
    if len(asignaciones) == len(variables):
        return asignaciones

    # 2. SELECCIÓN DE VARIABLE: Tomamos la primera que aún no tenga color
    estados_sin_pintar = [v for v in variables if v not in asignaciones]
    estado_actual = estados_sin_pintar[0]

    print(f"\n[?] Intentando pintar: {estado_actual}")

    # 3. PROBAR VALORES DEL DOMINIO: Intentamos con cada color disponible
    for color in dominios:
        print(f"  -> Probando color '{color}' para {estado_actual}...")
        
        # ¿Rompe alguna regla?
        if es_color_valido(estado_actual, color, asignaciones, grafo_vecinos):
            print(f"  [+] ÉXITO. {estado_actual} se pintó de {color}")
            
            # Aplicamos el color
            asignaciones[estado_actual] = color

            # Magia Recursiva: Llamamos a la función de nuevo para pintar el siguiente estado
            resultado = resolver_csp_backtracking(variables, dominios, grafo_vecinos, asignaciones)
            
            # Si el resultado no es None, significa que logramos pintar todo el mapa hasta el final
            if resultado is not None:
                return resultado

            # ==========================================
            # BACKTRACKING (EL RETROCESO)
            # ==========================================
            # Si llegamos a esta línea, significa que pintar este estado de este color 
            # causó un callejón sin salida más adelante. ¡Tenemos que borrarlo e intentar otro!
            print(f"  [-] ERROR A FUTURO. Borrando '{color}' de {estado_actual} (Backtracking)")
            del asignaciones[estado_actual]
            
        else:
            print(f"  [x] RECHAZADO. Conflicto de reglas. Un vecino ya es {color}.")

    # Si probamos todos los colores y ninguno sirvió, regresamos None para avisarle 
    # al estado anterior que él fue el que cometió el error y debe cambiar su color.
    return None

# ==========================================
# ZONA DE PRUEBAS (Coloreando el Centro/Occidente)
# ==========================================

# Nuestras Variables (X)
estados_mexico = [
    'Jalisco', 'Nayarit', 'Zacatecas', 
    'Aguascalientes', 'Guanajuato', 'Michoacan', 'Colima'
]

# Nuestro Dominio (D): Solo tenemos 3 latas de pintura
colores_disponibles = ['Rojo', 'Verde', 'Azul']

# Nuestras Restricciones (C): Quién colinda con quién
fronteras = {
    'Jalisco': ['Nayarit', 'Zacatecas', 'Aguascalientes', 'Guanajuato', 'Michoacan', 'Colima'],
    'Nayarit': ['Jalisco', 'Zacatecas'],
    'Zacatecas': ['Nayarit', 'Jalisco', 'Aguascalientes'],
    'Aguascalientes': ['Zacatecas', 'Jalisco'],
    'Guanajuato': ['Jalisco', 'Michoacan'],
    'Michoacan': ['Jalisco', 'Guanajuato', 'Colima'],
    'Colima': ['Jalisco', 'Michoacan']
}

print("--- Iniciando Resolución CSP (Pintado de Mapa) ---")

# Iniciamos con el diccionario de asignaciones vacío {}
mapa_resuelto = resolver_csp_backtracking(estados_mexico, colores_disponibles, fronteras, {})

if mapa_resuelto:
    print("\n ¡MAPA COLOREADO EXITOSAMENTE SIN ROMPER REGLAS!")
    for estado, color in mapa_resuelto.items():
        print(f" {estado}: {color}")
else:
    print("\n Es imposible pintar este mapa con los colores dados.")