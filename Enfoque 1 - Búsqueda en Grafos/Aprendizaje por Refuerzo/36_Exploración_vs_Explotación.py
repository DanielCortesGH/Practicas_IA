import random

class Tragamonedas:
    def __init__(self, probabilidad_real):
        self.probabilidad_real = probabilidad_real
        
    def jalar_palanca(self):
        # Devuelve 1 (Premio) o 0 (Nada) basado en su probabilidad secreta
        return 1 if random.random() < self.probabilidad_real else 0

class AgenteBandit:
    def __init__(self, num_maquinas, epsilon):
        self.epsilon = epsilon
        # Q(a): Lo que creemos que paga cada máquina
        self.valores_estimados = [0.0] * num_maquinas 
        # N(a): Cuántas veces hemos jalado cada máquina
        self.veces_elegida = [0] * num_maquinas      
        
    def elegir_maquina(self):
        """TEMA 36: El motor de Exploración vs Explotación"""
        if random.random() < self.epsilon:
            # EXPLORACIÓN: Elegimos una al azar
            return random.randint(0, len(self.valores_estimados) - 1)
        else:
            # EXPLOTACIÓN: Elegimos la que tenga el mayor valor estimado
            # (Si hay empate, 'index' y 'max' eligen la primera)
            max_valor = max(self.valores_estimados)
            return self.valores_estimados.index(max_valor)
            
    def actualizar_conocimiento(self, maquina, recompensa):
        # Actualizamos la estadística (Promedio móvil)
        self.veces_elegida[maquina] += 1
        n = self.veces_elegida[maquina]
        valor_actual = self.valores_estimados[maquina]
        
        # Nueva estimación = Estimación vieja + (Error / n)
        self.valores_estimados[maquina] = valor_actual + (1/n) * (recompensa - valor_actual)

# ==========================================
# ZONA DE PRUEBAS (El Casino)
# ==========================================

# 3 Máquinas con probabilidades SECRETAS: 10%, 70%, y 30%
casino = [Tragamonedas(0.1), Tragamonedas(0.7), Tragamonedas(0.3)]

# Nuestro agente con Epsilon 0.1 (10% de exploración)
agente = AgenteBandit(num_maquinas=3, epsilon=0.1)

print("--- Iniciando Simulación de 1000 jugadas ---")

recompensas_totales = 0

for turno in range(1, 1001):
    # 1. El agente decide (Explorar o Explotar)
    maquina_elegida = agente.elegir_maquina()
    
    # 2. El agente jala la palanca
    premio = casino[maquina_elegida].jalar_palanca()
    recompensas_totales += premio
    
    # 3. El agente actualiza su cerebro
    agente.actualizar_conocimiento(maquina_elegida, premio)

print(f"\n Terminado. Se ganaron {recompensas_totales} monedas.")
print("\n Lo que el agente APRENDIÓ de cada máquina:")
for i in range(3):
    prob_real = casino[i].probabilidad_real * 100
    prob_estimada = agente.valores_estimados[i] * 100
    veces = agente.veces_elegida[i]
    print(f"  Máquina {i}: Real [{prob_real:.0f}%] | Agente cree que es [{prob_estimada:.1f}%] | La jugó {veces} veces")