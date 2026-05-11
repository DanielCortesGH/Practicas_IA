import random
import math

# ==========================================
# FUNCIONES AUXILIARES FÍSICAS
# ==========================================
def campana_gauss(mu, sigma, x):
    """Calcula la probabilidad de 'x' en una campana de Gauss."""
    return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))

# ==========================================
# EL ENTORNO (La Realidad Oculta)
# ==========================================
class RobotReal:
    def __init__(self):
        self.x = 10.0 # Empieza en el metro 10
        
    def mover(self, distancia):
        ruido_llantas = random.gauss(0.0, 1.0)
        self.x += distancia + ruido_llantas
        
    def leer_sensor_gps(self):
        ruido_sensor = random.gauss(0.0, 3.0)
        return self.x + ruido_sensor

# ==========================================
# LA INTELIGENCIA ARTIFICIAL (Filtrado de Partículas)
# ==========================================
class FiltroParticulas:
    def __init__(self, num_particulas):
        # 1. POBLACIÓN INICIAL: Esparcimos N clones al azar por todo el pasillo (0 a 100m)
        self.N = num_particulas
        self.particulas = [random.uniform(0.0, 100.0) for _ in range(self.N)]
        self.pesos = [1.0 / self.N] * self.N
        
    def estimar_posicion(self):
        # La posición estimada es el promedio de dónde están todos los clones
        return sum(self.particulas) / self.N

    def ciclo_filtrado(self, movimiento_comandado, lectura_sensor):
        
        # 2. PREDICCIÓN (Movemos los clones con ruido)
        for i in range(self.N):
            ruido_virtual = random.gauss(0.0, 1.0) # Simulamos el derrape
            self.particulas[i] += movimiento_comandado + ruido_virtual
            
        # 3. ACTUALIZACIÓN DE PESOS (¿Qué tan lógico es este clon dado el sensor?)
        suma_pesos = 0.0
        for i in range(self.N):
            # Comparamos dónde está el clon (particulas[i]) con lo que dice el sensor
            # Si el clon está cerca de la lectura, la campana de Gauss le da un peso alto.
            self.pesos[i] = campana_gauss(mu=self.particulas[i], sigma=3.0, x=lectura_sensor)
            suma_pesos += self.pesos[i]
            
        # Normalizamos los pesos para que sumen 1.0
        for i in range(self.N):
            self.pesos[i] /= suma_pesos
            
        # 4. RE-MUESTREO (La Ruleta de la Evolución Darwiniana)
        # Elegimos N nuevos clones de la lista antigua, favoreciendo a los más pesados
        nuevas_particulas = random.choices(self.particulas, weights=self.pesos, k=self.N)
        
        # Sobreescribimos la generación antigua con los sobrevivientes clonados
        self.particulas = nuevas_particulas
        
        return self.estimar_posicion()

# ==========================================
# ZONA DE PRUEBAS
# ==========================================
print("--- Iniciando Filtrado de Partículas (Rastreo 1D) ---")

robot = RobotReal()
ia = FiltroParticulas(num_particulas=100) # Usaremos 100 clones virtuales

print("Paso | Posición REAL | Lectura SENSOR | Estimación IA (Nube)")
print("-" * 65)

for paso in range(1, 11):
    # 1. El mundo avanza
    comando_movimiento = 5.0 # Avanzar 5 metros
    robot.mover(comando_movimiento)
    sensor_z = robot.leer_sensor_gps()
    
    # 2. La IA procesa
    estimacion = ia.ciclo_filtrado(comando_movimiento, sensor_z)
    
    print(f"{paso:02d}   | {robot.x:13.2f} | {sensor_z:14.2f} | {estimacion:19.2f}")