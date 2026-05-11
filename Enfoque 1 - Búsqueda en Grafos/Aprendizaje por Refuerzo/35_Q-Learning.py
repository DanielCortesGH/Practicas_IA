import random

# ==========================================
# EL ENTORNO FÍSICO (Horno 230V con control TRIAC)
# ==========================================
def simular_horno(estado_temperatura, accion_triac):
    """
    Simula la inercia térmica del horno.
    Estados: 0 (Muy Frío) a 4 (Peligro de Fusión). Ideal = 2.
    """
    # Inercia térmica: el horno siempre tiende a enfriarse si no se le inyecta potencia
    enfriamiento_natural = -1 if random.random() < 0.3 else 0 
    
    cambio_temp = enfriamiento_natural
    
    if accion_triac == 'Aumentar_Potencia':
        cambio_temp += 1
    elif accion_triac == 'Reducir_Potencia':
        cambio_temp -= 1
        
    # Calculamos la nueva temperatura limitándola entre 0 y 4
    nueva_temp = max(0, min(4, estado_temperatura + cambio_temp))
    
    # SISTEMA DE RECOMPENSAS (La función de utilidad del ingeniero)
    if nueva_temp == 2:
        recompensa = 10.0  # ¡Perfecto! Temperatura ideal
    elif nueva_temp == 4:
        recompensa = -50.0 # ¡CRÍTICO! Riesgo de dañar resistencias
    elif nueva_temp == 0:
        recompensa = -10.0 # Muy frío, proceso de producción detenido
    else:
        recompensa = -1.0  # Cerca, pero no ideal (1 o 3)
        
    return nueva_temp, recompensa

# ==========================================
# EL MOTOR Q-LEARNING
# ==========================================
def entrenar_controlador_termico(episodios=2000, alpha=0.1, gamma=0.9):
    print("--- Entrenando Controlador TRIAC con Q-Learning ---")
    
    # 0=Muy Frío, 1=Frío, 2=Ideal, 3=Caliente, 4=Peligro
    estados = [0, 1, 2, 3, 4] 
    acciones = ['Reducir_Potencia', 'Mantener', 'Aumentar_Potencia']
    
    # Inicializamos la Tabla Q
    tabla_Q = {s: {a: 0.0 for a in acciones} for s in estados}
    epsilon = 1.0 # 100% de exploración al inicio
    
    for episodio in range(1, episodios + 1):
        # El horno empieza frío todos los días
        estado = 0 
        
        # Simulamos 50 ciclos de reloj por episodio
        for paso in range(50):
            
            # 1. Estrategia Epsilon-Greedy
            if random.uniform(0, 1) < epsilon:
                accion = random.choice(acciones)
            else:
                accion = max(tabla_Q[estado], key=tabla_Q[estado].get)
                
            # 2. El hardware actúa
            nuevo_estado, recompensa = simular_horno(estado, accion)
            
            # 3. ACTUALIZACIÓN MATEMÁTICA OFF-POLICY
            max_q_futuro = max(tabla_Q[nuevo_estado].values())
            
            # Ecuación de Q-Learning
            tabla_Q[estado][accion] = tabla_Q[estado][accion] + alpha * (recompensa + gamma * max_q_futuro - tabla_Q[estado][accion])
            
            estado = nuevo_estado
            
        # Decaimiento del epsilon: el controlador deja de explorar y se vuelve preciso
        if epsilon > 0.01:
            epsilon *= 0.995
            
    print(" Entrenamiento finalizado.")
    return tabla_Q

# ==========================================
# ZONA DE PRUEBAS Y ANÁLISIS
# ==========================================

q_table = entrenar_controlador_termico()

print("\n LEY DE CONTROL APRENDIDA (Tabla de verdad del microcontrolador):")
nombres_estados = {0: 'Muy Frío', 1: 'Frío', 2: 'IDEAL', 3: 'Caliente', 4: 'PELIGRO MÁXIMO'}

for estado in range(5):
    mejor_accion = max(q_table[estado], key=q_table[estado].get)
    # Formateamos para ver el valor Q asociado
    valor_q = q_table[estado][mejor_accion]
    print(f"  Si Temp es [{nombres_estados[estado]}] -> Acción: {mejor_accion} (Certeza: {valor_q:.1f})")