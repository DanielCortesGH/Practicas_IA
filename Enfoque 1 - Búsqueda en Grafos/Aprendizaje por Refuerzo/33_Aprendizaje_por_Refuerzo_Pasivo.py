import random

# ==========================================
# LA CAJA NEGRA (El Mundo Real)
# El agente NO tiene acceso a ver cómo funciona esto por dentro.
# ==========================================
def interactuar_con_mundo(estado_actual, accion):
    """Simula la física. Devuelve (nuevo_estado, recompensa)"""
    pasillo = ['Inicio', 'A', 'B', 'Meta (+10)', 'Trampa (-10)']
    idx = pasillo.index(estado_actual)
    
    # Física secreta del hielo: 80% de éxito, 20% de resbalar hacia atrás
    resbala = random.random() < 0.20
    
    if accion == 'Derecha':
        nuevo_idx = idx - 1 if resbala else idx + 1
    else: # Si fuera a la izquierda
        nuevo_idx = idx + 1 if resbala else idx - 1
        
    # Evitar salirnos de los bordes (chocar con pared)
    nuevo_idx = max(0, min(nuevo_idx, len(pasillo)-1))
    nuevo_estado = pasillo[nuevo_idx]
    
    # Recompensas secretas del mundo
    if nuevo_estado == 'Meta (+10)': return nuevo_estado, 10.0
    if nuevo_estado == 'Trampa (-10)': return nuevo_estado, -10.0
    
    return nuevo_estado, -0.1 # Costo de batería por dar un paso

# ==========================================
# EL CEREBRO DEL AGENTE (Aprendizaje TD)
# ==========================================
def aprendizaje_td_pasivo(episodios, alpha=0.1, gamma=0.9):
    print("--- Iniciando Aprendizaje por Diferencia Temporal (TD) ---")
    
    # El agente inicia su cerebro en blanco (Todo vale 0)
    estados_conocidos = ['Inicio', 'A', 'B']
    utilidades = {e: 0.0 for e in estados_conocidos}
    
    # La Política Fija: ¡Avanzar a la derecha cueste lo que cueste!
    politica_fija = {e: 'Derecha' for e in estados_conocidos}
    
    # El agente vivirá muchas "vidas" o episodios para aprender
    for episodio in range(1, episodios + 1):
        estado_actual = 'Inicio'
        
        # Sigue caminando hasta caer en la Meta o en la Trampa
        while estado_actual not in ['Meta (+10)', 'Trampa (-10)']:
            
            # 1. Consulta su regla estricta
            accion = politica_fija[estado_actual]
            
            # 2. Ejecuta la acción a ciegas y observa qué pasa
            nuevo_estado, recompensa = interactuar_con_mundo(estado_actual, accion)
            
            # 3. ACTUALIZACIÓN TD (La magia del aprendizaje)
            # Solo actualiza si no es un estado terminal (para simplificar)
            if nuevo_estado not in ['Meta (+10)', 'Trampa (-10)']:
                estimacion_futura = utilidades[nuevo_estado]
            else:
                estimacion_futura = 0.0 # El juego termina ahí
                
            # Aplicamos la fórmula matemática TD
            error_td = recompensa + (gamma * estimacion_futura) - utilidades[estado_actual]
            utilidades[estado_actual] += alpha * error_td
            
            # 4. Avanza mentalmente al siguiente estado
            estado_actual = nuevo_estado
            
        # Imprimimos el progreso mental del robot cada 100 vidas
        if episodio % 100 == 0:
            print(f"Episodio {episodio:03d} | Utilidades aprendidas: Inicio={utilidades['Inicio']:.2f}, A={utilidades['A']:.2f}, B={utilidades['B']:.2f}")
            
    print("\n✅ Entrenamiento terminado.")
    return utilidades

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Ejecutamos 500 simulaciones de la vida del robot
utilidades_finales = aprendizaje_td_pasivo(episodios=500, alpha=0.1, gamma=0.9)

print("\n Lo que el robot cree que vale el mundo tras la experiencia:")
for estado, valor in utilidades_finales.items():
    print(f"  Casilla '{estado}': {valor:.2f} pts de utilidad")