def prediccion_temporal_estacionaria(estado_inicial, modelo_transicion, dias_a_predecir):
    """
    TEMA 46: Simula la evolución de un proceso estacionario en el tiempo.
    Usa la MISMA matriz de transición (modelo_transicion) en cada paso del bucle.
    """
    print("--- Iniciando Predicción Temporal (Proceso Estacionario) ---")
    
    # El vector de creencia actual. Día 0: 100% seguros de que es 'Optimo'
    creencia_actual = estado_inicial
    estados = list(creencia_actual.keys())
    
    for t in range(1, dias_a_predecir + 1):
        # Creamos un vector en blanco para el nuevo día
        nueva_creencia = {estado: 0.0 for estado in estados}
        
        # PREDICCIÓN: P(X_t) = Sumatoria de P(X_t | X_t-1) * P(X_t-1)
        for estado_futuro in estados:
            prob_acumulada = 0.0
            for estado_pasado in estados:
                # LA CLAVE ESTACIONARIA: Usamos el mismo modelo sin importar 't'
                prob_transicion = modelo_transicion[estado_pasado][estado_futuro]
                prob_acumulada += prob_transicion * creencia_actual[estado_pasado]
                
            nueva_creencia[estado_futuro] = prob_acumulada
            
        # Actualizamos nuestra creencia y avanzamos el reloj
        creencia_actual = nueva_creencia
        
        # Formateamos la salida para ver la evolución
        str_creencia = " | ".join([f"{k}: {v*100:.1f}%" for k, v in creencia_actual.items()])
        print(f"Día {t:02d} -> {str_creencia}")

    return creencia_actual

# ==========================================
# ZONA DE PRUEBAS (El Servomotor)
# ==========================================

# Vector de creencia inicial (Día 0)
estado_dia_cero = {'Optimo': 1.0, 'Con_Ruido': 0.0, 'Fallo': 0.0}

# LA MATRIZ DE TRANSICIÓN ESTACIONARIA (No cambia nunca)
fisica_del_motor = {
    'Optimo':    {'Optimo': 0.85, 'Con_Ruido': 0.15, 'Fallo': 0.00},
    'Con_Ruido': {'Optimo': 0.10, 'Con_Ruido': 0.70, 'Fallo': 0.20},
    'Fallo':     {'Optimo': 0.00, 'Con_Ruido': 0.00, 'Fallo': 1.00} # Estado Absorbente
}

prediccion_temporal_estacionaria(estado_dia_cero, fisica_del_motor, dias_a_predecir=10)