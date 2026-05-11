def iteracion_de_valores(estados, recompensas, gamma, prob_exito, max_iteraciones=20):
    """
    TEMA 27: Algoritmo de Iteración de Valores para resolver un MDP.
    Propaga las recompensas por todo el mapa hasta que las utilidades convergen.
    """
    print("--- Iniciando Iteración de Valores ---")
    
    # 1. INICIALIZACIÓN: Al principio, el robot no sabe nada. 
    # La utilidad de todas las baldosas es 0.
    utilidades = {estado: 0.0 for estado in estados}
    
    # 2. EL CICLO DE ITERACIÓN (Las olas de propagación)
    for i in range(1, max_iteraciones + 1):
        # Creamos una copia en blanco para guardar los nuevos cálculos
        nuevas_utilidades = utilidades.copy()
        cambio_maximo = 0
        
        # Le aplicamos la Ecuación de Bellman a cada baldosa del pasillo
        for estado in estados:
            
            # Si es una celda final (Meta o Abismo), su valor es fijo. No cambia.
            if estado == 'Cargador (+100)' or estado == 'Abismo (-100)':
                nuevas_utilidades[estado] = recompensas[estado]
                continue
                
            # Evaluamos las dos acciones posibles: Ir a la Izquierda o a la Derecha
            # (Para simplificar el código del pasillo, codificaremos manualmente los vecinos)
            vecino_izq = estados[estados.index(estado) - 1] if estados.index(estado) > 0 else estado
            vecino_der = estados[estados.index(estado) + 1] if estados.index(estado) < len(estados) - 1 else estado
            
            # Calculamos la Utilidad Esperada si el robot decide ir a la IZQUIERDA
            eu_izquierda = (prob_exito * utilidades[vecino_izq]) + ((1 - prob_exito) * utilidades[estado])
            
            # Calculamos la Utilidad Esperada si el robot decide ir a la DERECHA
            eu_derecha = (prob_exito * utilidades[vecino_der]) + ((1 - prob_exito) * utilidades[estado])
            
            # MAX(a): El agente racional siempre elegirá la acción que le dé el mayor número
            mejor_futuro = max(eu_izquierda, eu_derecha)
            
            # LA ECUACIÓN DE BELLMAN COMPLETA: Recompensa local + (Gamma * Mejor futuro)
            nuevo_valor = recompensas[estado] + (gamma * mejor_futuro)
            
            # Verificamos qué tanto cambió el número respecto al turno anterior
            diferencia = abs(nuevo_valor - utilidades[estado])
            if diferencia > cambio_maximo:
                cambio_maximo = diferencia
                
            # Guardamos el nuevo valor en la baldosa
            nuevas_utilidades[estado] = nuevo_valor
            
        # Actualizamos el mapa oficial con los nuevos números
        utilidades = nuevas_utilidades
        
        # Mostramos cómo va cambiando el mapa en esta iteración
        valores_formateados = [f"{utilidades[e]:.1f}" for e in estados]
        print(f"Iteración {i:02d} | Mapa: {valores_formateados} | Cambio máx: {cambio_maximo:.2f}")
        
        # CONDICIÓN DE PARADA (Convergencia): Si los números ya casi no cambian, terminamos.
        if cambio_maximo < 0.01:
            print(f"\n El algoritmo ha convergido en la iteración {i}!")
            break
            
    return utilidades

# ==========================================
# ZONA DE PRUEBAS (El pasillo de la muerte)
# ==========================================

pasillo = ['Abismo (-100)', 'Baldosa A', 'Baldosa B', 'Cargador (+100)']

# Recompensas: El abismo es fatal, la meta es excelente. 
# Las baldosas normales gastan un poco de batería (-1) por estar ahí.
tabla_recompensas = {
    'Abismo (-100)': -100.0,
    'Baldosa A': -1.0,
    'Baldosa B': -1.0,
    'Cargador (+100)': 100.0
}

# Parámetros del MDP
factor_gamma = 0.9   # Las recompensas futuras valen 90% del presente
probabilidad = 0.8   # 80% de probabilidad de que las llantas no patinen

utilidades_finales = iteracion_de_valores(pasillo, tabla_recompensas, factor_gamma, probabilidad)

print("\n UTILIDADES FINALES DEL MAPA:")
for e in pasillo:
    print(f"  {e}: {utilidades_finales[e]:.2f} pts")