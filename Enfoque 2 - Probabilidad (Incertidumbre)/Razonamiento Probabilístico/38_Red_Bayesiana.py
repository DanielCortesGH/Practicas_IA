# ==========================================
# SECCIÓN 1: DEFINICIÓN DE LA RED BAYESIANA (CPTs)
# ==========================================

# 1. Nodos raíz (Probabilidades a priori de los eventos base)
# La red eléctrica de 230V tiene un 5% de probabilidad de sufrir un pico anómalo.
P_Pico_230V = 0.05 
# El circuito de control tiene un 10% de probabilidad de fallar al enviar el pulso.
P_Fallo_Gatillo = 0.10 

# 2. Nodo Intermedio: TRIAC Dañado
# Depende de sus dos padres. Formato: (Pico_230V, Fallo_Gatillo) : Probabilidad
CPT_TRIAC_Danado = {
    (True, True): 0.95,   # Pico + Fallo Gatillo = 95% seguro que se quema
    (True, False): 0.80,  # Solo Pico en la red = 80% de riesgo
    (False, True): 0.60,  # Solo fallo en gatillo (sobrecorriente localizada) = 60%
    (False, False): 0.01  # Funcionamiento normal, fallo espontáneo = 1%
}

# 3. Nodo Hoja: Sobrecalentamiento
# Depende únicamente del estado del TRIAC
CPT_Sobrecalentamiento = {
    True: 0.90,  # Si el TRIAC está dañado (en corto), 90% seguro se sobrecalienta
    False: 0.05  # Si el TRIAC está bien, 5% de probabilidad de calor por el ambiente
}

def calcular_probabilidad_conjunta(pico, gatillo, triac, sobrecalentamiento):
    """
    Calcula la probabilidad P(X1, X2, X3, X4) multiplicando la red completa.
    """
    # Obtenemos la probabilidad de cada nodo dado el estado de sus padres
    p_p = P_Pico_230V if pico else (1 - P_Pico_230V)
    p_g = P_Fallo_Gatillo if gatillo else (1 - P_Fallo_Gatillo)
    
    prob_triac_dado_padres = CPT_TRIAC_Danado[(pico, gatillo)]
    p_t = prob_triac_dado_padres if triac else (1 - prob_triac_dado_padres)
    
    prob_sobre_dado_triac = CPT_Sobrecalentamiento[triac]
    p_s = prob_sobre_dado_triac if sobrecalentamiento else (1 - prob_sobre_dado_triac)
    
    # La Regla de la Cadena de la Red Bayesiana
    return p_p * p_g * p_t * p_s

# ==========================================
# SECCIÓN 2: MOTOR DE INFERENCIA POR ENUMERACIÓN
# ==========================================

def inferencia_diagnostico_triac(evidencia_sobrecalentamiento):
    """
    Responde a la consulta: P(TRIAC_Danado = True | Sobrecalentamiento = evidencia)
    Usando el Teorema de Bayes: P(A|B) = P(A y B) / P(B)
    """
    print(f"--- Ejecutando Inferencia Diagnóstica ---")
    print(f"Evidencia detectada por sensores: Sobrecalentamiento = {evidencia_sobrecalentamiento}")
    
    # Numerador: Probabilidad de que el TRIAC esté dañado Y exista la evidencia.
    # Tenemos que sumar (marginar) todas las combinaciones de los nodos ocultos (Pico y Gatillo)
    numerador = 0.0
    for pico in [True, False]:
        for gatillo in [True, False]:
            numerador += calcular_probabilidad_conjunta(pico, gatillo, True, evidencia_sobrecalentamiento)
            
    # Denominador: Probabilidad total de la evidencia.
    # Sumamos TODAS las combinaciones de la red donde Sobrecalentamiento coincida con la evidencia.
    denominador = 0.0
    for pico in [True, False]:
        for gatillo in [True, False]:
            for triac in [True, False]:
                denominador += calcular_probabilidad_conjunta(pico, gatillo, triac, evidencia_sobrecalentamiento)
                
    # Normalización
    probabilidad_final = numerador / denominador
    return probabilidad_final

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Caso 1: El termistor lee altas temperaturas.
prob_fallo_con_calor = inferencia_diagnostico_triac(evidencia_sobrecalentamiento=True)
print(f"🚨 RESULTADO: La probabilidad de que el TRIAC esté destruido es {prob_fallo_con_calor * 100:.2f}%\n")

# Caso 2: El disipador está frío.
prob_fallo_sin_calor = inferencia_diagnostico_triac(evidencia_sobrecalentamiento=False)
print(f"✅ RESULTADO: La probabilidad de que el TRIAC esté destruido es {prob_fallo_sin_calor * 100:.2f}%")