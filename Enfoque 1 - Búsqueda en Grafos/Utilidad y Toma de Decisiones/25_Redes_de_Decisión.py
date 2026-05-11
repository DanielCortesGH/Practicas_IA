def calcular_utilidad_esperada(decision, probabilidades_azar, matriz_utilidad):
    """
    TEMA 25: Calcula la Utilidad Esperada (EU) de una decisión bajo incertidumbre.
    Fórmula: EU(Acción) = Σ [ Probabilidad(Resultado) * Utilidad(Acción, Resultado) ]
    """
    utilidad_esperada = 0.0
    
    # Iteramos sobre todos los futuros posibles que la naturaleza nos puede arrojar
    for estado_naturaleza, probabilidad in probabilidades_azar.items():
        
        # Buscamos qué puntaje (Utilidad) obtendríamos bajo este futuro específico
        puntaje = matriz_utilidad[decision][estado_naturaleza]
        
        # Sumamos el promedio ponderado
        utilidad_esperada += probabilidad * puntaje
        
        print(f"    - Si ocurre '{estado_naturaleza}' ({probabilidad*100}%): Ganamos {puntaje} pts.")
        
    return utilidad_esperada

def tomar_decision_red_bayesiana(decisiones_posibles, probabilidades_azar, matriz_utilidad):
    """
    Evalúa todas las decisiones y elige la que maximice la Utilidad Esperada general.
    """
    print("--- Red de Decisión: Analizando Futuros Posibles ---\n")
    
    mejor_decision = None
    maxima_eu = -float('inf')
    
    for decision in decisiones_posibles:
        print(f"[?] Evaluando decisión: {decision}")
        
        # Calculamos el promedio de todos los futuros para esta decisión
        eu_actual = calcular_utilidad_esperada(decision, probabilidades_azar, matriz_utilidad)
        print(f"  => UTILIDAD ESPERADA (EU) de '{decision}': {eu_actual:.2f}\n")
        
        if eu_actual > maxima_eu:
            maxima_eu = eu_actual
            mejor_decision = decision
            
    return mejor_decision, maxima_eu

# ==========================================
# ZONA DE PRUEBAS (El Robot de Riego en Jalisco)
# ==========================================

# 1. El Nodo de Decisión (Lo que el robot puede hacer)
decisiones = ['Encender Bomba', 'No Encender']

# 2. El Nodo de Azar (Lo que dice el pronóstico del clima local)
clima_probabilidades = {
    'Lluvia': 0.70,   # 70% de probabilidad de que llueva
    'Sequia': 0.30    # 30% de que no caiga ni una gota
}

# 3. El Nodo de Utilidad (Las consecuencias de nuestras acciones + la naturaleza)
# Valores: Ahorrar energía y tener agua gratis es lo mejor (100).
# Gastar electricidad a lo tonto es malo (20). Que se muera la planta es pésimo (-50).
tabla_utilidades = {
    'Encender Bomba': {
        'Lluvia': 20,  # Desperdiciamos electricidad porque la lluvia ya iba a regar (Utilidad baja)
        'Sequia': 80   # Gastamos luz, pero salvamos el agave (Utilidad buena)
    },
    'No Encender': {
        'Lluvia': 100, # ¡El escenario perfecto! Cero gasto eléctrico, riego gratis (Utilidad máxima)
        'Sequia': -50  # El peor escenario. No regamos y no llovió. Cosecha perdida (Utilidad fatal)
    }
}

decision_final, eu_final = tomar_decision_red_bayesiana(decisiones, clima_probabilidades, tabla_utilidades)

print("-" * 40)
print(f" DECISIÓN RACIONAL DEL ROBOT: '{decision_final}'")
print(f" Justificación: Maximiza la Utilidad Esperada a {eu_final:.2f} puntos promediados.")