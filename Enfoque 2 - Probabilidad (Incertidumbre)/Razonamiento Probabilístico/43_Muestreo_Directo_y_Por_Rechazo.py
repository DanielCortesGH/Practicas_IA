import random

# ==========================================
# 1. MUESTREO DIRECTO (Generador de Universos)
# ==========================================
def tirar_dado(probabilidad_true):
    """Devuelve True o False simulando probabilidad con un número aleatorio."""
    return random.random() < probabilidad_true

def generar_muestra_directa():
    """
    TEMA 43 (Parte 1): Crea un 'universo' paso a paso respetando la jerarquía causal.
    Red: Suministro_Electrico -> Brazo_Atascado -> Alarma
    """
    # Nodo Raíz: 10% de probabilidad de que la red eléctrica de la fábrica falle
    suministro_falla = tirar_dado(0.10)
    
    # Nodo Hijo 1: Depende del suministro
    if suministro_falla:
        brazo_atascado = tirar_dado(0.80) # Sin energía, 80% seguro que el motor se frena
    else:
        brazo_atascado = tirar_dado(0.05) # Con energía, falla mecánica espontánea (5%)
        
    # Nodo Hijo 2: Depende del brazo
    if brazo_atascado:
        alarma = tirar_dado(0.90) # Sensor bueno, detecta el atasco el 90% de las veces
    else:
        alarma = tirar_dado(0.02) # Falsa alarma por ruido (2%)
        
    # Devolvemos un diccionario que representa TODO lo que pasó en esta simulación
    return {
        'Suministro_Falla': suministro_falla,
        'Brazo_Atascado': brazo_atascado,
        'Alarma': alarma
    }

# ==========================================
# 2. MUESTREO POR RECHAZO (Inferencia)
# ==========================================
def muestreo_por_rechazo(variable_consulta, evidencia, num_simulaciones=10000):
    """
    TEMA 43 (Parte 2): Responde consultas estadísticamente tirando a la basura
    los universos que no coinciden con nuestros sensores.
    """
    print(f"--- Iniciando Muestreo por Rechazo ({num_simulaciones} iteraciones) ---")
    
    muestras_aceptadas = 0
    consulta_verdadera = 0
    
    for i in range(num_simulaciones):
        # 1. Creamos un universo paralelo
        muestra = generar_muestra_directa()
        
        # 2. RECHAZO: Verificamos si este universo es compatible con nuestra realidad
        es_compatible = True
        for clave_evidencia, valor_evidencia in evidencia.items():
            if muestra[clave_evidencia] != valor_evidencia:
                es_compatible = False
                break
                
        # Si el universo contradice la evidencia, lo ignoramos por completo
        if not es_compatible:
            continue
            
        # 3. Si sobrevivió al rechazo, lo contabilizamos
        muestras_aceptadas += 1
        
        # 4. Verificamos si en este universo válido la consulta fue Verdadera
        if muestra[variable_consulta] == True:
            consulta_verdadera += 1
            
    # El resultado final es la simple proporción de casos exitosos
    if muestras_aceptadas == 0:
        return 0.0 # Evitamos división por cero si rechazamos todo
        
    probabilidad = consulta_verdadera / muestras_aceptadas
    
    print(f"Simulaciones creadas: {num_simulaciones}")
    print(f"Simulaciones RECHAZADAS: {num_simulaciones - muestras_aceptadas}")
    print(f"Simulaciones Aceptadas: {muestras_aceptadas}")
    
    return probabilidad

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Pregunta: ¿Cuál es la probabilidad de que la red eléctrica haya fallado,
# DADO QUE estamos escuchando la alarma del brazo robótico?
evidencia_real = {'Alarma': True}
prob_estadistica = muestreo_por_rechazo('Suministro_Falla', evidencia_real, num_simulaciones=50000)

print("-" * 50)
print(f"📊 DIAGNÓSTICO APROXIMADO: P(Suministro Falla | Alarma) ≈ {prob_estadistica * 100:.2f}%")