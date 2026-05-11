# ==========================================
# 1. DEFINICIÓN DEL HMM (La tupla de 5 elementos)
# ==========================================
estados_ocultos = ['Saludable', 'Dañado']
observaciones = ['Normal', 'Vibracion', 'Ruido_Fuerte']

# pi: Probabilidades Iniciales
prob_inicial = {'Saludable': 0.90, 'Dañado': 0.10}

# A: Matriz de Transición
transicion = {
    'Saludable': {'Saludable': 0.80, 'Dañado': 0.20},
    'Dañado':    {'Saludable': 0.00, 'Dañado': 1.00}
}

# B: Matriz de Emisión (Sensores)
emision = {
    'Saludable': {'Normal': 0.70, 'Vibracion': 0.25, 'Ruido_Fuerte': 0.05},
    'Dañado':    {'Normal': 0.10, 'Vibracion': 0.40, 'Ruido_Fuerte': 0.50}
}

# ==========================================
# 2. EL ALGORITMO DE VITERBI
# ==========================================
def algoritmo_viterbi(secuencia_obs):
    """
    Decodifica la secuencia de estados ocultos más probable
    dada una secuencia de observaciones, usando Programación Dinámica.
    """
    print(f"--- Iniciando Decodificación Viterbi ---")
    print(f"Secuencia de sensores capturada: {secuencia_obs}\n")
    
    T = len(secuencia_obs)
    
    # V[t][estado] guardará la probabilidad de la mejor ruta hasta el tiempo t
    V = [{}]
    # backpointer[t][estado] recordará qué estado anterior nos dio esa mejor ruta
    backpointer = [{}]
    
    # INICIALIZACIÓN (Tiempo 0)
    obs_inicial = secuencia_obs[0]
    for estado in estados_ocultos:
        # P_inicial * P_emision
        V[0][estado] = prob_inicial[estado] * emision[estado][obs_inicial]
        backpointer[0][estado] = None
        
    # RECURSIÓN (Tiempo 1 hasta T-1)
    for t in range(1, T):
        V.append({})
        backpointer.append({})
        obs_actual = secuencia_obs[t]
        
        for estado_actual in estados_ocultos:
            prob_maxima = -1.0
            mejor_estado_previo = None
            
            # Buscamos cuál estado del pasado maximiza la probabilidad de llegar al estado actual
            for estado_previo in estados_ocultos:
                # Ecuación de Viterbi: V_{t-1} * Transicion * Emision
                prob_ruta = V[t-1][estado_previo] * transicion[estado_previo][estado_actual] * emision[estado_actual][obs_actual]
                
                if prob_ruta > prob_maxima:
                    prob_maxima = prob_ruta
                    mejor_estado_previo = estado_previo
                    
            V[t][estado_actual] = prob_maxima
            backpointer[t][estado_actual] = mejor_estado_previo
            
    # TERMINACIÓN (Encontrar el mejor estado final)
    prob_final_maxima = -1.0
    mejor_estado_final = None
    
    for estado in estados_ocultos:
        if V[T-1][estado] > prob_final_maxima:
            prob_final_maxima = V[T-1][estado]
            mejor_estado_final = estado
            
    # RECONSTRUCCIÓN DE LA RUTA (Viajamos hacia atrás usando los backpointers)
    ruta_optima = [mejor_estado_final]
    estado_actual_retroceso = mejor_estado_final
    
    for t in range(T-1, 0, -1):
        estado_previo = backpointer[t][estado_actual_retroceso]
        ruta_optima.insert(0, estado_previo)
        estado_actual_retroceso = estado_previo
        
    return ruta_optima

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Escuchamos a la máquina durante 4 ciclos de trabajo
secuencia_audio = ['Normal', 'Vibracion', 'Vibracion', 'Ruido_Fuerte']

historia_reconstruida = algoritmo_viterbi(secuencia_audio)

print("🔍 LA HISTORIA OCULTA MÁS PROBABLE ES:")
for t in range(len(secuencia_audio)):
    print(f"  Paso {t+1}: Sensor=[{secuencia_audio[t]}] --> Estado Real Estimado=[{historia_reconstruida[t]}]")