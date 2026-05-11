def obtener_vecino_segun_accion(estado_actual, accion, todos_los_estados):
    """Devuelve a qué estado llegarías si intentas una acción."""
    indice = todos_los_estados.index(estado_actual)
    if accion == 'Izquierda' and indice > 0:
        return todos_los_estados[indice - 1]
    elif accion == 'Derecha' and indice < len(todos_los_estados) - 1:
        return todos_los_estados[indice + 1]
    return estado_actual # Chocó con pared

def evaluar_politica(politica_actual, utilidades, estados, recompensas, gamma, prob_exito, iteraciones_eval=10):
    """
    FASE 1: Evaluar la Política.
    Calcula los números de Utilidad (U) ASUMIENDO que el robot obedece ciegamente la política actual.
    No busca el 'max(a)', solo sigue la flecha que le toca.
    """
    for _ in range(iteraciones_eval):
        nuevas_utilidades = utilidades.copy()
        
        for estado in estados:
            if estado == 'Abismo (-100)' or estado == 'Cargador (+100)':
                continue # Los finales no cambian
                
            # ¿Qué dice la política que debemos hacer aquí?
            accion_dictada = politica_actual[estado]
            vecino_destino = obtener_vecino_segun_accion(estado, accion_dictada, estados)
            
            # Calculamos la Utilidad Esperada siguiendo ESTRICTAMENTE esa acción
            eu_accion = (prob_exito * utilidades[vecino_destino]) + ((1 - prob_exito) * utilidades[estado])
            
            # Actualizamos el valor de la baldosa (Ecuación de Bellman sin el 'max')
            nuevas_utilidades[estado] = recompensas[estado] + (gamma * eu_accion)
            
        utilidades = nuevas_utilidades
        
    return utilidades

def iteracion_de_politicas(estados, recompensas, gamma, prob_exito):
    """
    TEMA 28: El ciclo principal que alterna entre Evaluar y Mejorar.
    """
    print("--- Iniciando Iteración de Políticas ---")
    
    # 1. INICIALIZACIÓN: 
    utilidades = {e: 0.0 for e in estados}
    utilidades['Abismo (-100)'] = recompensas['Abismo (-100)']
    utilidades['Cargador (+100)'] = recompensas['Cargador (+100)']
    
    # Empezamos con una política TERRIBLE y testaruda (Todo a la izquierda)
    politica = {'Baldosa A': 'Izquierda', 'Baldosa B': 'Izquierda'}
    
    acciones_posibles = ['Izquierda', 'Derecha']
    politica_estable = False
    paso = 1

    while not politica_estable:
        print(f"\n[Ciclo {paso}] Política actual: {politica}")
        
        # FASE 1: Evaluar qué tan buena (o mala) es esta política
        utilidades = evaluar_politica(politica, utilidades, estados, recompensas, gamma, prob_exito)
        print(f"  -> Utilidades evaluadas: A={utilidades['Baldosa A']:.1f}, B={utilidades['Baldosa B']:.1f}")

        politica_estable = True # Asumimos que es perfecta hasta que demostremos lo contrario
        
        # FASE 2: Mejorar la Política (Buscando rebeliones)
        for estado in ['Baldosa A', 'Baldosa B']:
            accion_actual = politica[estado]
            mejor_accion = accion_actual
            max_eu = -float('inf')
            
            # El robot se pregunta: "¿Qué pasaría si desobedezco mi política y pruebo otra acción?"
            for accion_rebelde in acciones_posibles:
                vecino_destino = obtener_vecino_segun_accion(estado, accion_rebelde, estados)
                eu_rebelde = (prob_exito * utilidades[vecino_destino]) + ((1 - prob_exito) * utilidades[estado])
                
                if eu_rebelde > max_eu:
                    max_eu = eu_rebelde
                    mejor_accion = accion_rebelde
            
            # Si desobedecer da un mejor resultado matemático, ¡cambiamos la política oficial!
            if mejor_accion != accion_actual:
                print(f"  [!] Mejora detectada en '{estado}': '{accion_actual}' era mala, cambiamos a '{mejor_accion}'")
                politica[estado] = mejor_accion
                politica_estable = False
                
        paso += 1

    print("\n✅ La política ha convergido. ¡Es la estrategia óptima!")
    return politica, utilidades

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

pasillo = ['Abismo (-100)', 'Baldosa A', 'Baldosa B', 'Cargador (+100)']

tabla_recompensas = {
    'Abismo (-100)': -100.0,
    'Baldosa A': -1.0,
    'Baldosa B': -1.0,
    'Cargador (+100)': 100.0
}

factor_gamma = 0.9
probabilidad = 0.8

politica_final, utilidades_finales = iteracion_de_politicas(pasillo, tabla_recompensas, factor_gamma, probabilidad)

print("\n RESULTADO FINAL DEL ENTRENAMIENTO:")
for estado in ['Baldosa A', 'Baldosa B']:
    print(f"  Si estás en {estado} -> Debes ir a la {politica_final[estado]}")