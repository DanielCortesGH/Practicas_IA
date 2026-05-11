# ==========================================
# 1. DEFINICIÓN DEL MODELO OCULTO DE MARKOV
# ==========================================
# Estados: 0 = Sin Intruso, 1 = Con Intruso
estados = [0, 1]

# Probabilidad Inicial (Día 0)
prob_inicial = {0: 0.80, 1: 0.20}

# Modelo de Transición: P(X_t | X_{t-1})
# [Estado_Anterior][Estado_Actual]
transicion = {
    0: {0: 0.70, 1: 0.30}, # Si no había intruso, 30% de que entre uno
    1: {0: 0.40, 1: 0.60}  # Si había intruso, 60% de que siga ahí
}

# Modelo del Sensor: P(e_t | X_t)
# [Estado_Actual][Evidencia] -> Evidencia: 'Activo' o 'Silencio'
sensor = {
    0: {'Activo': 0.10, 'Silencio': 0.90}, # Falsa alarma 10%
    1: {'Activo': 0.80, 'Silencio': 0.20}  # Falla del sensor 20%
}

def normalizar(vector_prob):
    suma = sum(vector_prob.values())
    return {k: v / suma for k, v in vector_prob.items()}

# ==========================================
# 2. EL ALGORITMO FORWARD-BACKWARD
# ==========================================
def algoritmo_hacia_delante_atras(evidencia_secuencia):
    T = len(evidencia_secuencia)
    
    # 1. FASE FORWARD (Hacia Delante)
    # fv[t] guarda la creencia filtrada hasta el día t
    fv = [prob_inicial] 
    
    for t in range(T):
        lectura_sensor = evidencia_secuencia[t]
        mensaje_f_previo = fv[-1]
        mensaje_f_nuevo = {0: 0.0, 1: 0.0}
        
        for estado_actual in estados:
            # Sumatoria: P(X_t|X_t-1) * P(X_t-1)
            suma_transicion = sum(
                transicion[estado_prev][estado_actual] * mensaje_f_previo[estado_prev]
                for estado_prev in estados
            )
            # Multiplicar por evidencia del sensor
            mensaje_f_nuevo[estado_actual] = sensor[estado_actual][lectura_sensor] * suma_transicion
            
        fv.append(normalizar(mensaje_f_nuevo))
        
    # 2. FASE BACKWARD (Hacia Atrás)
    # bv[t] guarda la evidencia futura dado el estado t.
    # El mensaje del "último día futuro" se inicializa siempre en 1.0
    bv = [{0: 1.0, 1: 1.0}] 
    
    # Recorremos el tiempo al revés (de T-1 hasta 0)
    for t in range(T - 1, -1, -1):
        lectura_futura = evidencia_secuencia[t]
        mensaje_b_siguiente = bv[0] # El último que calculamos (que es el "futuro" relativo)
        mensaje_b_nuevo = {0: 0.0, 1: 0.0}
        
        for estado_actual in estados:
            # Sumatoria de: P(e_t+1 | X_t+1) * P(X_t+1 | X_t) * b_{t+1}
            suma_atras = sum(
                sensor[estado_futuro][lectura_futura] * 
                transicion[estado_actual][estado_futuro] * 
                mensaje_b_siguiente[estado_futuro]
                for estado_futuro in estados
            )
            mensaje_b_nuevo[estado_actual] = suma_atras
            
        # Insertamos al principio de la lista porque vamos hacia atrás
        bv.insert(0, mensaje_b_nuevo) 
        
    # 3. FASE DE SUAVIZADO (Combinar Forward y Backward)
    sv = []
    # Ignoramos el índice 0 de los vectores para alinear con los días 1, 2, 3
    for i in range(1, T + 1):
        dia_suavizado = {0: 0.0, 1: 0.0}
        for estado in estados:
            # P(X_k | e_1:t) = a * f * b
            dia_suavizado[estado] = fv[i][estado] * bv[i][estado]
            
        sv.append(normalizar(dia_suavizado))
        
    return fv[1:], sv

# ==========================================
# ZONA DE PRUEBAS
# ==========================================
secuencia = ['Activo', 'Silencio', 'Activo']
forward_filtrado, suavizado_final = algoritmo_hacia_delante_atras(secuencia)

print("--- ANÁLISIS DEL DÍA 2 ---")
print("Evidencia del Día 2: Sensor en 'Silencio'")
print(f"1. Creencia Filtrada (Conocimiento normal hasta el Día 2):")
print(f"   -> Probabilidad de Intruso: {forward_filtrado[1][1]*100:.1f}%\n")

print("Evidencia del Día 3: Sensor 'Se Activa'")
print(f"2. Creencia Suavizada (Re-evaluación del Día 2 usando el futuro):")
print(f"   -> Probabilidad de Intruso: {suavizado_final[1][1]*100:.1f}%")