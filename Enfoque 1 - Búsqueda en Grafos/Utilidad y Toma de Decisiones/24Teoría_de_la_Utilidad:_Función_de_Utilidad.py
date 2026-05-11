def calcular_utilidad(opcion, pesos):
    """
    TEMA 24: Función de Utilidad U(s).
    Evalúa qué tan 'deseable' es una opción basándose en los pesos de preferencia.
    """
    # Extraemos las características de la opción
    bateria_ahorrada = opcion['bateria_ahorrada_porcentaje']
    tiempo_minutos = opcion['tiempo_estimado_minutos']
    probabilidad_danio = opcion['riesgo_danio_porcentaje']
    
    # Extraemos la "personalidad" del agente (los pesos)
    w_bateria = pesos['peso_bateria']
    w_tiempo = pesos['peso_tiempo']
    w_riesgo = pesos['peso_riesgo']
    
    # La fórmula de utilidad matemática U(s)
    # Entre más batería ahorre, mejor (+). Entre más tarde o más riesgo haya, peor (-).
    utilidad = (w_bateria * bateria_ahorrada) - (w_tiempo * tiempo_minutos) - (w_riesgo * probabilidad_danio)
    
    return utilidad

def tomar_decision_racional(opciones, pesos_preferencia):
    """
    El agente evalúa todas las opciones y elige la que maximiza su función de utilidad.
    """
    mejor_opcion = None
    maxima_utilidad = -float('inf')
    
    print("--- Evaluando opciones disponibles ---")
    for nombre, caracteristicas in opciones.items():
        # Calculamos U(s) para esta opción
        u_actual = calcular_utilidad(caracteristicas, pesos_preferencia)
        print(f"  > {nombre}: Utilidad calculada = {u_actual:.2f}")
        
        # El principio de Máxima Utilidad Esperada
        if u_actual > maxima_utilidad:
            maxima_utilidad = u_actual
            mejor_opcion = nombre
            
    return mejor_opcion, maxima_utilidad

# ==========================================
# ZONA DE PRUEBAS (El Dron Repartidor)
# ==========================================

# Las opciones de navegación física
rutas_disponibles = {
    'Ruta 1 (Por Av. Vallarta - Directo pero con tráfico de aves)': {
        'bateria_ahorrada_porcentaje': 40,
        'tiempo_estimado_minutos': 10,
        'riesgo_danio_porcentaje': 15  # Alto riesgo
    },
    'Ruta 2 (Rodeando por Periférico - Largo pero despejado)': {
        'bateria_ahorrada_porcentaje': 10, # Gasta mucha batería
        'tiempo_estimado_minutos': 25,
        'riesgo_danio_porcentaje': 2   # Muy seguro
    },
    'Ruta 3 (Corte por colonias residenciales)': {
        'bateria_ahorrada_porcentaje': 25,
        'tiempo_estimado_minutos': 15,
        'riesgo_danio_porcentaje': 5
    }
}

# ESCENARIO A: Modo "Urgencia Médica"
# El tiempo es vital, la batería y el equipo no importan tanto.
pesos_emergencia = {
    'peso_bateria': 1.0,
    'peso_tiempo': 10.0,  # Penaliza brutalmente la tardanza
    'peso_riesgo': 2.0
}

# ESCENARIO B: Modo "Traslado de Cristal Fino"
# El paquete es invaluable, el tiempo no importa.
pesos_fragil = {
    'peso_bateria': 1.0,
    'peso_tiempo': 1.0,
    'peso_riesgo': 20.0   # Penaliza brutalmente cualquier riesgo
}

print(" ESCENARIO A: Entrega de Emergencia Médica")
decision_a, util_a = tomar_decision_racional(rutas_disponibles, pesos_emergencia)
print(f" Decisión Racional: Tomar la '{decision_a}' (Utilidad: {util_a:.2f})\n")

print(" ESCENARIO B: Entrega de Cristal Fino")
decision_b, util_b = tomar_decision_racional(rutas_disponibles, pesos_fragil)
print(f" Decisión Racional: Tomar la '{decision_b}' (Utilidad: {util_b:.2f})")