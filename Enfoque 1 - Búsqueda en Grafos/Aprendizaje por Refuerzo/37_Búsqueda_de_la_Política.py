import random

# ==========================================
# LA FÍSICA DEL DRON (El Entorno)
# ==========================================
def simular_vuelo(w1, w2):
    """
    Simula un vuelo usando la política matemática definida por w1 y w2.
    Devuelve el tiempo total (en ciclos) que el dron logró mantenerse en el aire.
    """
    angulo = random.uniform(-0.5, 0.5) # Inclinación inicial aleatoria
    velocidad = 0.0
    tiempo_supervivencia = 0
    
    # Simulamos un máximo de 500 ciclos (Si llega a 500, el vuelo fue perfecto)
    for ciclo in range(500):
        # 1. LA POLÍTICA MATEMÁTICA: Decide la fuerza directamente
        fuerza_motores = (w1 * angulo) + (w2 * velocidad)
        
        # 2. Física básica (La fuerza cambia la velocidad, la velocidad cambia el ángulo)
        velocidad += fuerza_motores + random.uniform(-0.05, 0.05) # Añadimos viento (ruido)
        angulo += velocidad
        
        # 3. Condición de falla (Si se voltea más de 90 grados, se estrella)
        if abs(angulo) > 1.5: # 1.5 radianes ~= 85 grados
            break
            
        tiempo_supervivencia += 1
        
    return tiempo_supervivencia

# ==========================================
# EL MOTOR DE BÚSQUEDA (Hill Climbing)
# ==========================================
def busqueda_politica_hill_climbing(iteraciones=1000):
    print("--- Iniciando Búsqueda de Política (Ascenso de Colina) ---")
    
    # 1. Configuración inicial completamente al azar (Theta = [w1, w2])
    mejores_pesos = [random.uniform(-1, 1), random.uniform(-1, 1)]
    mejor_puntuacion = simular_vuelo(mejores_pesos[0], mejores_pesos[1])
    
    print(f"[{'Inicio'}] Pesos aleatorios: w1={mejores_pesos[0]:.3f}, w2={mejores_pesos[1]:.3f} | Sobrevivió: {mejor_puntuacion} ciclos")
    
    # 2. El ciclo de optimización
    for i in range(1, iteraciones + 1):
        # Añadimos "ruido" a nuestras mejores perillas para explorar configuraciones cercanas
        ruido_w1 = random.uniform(-0.1, 0.1)
        ruido_w2 = random.uniform(-0.1, 0.1)
        
        pesos_candidatos = [mejores_pesos[0] + ruido_w1, mejores_pesos[1] + ruido_w2]
        
        # Probamos la nueva configuración en el simulador
        puntuacion_candidata = simular_vuelo(pesos_candidatos[0], pesos_candidatos[1])
        
        # 3. Si la nueva política es mejor, sobreescribimos nuestro cerebro
        if puntuacion_candidata > mejor_puntuacion:
            mejores_pesos = pesos_candidatos
            mejor_puntuacion = puntuacion_candidata
            print(f"[Iteración {i}] ¡Mejora! Nuevos pesos: w1={mejores_pesos[0]:.3f}, w2={mejores_pesos[1]:.3f} | Sobrevivió: {mejor_puntuacion} ciclos")
            
            # Si logramos el vuelo perfecto (500 ciclos), detenemos la búsqueda
            if mejor_puntuacion == 500:
                print("\n ¡POLÍTICA ÓPTIMA ENCONTRADA! El dron es perfectamente estable.")
                break

    return mejores_pesos

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

pesos_finales = busqueda_politica_hill_climbing()

print("\n ECUACIÓN DEL CONTROLADOR FINAL:")
print(f"Fuerza_Motores = ({pesos_finales[0]:.3f} * Angulo) + ({pesos_finales[1]:.3f} * Velocidad)")