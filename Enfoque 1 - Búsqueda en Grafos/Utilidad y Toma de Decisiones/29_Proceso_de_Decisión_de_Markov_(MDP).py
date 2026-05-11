class ProcesoDecisionMarkov:
    """
    TEMA 29: Representación formal de un MDP.
    Actúa como el 'Motor Físico' o el 'Mundo' con el que interactúa el agente.
    """
    def __init__(self, estados, acciones, transiciones, recompensas, gamma=0.9):
        self.S = estados           # Lista de estados
        self.A = acciones          # Lista de acciones posibles
        self.P = transiciones      # Diccionario anidado: P[estado][accion] = [(prob, estado_siguiente), ...]
        self.R = recompensas       # Diccionario de utilidades/puntos por estado
        self.gamma = gamma         # Factor de descuento

    def obtener_estados(self):
        return self.S

    def obtener_acciones(self, estado):
        """Devuelve las acciones legales desde un estado específico."""
        # Si el estado es una meta o un pozo, no hay acciones posibles (Juego terminado)
        if self.R.get(estado, 0) >= 100 or self.R.get(estado, 0) <= -100:
            return []
        return self.A

    def obtener_transiciones(self, estado, accion):
        """
        La Propiedad de Markov en acción: 
        Devuelve las probabilidades de a dónde irás a parar (s') 
        solo conociendo tu estado actual (s) y tu acción (a).
        """
        if estado not in self.P or accion not in self.P[estado]:
            return [(1.0, estado)] # Si intentas algo inválido, te quedas donde mismo
            
        return self.P[estado][accion]

    def obtener_recompensa(self, estado):
        """Devuelve el valor R(s) de estar en este estado."""
        return self.R.get(estado, 0.0)

# ==========================================
# ZONA DE USO (Instanciando nuestro Mundo Mecatrónico)
# ==========================================

# 1. Definimos S y A
estados_laboratorio = ['Entrada', 'Pasillo', 'Mesa de Trabajo (Meta)']
comandos_motor = ['Avanzar', 'Retroceder']

# 2. Definimos P (La física del entorno con ruido/error)
# Formato: P[estado][accion] = [(Probabilidad, Estado_Destino), ...]
modelo_fisico = {
    'Entrada': {
        'Avanzar': [(0.9, 'Pasillo'), (0.1, 'Entrada')], # 10% de probabilidad de que la llanta patine
        'Retroceder': [(1.0, 'Entrada')] # Choca con la pared, se queda ahí
    },
    'Pasillo': {
        'Avanzar': [(0.8, 'Mesa de Trabajo (Meta)'), (0.2, 'Pasillo')],
        'Retroceder': [(0.95, 'Entrada'), (0.05, 'Pasillo')]
    }
}

# 3. Definimos R (Las recompensas)
sistema_puntos = {
    'Entrada': -1.0,  
    'Pasillo': -2.0,  # El pasillo gasta más batería por la fricción
    'Mesa de Trabajo (Meta)': 100.0 # ¡Objetivo cumplido!
}

# 4. Empaquetamos todo en nuestro Objeto MDP formal
entorno_mdp = ProcesoDecisionMarkov(
    estados=estados_laboratorio, 
    acciones=comandos_motor, 
    transiciones=modelo_fisico, 
    recompensas=sistema_puntos, 
    gamma=0.95
)

print("--- Entorno MDP Inicializado Exitosamente ---")
print(f" Espacio de Estados (S): {entorno_mdp.obtener_estados()}")
print(f"  Espacio de Acciones (A): {entorno_mdp.A}")

print("\n Simulando una consulta de la Propiedad de Markov:")
print("Pregunta del Agente: 'Estoy en el Pasillo y mis motores reciben comando Avanzar. ¿Qué pasará?'")
posibles_futuros = entorno_mdp.obtener_transiciones('Pasillo', 'Avanzar')

for probabilidad, destino in posibles_futuros:
    print(f"  -> Hay {probabilidad*100}% de probabilidad de terminar en: '{destino}'")