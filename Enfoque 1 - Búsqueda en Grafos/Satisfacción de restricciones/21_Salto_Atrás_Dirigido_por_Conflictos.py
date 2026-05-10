def resolver_csp_cbj(variables, dominios, fronteras, indice_actual=0, asignaciones=None, historial_conflictos=None):
    """
    TEMA 21: Salto Atrás Dirigido por Conflictos.
    Si falla, salta directamente a la variable que causó el conflicto más reciente.
    """
    if asignaciones is None: asignaciones = {}
    if historial_conflictos is None: historial_conflictos = {v: set() for v in variables}

    # 1. PRUEBA DE META
    if indice_actual == len(variables):
        return True, None  # Exito total, no hay saltos pendientes

    estado_actual = variables[indice_actual]
    historial_conflictos[estado_actual] = set() # Reiniciamos su historial
    
    print(f"\n[?] Intentando pintar: {estado_actual}")

    # 2. PROBAR COLORES
    for color in dominios:
        # Encontrar quiénes de mis vecinos en el PASADO me bloquean este color
        vecinos_culpables = [
            pasado for pasado in variables[:indice_actual] 
            if pasado in fronteras.get(estado_actual, []) and asignaciones.get(pasado) == color
        ]
        
        if vecinos_culpables:
            print(f"  [x] '{color}' rechazado. Culpables: {vecinos_culpables}")
            # Anotamos a los culpables en nuestro historial de conflictos
            for culpable in vecinos_culpables:
                historial_conflictos[estado_actual].add(culpable)
            continue # Intentamos el siguiente color
            
        # Si el color es válido, lo asignamos
        print(f"  [+] ÉXITO. {estado_actual} se pintó de {color}")
        asignaciones[estado_actual] = color
        
        # Avanzamos al siguiente estado (Recursión)
        exito, salto_hacia = resolver_csp_cbj(variables, dominios, fronteras, indice_actual + 1, asignaciones, historial_conflictos)
        
        if exito:
            return True, None
            
        # ==========================================
        # EL MOTOR DE SALTO (BACKJUMPING)
        # ==========================================
        # Si el código de adelante falló y pidió un salto...
        if salto_hacia and salto_hacia != estado_actual:
            print(f"   {estado_actual} ignorado. Saltando por encima de mí hacia: {salto_hacia}")
            del asignaciones[estado_actual]
            
            # Le pasamos nuestros conflictos al estado al que estamos saltando para que no los olvide
            historial_conflictos[salto_hacia].update(historial_conflictos[estado_actual])
            
            # ¡Retornamos inmediatamente! (No intentamos más colores, simplemente saltamos)
            return False, salto_hacia
            
        # Si el salto era hacia mí, me quito el color e intento el siguiente en el ciclo 'for'
        print(f" Aterrizaje de salto en {estado_actual}. Intentaré otro color.")
        del asignaciones[estado_actual]

    # 3. SI TODOS LOS COLORES FALLARON, DECIDIR A DÓNDE SALTAR
    if not historial_conflictos[estado_actual]:
        return False, None # Callejón sin salida total
        
    # Buscamos al culpable que hayamos pintado más recientemente
    # (El que tenga el índice más alto en nuestra lista de variables)
    culpable_mas_reciente = max(historial_conflictos[estado_actual], key=lambda x: variables.index(x))
    
    print(f"  [💥] {estado_actual} se quedó sin opciones. Iniciando SALTO a su culpable directo: {culpable_mas_reciente}")
    
    # Le pasamos el resto de nuestros conflictos a ese culpable
    conflictos_heredados = [c for c in historial_conflictos[estado_actual] if c != culpable_mas_reciente]
    historial_conflictos[culpable_mas_reciente].update(conflictos_heredados)
    
    return False, culpable_mas_reciente

# ==========================================
# ZONA DE PRUEBAS (El mapa trampa)
# ==========================================

# Variables ordenadas (El algoritmo las procesará en este orden)
estados = ['Camisa', 'Pantalones', 'Calcetines', 'Sombrero']

# Solo tenemos dos colores
colores = ['Rojo', 'Azul']

# Restricciones:
# - El Sombrero no puede ser del mismo color que la Camisa.
# - El Sombrero no puede ser del mismo color que los Pantalones.
# - ¡Los calcetines no tienen restricciones con nadie!
restricciones = {
    'Camisa': ['Sombrero'],
    'Pantalones': ['Sombrero'],
    'Calcetines': [], # Completamente independientes
    'Sombrero': ['Camisa', 'Pantalones']
}

print("--- Iniciando Salto Atrás Dirigido por Conflictos ---")
asignaciones_finales = {}
exito, _ = resolver_csp_cbj(estados, colores, restricciones, 0, asignaciones_finales)

if exito:
    print("\n ¡ATUENDO SELECCIONADO CON ÉXITO!")
    for prenda, color in asignaciones_finales.items():
        print(f" {prenda}: {color}")
else:
    print("\n Es imposible combinar este atuendo.")