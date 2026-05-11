def calcular_eu_sin_informacion(decisiones, probabilidades, utilidades):
    """Calcula la Utilidad Esperada a ciegas (Lo que hicimos en el Tema 25)."""
    max_eu = -float('inf')
    for decision in decisiones:
        eu_actual = sum(probabilidades[clima] * utilidades[decision][clima] for clima in probabilidades)
        if eu_actual > max_eu:
            max_eu = eu_actual
    return max_eu

def calcular_eu_con_informacion_perfecta(decisiones, probabilidades, utilidades):
    """
    Calcula la Utilidad Esperada asumiendo que un sensor nos dirá EXACTAMENTE 
    qué clima hará antes de tomar la decisión.
    """
    eu_perfecta = 0.0
    
    # Para cada futuro posible que el sensor nos podría revelar...
    for clima, probabilidad_de_que_ocurra in probabilidades.items():
        
        # Como ya sabemos el clima, revisamos TODAS las decisiones y elegimos la mejor para ESE clima
        mejor_utilidad_para_este_clima = -float('inf')
        mejor_decision = None
        
        for decision in decisiones:
            utilidad = utilidades[decision][clima]
            if utilidad > mejor_utilidad_para_este_clima:
                mejor_utilidad_para_este_clima = utilidad
                mejor_decision = decision
                
        print(f"    - Si el sensor lee '{clima}': La IA elegirá '{mejor_decision}' asegurando {mejor_utilidad_para_este_clima} pts.")
        
        # Ponderamos esta ganancia asegurada por la probabilidad de que el sensor lea este clima
        eu_perfecta += probabilidad_de_que_ocurra * mejor_utilidad_para_este_clima
        
    return eu_perfecta

def calcular_valor_informacion(decisiones, probabilidades, utilidades):
    """TEMA 26: Calcula el Valor de la Información Perfecta (VPI)."""
    print("--- Calculando el Valor del Nuevo Sensor de Humedad ---\n")
    
    # 1. ¿Cuánto ganamos actualmente (hardware básico)?
    eu_actual = calcular_eu_sin_informacion(decisiones, probabilidades, utilidades)
    print(f"[1] Utilidad Esperada actual (A ciegas): {eu_actual:.2f} pts")
    
    # 2. ¿Cuánto ganaríamos si compramos el sensor perfecto?
    print("[2] Simulando comportamiento con el nuevo sensor:")
    eu_futura = calcular_eu_con_informacion_perfecta(decisiones, probabilidades, utilidades)
    print(f"    => Utilidad Esperada con información perfecta: {eu_futura:.2f} pts\n")
    
    # 3. La resta matemática (VPI)
    vpi = eu_futura - eu_actual
    return vpi

# ==========================================
# ZONA DE PRUEBAS (Justificando la compra del hardware)
# ==========================================

decisiones = ['Encender Bomba', 'No Encender']
clima_probabilidades = {'Lluvia': 0.70, 'Sequia': 0.30}
tabla_utilidades = {
    'Encender Bomba': {'Lluvia': 20, 'Sequia': 80},
    'No Encender': {'Lluvia': 100, 'Sequia': -50}
}

valor_sensor = calcular_valor_informacion(decisiones, clima_probabilidades, tabla_utilidades)

print("-" * 40)
print(f" VALOR DE LA INFORMACIÓN (VPI) = {valor_sensor:.2f} puntos.")

# Supongamos que 1 punto de utilidad equivale a $10 MXN de ahorro en el cultivo.
ahorro_maximo = valor_sensor * 10
print(f" Conclusión: El robot aumentará sus ganancias en {valor_sensor:.2f} puntos.")
print(f"  Si el módulo del sensor cuesta MENOS de ${ahorro_maximo:.2f} MXN, ¡cómpralo e instálalo!")
print(f" Si cuesta MÁS, rechaza el rediseño. Es mejor quedarse con el software actual.")