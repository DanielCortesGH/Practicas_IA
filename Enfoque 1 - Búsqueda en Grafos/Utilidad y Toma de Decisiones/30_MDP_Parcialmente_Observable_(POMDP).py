def actualizar_creencia(estados, creencia_actual, accion, observacion, transiciones, modelo_sensor):
    """
    TEMA 30: Actualización del Estado de Creencia en un POMDP (Filtro Bayesiano).
    Combina la física del movimiento con la lectura del sensor ruidoso.
    """
    nueva_creencia = {estado: 0.0 for estado in estados}
    probabilidad_total = 0.0
    
    for estado_destino in estados:
        
        # PASO 1: PREDICCIÓN (¿A dónde creo que me llevó el movimiento?)
        # Sumamos las probabilidades de haber llegado aquí desde cualquier estado origen
        prob_predicha = 0.0
        for estado_origen in estados:
            prob_mover = transiciones[estado_origen][accion].get(estado_destino, 0.0)
            prob_predicha += prob_mover * creencia_actual[estado_origen]
            
        # PASO 2: ACTUALIZACIÓN (¿Qué dice mi sensor ahora que estoy aquí?)
        # Multiplicamos nuestra predicción por la probabilidad de ver esta lectura
        prob_observacion = modelo_sensor[estado_destino].get(observacion, 0.0)
        
        prob_final_estado = prob_observacion * prob_predicha
        
        nueva_creencia[estado_destino] = prob_final_estado
        probabilidad_total += prob_final_estado
        
    # PASO 3: NORMALIZACIÓN (El factor Alpha de la fórmula)
    # Ajustamos los números para que la suma total vuelva a ser exactamente 1.0 (100%)
    if probabilidad_total > 0:
        for estado in estados:
            nueva_creencia[estado] /= probabilidad_total
    else:
        print(" ALERTA: La lectura del sensor es lógicamente imposible según el modelo.")
        
    return nueva_creencia

# ==========================================
# ZONA DE PRUEBAS (El Robot en el Ducto)
# ==========================================

espacio_estados = ['Zona Limpia', 'Zona con Basura']

# 1. El Estado de Creencia Inicial
# Al encenderlo, el robot no tiene idea de dónde está (50/50)
creencia = {'Zona Limpia': 0.50, 'Zona con Basura': 0.50}

# 2. Modelo de Transición (P): Si decide 'Avanzar', las zonas cambian.
# Si está limpio, 80% seguro llegará a otra zona limpia. 
fisica_mundo = {
    'Zona Limpia': {
        'Avanzar': {'Zona Limpia': 0.80, 'Zona con Basura': 0.20}
    },
    'Zona con Basura': {
        'Avanzar': {'Zona Limpia': 0.40, 'Zona con Basura': 0.60}
    }
}

# 3. Modelo del Sensor Ruidoso (O): ¿Qué ve la cámara dependiendo de dónde está realmente?
# La cámara a veces confunde manchas de agua con basura (20% de error).
sensores = {
    'Zona Limpia': {
        'Lectura_Limpio': 0.80, # 80% de las veces acierta
        'Lectura_Basura': 0.20  # 20% de las veces se equivoca (Falso positivo)
    },
    'Zona con Basura': {
        'Lectura_Limpio': 0.10, # 10% de las veces la cámara no ve la basura (Falso negativo)
        'Lectura_Basura': 0.90  # 90% de las veces acierta
    }
}

print("--- Inicializando Rastreador de Creencia POMDP ---")
print(f"[{'Turno 0'}] Creencia (b): {creencia['Zona Limpia']*100:.1f}% Limpio | {creencia['Zona con Basura']*100:.1f}% Basura")

# EL ROBOT COMIENZA A OPERAR
# Turno 1: Avanza y su cámara cree ver basura
accion_1 = 'Avanzar'
lectura_1 = 'Lectura_Basura'

creencia = actualizar_creencia(espacio_estados, creencia, accion_1, lectura_1, fisica_mundo, sensores)
print(f"\n[Turno 1] Acción: '{accion_1}' | Sensor detectó: '{lectura_1}'")
print(f"   -> Nueva Creencia (b'): {creencia['Zona Limpia']*100:.1f}% Limpio | {creencia['Zona con Basura']*100:.1f}% Basura")

# Turno 2: Avanza de nuevo, y su cámara VUELVE a ver basura
accion_2 = 'Avanzar'
lectura_2 = 'Lectura_Basura'

creencia = actualizar_creencia(espacio_estados, creencia, accion_2, lectura_2, fisica_mundo, sensores)
print(f"\n[Turno 2] Acción: '{accion_2}' | Sensor detectó: '{lectura_2}'")
print(f"   -> Nueva Creencia (b'): {creencia['Zona Limpia']*100:.1f}% Limpio | {creencia['Zona con Basura']*100:.1f}% Basura")