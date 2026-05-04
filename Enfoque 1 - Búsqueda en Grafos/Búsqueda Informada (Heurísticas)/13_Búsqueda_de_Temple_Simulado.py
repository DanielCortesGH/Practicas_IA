import math
import random

def temple_simulado(grafo, altitudes, inicio, temp_inicial, factor_enfriamiento, iteraciones):
   
    print(f"--- Iniciando Temple Simulado (Punto de partida: {inicio}) ---\n")
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    estado_actual = inicio
    mejor_global = inicio
    
    temperatura = temp_inicial

    # ==========================================
    # SECCIÓN 2: CICLO DE ENFRIAMIENTO
    # ==========================================
    for i in range(iteraciones):
        
        # Si la temperatura llega a cero, el metal se congeló. Terminamos.
        if temperatura <= 0.01:
            print(f"\n❄️ El sistema se ha enfriado por completo en el paso {i}.")
            break
            
        print(f"[Paso {i}] Nodo: {estado_actual} (Alt: {altitudes[estado_actual]}) | Temp: {temperatura:.2f}")
        
        # Obtenemos los vecinos y elegimos UNO al azar
        vecinos = grafo.get(estado_actual, [])
        if not vecinos:
            break
            
        vecino_candidato = random.choice(vecinos)
        
        # Calculamos la diferencia de altura (Delta E)
        # Si es positiva, el vecino es más alto. Si es negativa, es más bajo (peor).
        delta_e = altitudes[vecino_candidato] - altitudes[estado_actual]

        # ==========================================
        # SECCIÓN 3: LA REGLA TERMODINÁMICA
        # ==========================================
        if delta_e > 0:
            # ¡Es un paso hacia arriba! Lo tomamos sin dudarlo.
            print(f"    -> ⬆️ Subiendo hacia '{vecino_candidato}' (Es mejor)")
            estado_actual = vecino_candidato
            
            # Actualizamos nuestro récord histórico
            if altitudes[estado_actual] > altitudes[mejor_global]:
                mejor_global = estado_actual
        else:
            # ¡Es un paso hacia abajo!
            # Calculamos la probabilidad de aceptarlo usando la fórmula física: P = e^(Delta_E / T)
            probabilidad = math.exp(delta_e / temperatura)
            dado = random.random() # Genera un número del 0.0 al 1.0
            
            if dado < probabilidad:
                print(f"    -> ⚠️ BAJANDO hacia '{vecino_candidato}' (Probabilidad: {probabilidad:.2f} | Dado: {dado:.2f})")
                estado_actual = vecino_candidato
            else:
                print(f"    -> 🚫 Rechazando bajar a '{vecino_candidato}' (Probabilidad: {probabilidad:.2f} | Dado: {dado:.2f})")
                
        # Al final de cada paso, enfriamos el sistema un poco
        temperatura = temperatura * factor_enfriamiento

    return mejor_global, altitudes[mejor_global]

# ==========================================
# ZONA DE PRUEBAS (Grafo con Máximo Local)
# ==========================================

# Diseñé este grafo específicamente para engañar a algoritmos ciegos.
# A conecta con B y C. 
# B lleva a D (Altura 70 - ¡Una trampa de Máximo Local!)
# C obliga a bajar drásticamente (Altura 20), pero es el único puente hacia E (Altura 100).
grafo_elevaciones = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'E'],
    'D': ['B'], # Callejón sin salida (Máximo Local)
    'E': ['C']  # Meta real (Máximo Global)
}

# Diccionario de altitudes (Nuestro mapa topográfico)
altitudes_ciudades = {
    'A': 50,
    'B': 60,
    'C': 20, # ¡Aquí hay que sufrir para poder ganar!
    'D': 70, # La cima engañosa
    'E': 100 # El verdadero Monte Everest
}

punto_de_partida = 'A'

# Parámetros físicos
temp_inicial = 100.0
factor_enfriamiento = 0.85 # En cada paso perdemos el 15% del calor
max_pasos = 30

# Ojo: Como usa probabilidad aleatoria, el resultado puede variar en cada ejecución.
# A veces caerá en la trampa, a veces logrará cruzar a la cima E.
mejor_nodo, mejor_altitud = temple_simulado(
    grafo_elevaciones, 
    altitudes_ciudades, 
    punto_de_partida, 
    temp_inicial, 
    factor_enfriamiento, 
    max_pasos
)

print(f"\n Terminado. El punto más alto descubierto fue '{mejor_nodo}' con una altura de {mejor_altitud}.")