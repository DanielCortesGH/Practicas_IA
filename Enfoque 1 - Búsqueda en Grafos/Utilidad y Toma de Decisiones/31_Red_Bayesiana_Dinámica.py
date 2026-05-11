def filtrado_dbn(estados, creencia_previa, lectura_sensores, modelo_transicion, modelo_sensores):
    """
    TEMA 31: Algoritmo de Filtrado para una Red Bayesiana Dinámica (DBN).
    Actualiza la creencia del estado oculto integrando MÚLTIPLES sensores en el tiempo t.
    """
    nueva_creencia = {estado: 0.0 for estado in estados}
    prob_total = 0.0
    
    # Desempaquetamos la evidencia del tiempo actual (t)
    lectura_vib = lectura_sensores['Vibracion']
    lectura_temp = lectura_sensores['Temperatura']
    
    for estado_actual in estados:
        
        # PASO 1: PREDICCIÓN (¿Cómo evolucionó la máquina desde t-1 a t?)
        prediccion = 0.0
        for estado_previo in estados:
            prob_transicion = modelo_transicion[estado_previo][estado_actual]
            prediccion += prob_transicion * creencia_previa[estado_previo]
            
        # PASO 2: ACTUALIZACIÓN POR SENSORES (Evidencia Múltiple)
        # En una DBN, asumimos que los sensores son condicionalmente independientes dado el estado.
        # Por lo tanto, multiplicamos sus probabilidades.
        prob_evidencia_vib = modelo_sensores['Vibracion'][estado_actual][lectura_vib]
        prob_evidencia_temp = modelo_sensores['Temperatura'][estado_actual][lectura_temp]
        
        prob_evidencia_total = prob_evidencia_vib * prob_evidencia_temp
        
        # Combinamos predicción física con la evidencia de los sensores
        prob_final = prob_evidencia_total * prediccion
        
        nueva_creencia[estado_actual] = prob_final
        prob_total += prob_final
        
    # PASO 3: NORMALIZACIÓN (Factor Alpha)
    for estado in estados:
        nueva_creencia[estado] /= prob_total
        
    return nueva_creencia

# ==========================================
# ZONA DE PRUEBAS (Monitoreo de Máquina CNC)
# ==========================================

espacio_estados = ['Optima', 'Desgastada']

# 1. Creencia Inicial (Hora 0)
# Acabamos de poner una broca nueva. Estamos 100% seguros de que está óptima.
creencia = {'Optima': 1.0, 'Desgastada': 0.0}

# 2. Modelo de Transición (El desgaste natural por el paso del tiempo)
# Una broca óptima tiene 10% de probabilidad de desgastarse cada hora.
# Una broca desgastada se queda desgastada (probabilidad 1.0) hasta que un humano la cambie.
transiciones = {
    'Optima': {'Optima': 0.90, 'Desgastada': 0.10},
    'Desgastada': {'Optima': 0.0, 'Desgastada': 1.0}
}

# 3. Modelo de Sensores (La Evidencia)
sensores = {
    'Vibracion': {
        'Optima': {'Normal': 0.85, 'Alta': 0.15},
        'Desgastada': {'Normal': 0.20, 'Alta': 0.80}
    },
    'Temperatura': {
        'Optima': {'Fria': 0.90, 'Caliente': 0.10},
        'Desgastada': {'Fria': 0.30, 'Caliente': 0.70}
    }
}

print("--- Iniciando Monitoreo DBN (Máquina CNC) ---")

# Simularemos 3 horas de trabajo continuo con diferentes lecturas de sensores
flujo_de_datos = [
    {'Hora': 1, 'Sensores': {'Vibracion': 'Normal', 'Temperatura': 'Fria'}},
    {'Hora': 2, 'Sensores': {'Vibracion': 'Alta', 'Temperatura': 'Fria'}},   # Anomalía de vibración
    {'Hora': 3, 'Sensores': {'Vibracion': 'Alta', 'Temperatura': 'Caliente'}} # Doble anomalía
]

for dato in flujo_de_datos:
    hora = dato['Hora']
    lecturas = dato['Sensores']
    
    # Alimentamos la DBN con el flujo de datos paso a paso
    creencia = filtrado_dbn(espacio_estados, creencia, lecturas, transiciones, sensores)
    
    print(f"\n[Hora {hora}] Sensores: Vibración {lecturas['Vibracion']} | Temp {lecturas['Temperatura']}")
    print(f"  -> Probabilidad de Desgaste: {creencia['Desgastada']*100:.2f}%")