import random

# ==========================================
# 1. LA RED BAYESIANA (CPTs)
# ==========================================
P_Fallo_Bomba = 0.05 # 5% de riesgo a priori

def prob_bajo_flujo(bomba_falla):
    # Si la bomba falla, 95% de probabilidad de bajo flujo. Si no, 10% de falla en tuberías.
    return 0.95 if bomba_falla else 0.10

def prob_alta_temperatura(bajo_flujo):
    # Si hay bajo flujo, 90% seguro se calienta. Si no, 5% de calentamiento ambiental.
    return 0.90 if bajo_flujo else 0.05

def tirar_dado(probabilidad):
    return random.random() < probabilidad

# ==========================================
# 2. EL GENERADOR PONDERADO
# ==========================================
def generar_muestra_ponderada(evidencia_fija):
    """
    TEMA 44: Genera UNA simulación. Fuerza la evidencia y calcula su peso 'w'.
    """
    peso_w = 1.0 # Todas las simulaciones nacen valiendo 1 entero
    muestra = {}
    
    # NODO 1: Fallo_Bomba (No es evidencia, así que lo simulamos normal)
    if 'Fallo_Bomba' in evidencia_fija:
        muestra['Fallo_Bomba'] = evidencia_fija['Fallo_Bomba']
        # (Si fuera evidencia, multiplicaríamos el peso aquí)
    else:
        muestra['Fallo_Bomba'] = tirar_dado(P_Fallo_Bomba)
        
    # NODO 2: Bajo_Flujo (No es evidencia, simulamos normal)
    p_flujo = prob_bajo_flujo(muestra['Fallo_Bomba'])
    
    if 'Bajo_Flujo' in evidencia_fija:
        muestra['Bajo_Flujo'] = evidencia_fija['Bajo_Flujo']
    else:
        muestra['Bajo_Flujo'] = tirar_dado(p_flujo)
        
    # NODO 3: Alta_Temperatura (¡ESTA ES NUESTRA EVIDENCIA!)
    p_temp = prob_alta_temperatura(muestra['Bajo_Flujo'])
    
    if 'Alta_Temperatura' in evidencia_fija:
        # 1. HACEMOS TRAMPA: Obligamos a la simulación a tener este valor
        muestra['Alta_Temperatura'] = evidencia_fija['Alta_Temperatura']
        
        # 2. COBRAMOS EL IMPUESTO: 
        # Si la evidencia dictaba 'True', multiplicamos por p_temp. 
        # Si dictaba 'False', multiplicaríamos por (1 - p_temp).
        probabilidad_natural = p_temp if evidencia_fija['Alta_Temperatura'] else (1.0 - p_temp)
        peso_w *= probabilidad_natural
    else:
        muestra['Alta_Temperatura'] = tirar_dado(p_temp)
        
    return muestra, peso_w

# ==========================================
# 3. EL MOTOR ESTADÍSTICO (Inferencia)
# ==========================================
def ponderacion_verosimilitud(consulta, evidencia, iteraciones=10000):
    print(f"--- Iniciando Ponderación de Verosimilitud ({iteraciones} iteraciones) ---")
    
    suma_pesos_consulta_true = 0.0
    suma_pesos_totales = 0.0
    
    for _ in range(iteraciones):
        # Cada simulación nos devuelve su universo y cuánto "pesa" (vale)
        universo, peso = generar_muestra_ponderada(evidencia)
        
        # Sumamos todos los pesos para el factor de normalización
        suma_pesos_totales += peso
        
        # Si en este universo la bomba falló, sumamos su peso a la columna de 'True'
        if universo[consulta] == True:
            suma_pesos_consulta_true += peso
            
    # La probabilidad es la fracción de los pesos, no de las simulaciones crudas
    probabilidad_final = suma_pesos_consulta_true / suma_pesos_totales
    
    print(f"Simulaciones generadas: {iteraciones}")
    print(f"Simulaciones RECHAZADAS: 0 (¡100% de eficiencia!)")
    
    return probabilidad_final

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Nuestro sensor detecta Alta Temperatura. Queremos saber si la bomba falló.
evidencia_sensores = {'Alta_Temperatura': True}
resultado = ponderacion_verosimilitud('Fallo_Bomba', evidencia_sensores, iteraciones=10000)

print("-" * 50)
print(f"📊 DIAGNÓSTICO: P(Fallo_Bomba | Alta_Temperatura) ≈ {resultado * 100:.2f}%")