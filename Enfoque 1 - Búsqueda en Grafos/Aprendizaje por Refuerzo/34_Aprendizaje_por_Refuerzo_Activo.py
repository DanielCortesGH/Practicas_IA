import random

# ==========================================
# EL ENTORNO (La Caja Negra física)
# ==========================================
def mundo_desconocido(estado, accion):
    """Devuelve (nuevo_estado, recompensa, es_terminal)"""
    # Mapa simplificado: 
    # [Inicio] -> [Atajo_Peligroso] -> [Meta (+100)]
    #          -> [Trampa (-100)] (Pegada al atajo)
    # [Inicio] -> [Camino_Largo_1] -> [Camino_Largo_2] -> [Meta (+100)]
    
    if estado == 'Inicio':
        if accion == 'Derecha': return 'Camino_Largo_1', -1, False
        if accion == 'Arriba': return 'Atajo_Peligroso', -1, False
        
    elif estado == 'Camino_Largo_1':
        if accion == 'Derecha': return 'Camino_Largo_2', -1, False
        
    elif estado == 'Camino_Largo_2':
        if accion == 'Arriba': return 'Meta (+100)', 100, True
        
    elif estado == 'Atajo_Peligroso':
        # El motor falla a veces (20% de probabilidad de caer en la trampa en el atajo)
        if accion == 'Derecha':
            if random.random() < 0.20:
                return 'Trampa (-100)', -100, True
            else:
                return 'Meta (+100)', 100, True
                
    # Si choca con pared o hace acción inválida, se queda en el lugar perdiendo batería
    return estado, -5, False

# ==========================================
# EL CEREBRO DEL ROBOT (Q-Learning)
# ==========================================
def entrenar_q_learning(episodios=1000, alpha=0.1, gamma=0.9, epsilon_inicial=1.0):
    print("--- Iniciando Entrenamiento Q-Learning ---")
    
    estados = ['Inicio', 'Camino_Largo_1', 'Camino_Largo_2', 'Atajo_Peligroso', 'Meta (+100)', 'Trampa (-100)']
    acciones = ['Arriba', 'Abajo', 'Izquierda', 'Derecha']
    
    # 1. INICIALIZAR TABLA Q: Todo empieza en cero
    # Q[estado][accion] = valor numérico
    tabla_Q = {s: {a: 0.0 for a in acciones} for s in estados}
    
    epsilon = epsilon_inicial # Probabilidad de explorar (1.0 = 100% aleatorio al inicio)
    
    for episodio in range(1, episodios + 1):
        estado_actual = 'Inicio'
        terminado = False
        
        while not terminado:
            # 2. SELECCIÓN DE ACCIÓN (Estrategia Epsilon-Greedy)
            if random.uniform(0, 1) < epsilon:
                accion = random.choice(acciones) # EXPLORACIÓN: Acción loca
            else:
                # EXPLOTACIÓN: La mejor acción según la Tabla Q
                accion = max(tabla_Q[estado_actual], key=tabla_Q[estado_actual].get)
                
            # 3. INTERACCIÓN FÍSICA
            nuevo_estado, recompensa, terminado = mundo_desconocido(estado_actual, accion)
            
            # 4. ACTUALIZACIÓN MATEMÁTICA (La Ecuación de Bellman para Q)
            # Buscamos cuál sería la mejor acción futura en el nuevo estado
            max_q_futuro = max(tabla_Q[nuevo_estado].values())
            
            # Calculamos el error TD
            error_td = recompensa + (gamma * max_q_futuro) - tabla_Q[estado_actual][accion]
            
            # Actualizamos nuestra base de conocimientos
            tabla_Q[estado_actual][accion] += alpha * error_td
            
            estado_actual = nuevo_estado
            
        # Al terminar cada vida, reducimos el épsilon para que el robot madure
        # (Pasa de explorar a explotar)
        if epsilon > 0.01:
            epsilon *= 0.99
            
    print(" Entrenamiento completado (1000 vidas jugadas).")
    return tabla_Q

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

q_table_final = entrenar_q_learning()

print("\n LA POLÍTICA ÓPTIMA DESCUBIERTA (El Instinto del Robot):")
estados_clave = ['Inicio', 'Camino_Largo_1', 'Camino_Largo_2', 'Atajo_Peligroso']

for estado in estados_clave:
    # Obtenemos la acción con el número más alto en la tabla Q para ese estado
    mejor_accion = max(q_table_final[estado], key=q_table_final[estado].get)
    puntaje = q_table_final[estado][mejor_accion]
    print(f"   En '{estado}' -> ¡Debo ir hacia {mejor_accion}! (Confianza: {puntaje:.1f})")