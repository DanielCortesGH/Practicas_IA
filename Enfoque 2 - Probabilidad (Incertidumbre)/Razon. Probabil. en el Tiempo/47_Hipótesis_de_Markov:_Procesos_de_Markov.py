import random

def siguiente_estado_markov(estado_actual, matriz_transicion):
    """
    La esencia de la Hipótesis de Markov:
    Para calcular el siguiente estado, esta función SOLO recibe 'estado_actual'.
    No recibe un historial, ni listas, ni arreglos de memoria pasada.
    """
    probabilidades = matriz_transicion[estado_actual]
    estados_posibles = list(probabilidades.keys())
    pesos = list(probabilidades.values())
    
    # random.choices elige un elemento basándose en sus pesos (probabilidades)
    # Devuelve una lista, así que tomamos el elemento [0]
    nuevo_estado = random.choices(estados_posibles, weights=pesos, k=1)[0]
    return nuevo_estado

def simular_proceso_markov(estado_inicial, matriz_transicion, pasos_de_tiempo):
    """
    TEMA 47: Simula un Proceso de Markov completo.
    Genera una 'Cadena de Markov' a lo largo del tiempo.
    """
    print("--- Simulador de Proceso de Markov (Telemetría ESP32) ---")
    
    historial_cadena = [estado_inicial]
    estado_actual = estado_inicial
    
    print(f"t=0 | Señal: {estado_actual}")
    
    for t in range(1, pasos_de_tiempo + 1):
        # 1. El cálculo del futuro depende ÚNICAMENTE del presente
        estado_futuro = siguiente_estado_markov(estado_actual, matriz_transicion)
        
        # 2. El futuro se convierte en el nuevo presente
        estado_actual = estado_futuro
        
        historial_cadena.append(estado_actual)
        print(f"t={t} | Señal: {estado_actual}")
        
    return historial_cadena

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Definimos nuestra Matriz Estacionaria (Tema 46)
matriz_telemetria = {
    'Fuerte':  {'Fuerte': 0.80, 'Debil': 0.15, 'Perdida': 0.05},
    'Debil':   {'Fuerte': 0.40, 'Debil': 0.40, 'Perdida': 0.20},
    'Perdida': {'Fuerte': 0.10, 'Debil': 0.30, 'Perdida': 0.60} 
}

# Iniciamos el microcontrolador con buena señal y lo dejamos correr 10 ciclos
cadena_resultante = simular_proceso_markov('Fuerte', matriz_telemetria, pasos_de_tiempo=10)

print("\n📡 CADENA DE MARKOV GENERADA:")
print(" -> ".join(cadena_resultante))