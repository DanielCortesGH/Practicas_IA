import random

# ==========================================
# 1. EL ENTORNO (El vuelo real y ruidoso)
# ==========================================
def simular_vuelo_y_sensor(altitud_real_anterior, movimiento_comandado):
    """Simula la física imperfecta y el sensor barato."""
    # 1. El viento empuja el dron al azar (Ruido de Proceso)
    viento = random.gauss(mu=0.0, sigma=0.5) 
    altitud_real_nueva = altitud_real_anterior + movimiento_comandado + viento
    
    # 2. El sensor GPS/Barómetro tiene mucha estática (Ruido de Medición)
    ruido_sensor = random.gauss(mu=0.0, sigma=3.0) 
    lectura_sensor = altitud_real_nueva + ruido_sensor
    
    return altitud_real_nueva, lectura_sensor

# ==========================================
# 2. EL FILTRO DE KALMAN
# ==========================================
class FiltroKalman1D:
    def __init__(self, altitud_inicial, incertidumbre_inicial, Q, R):
        self.x = altitud_inicial      # Estado estimado
        self.P = incertidumbre_inicial # Incertidumbre inicial (Varianza)
        self.Q = Q # Ruido del Proceso (¿Qué tanto confío en mi física?)
        self.R = R # Ruido del Sensor (¿Qué tanto confío en mi sensor?)
        
    def ciclo_kalman(self, movimiento_comandado, lectura_z):
        # --- PASO 1: PREDICCIÓN (Física) ---
        x_pred = self.x + movimiento_comandado
        P_pred = self.P + self.Q
        
        # --- PASO 2: ACTUALIZACIÓN (Ganancia de Kalman) ---
        # Calculamos a quién creerle más
        K = P_pred / (P_pred + self.R)
        
        # Corregimos nuestra predicción tirando hacia lo que dice el sensor
        self.x = x_pred + K * (lectura_z - x_pred)
        
        # Reducimos nuestra incertidumbre (porque acabamos de medir)
        self.P = (1 - K) * P_pred
        
        return self.x, K

# ==========================================
# ZONA DE PRUEBAS
# ==========================================
print("--- Iniciando Telemetría: Filtro de Kalman ---")

# Configuración del motor de inferencia
# Q=0.1 (Creemos mucho en nuestra física), R=10.0 (Sabemos que el sensor es terrible)
filtro = FiltroKalman1D(altitud_inicial=0.0, incertidumbre_inicial=1.0, Q=0.1, R=10.0)

altitud_real = 0.0
movimiento_vertical = 2.0 # El dron intenta subir 2 metros por segundo

print("Seg | Altitud REAL | Lectura SENSOR | Estimación KALMAN | Ganancia K")
print("-" * 70)

for segundo in range(1, 16):
    # El universo avanza un segundo
    altitud_real, lectura_z = simular_vuelo_y_sensor(altitud_real, movimiento_vertical)
    
    # La IA del dron procesa la lectura
    estimacion_limpia, ganancia_K = filtro.ciclo_kalman(movimiento_vertical, lectura_z)
    
    # Formateo visual
    print(f"{segundo:02d}  | {altitud_real:12.2f} | {lectura_z:14.2f} | {estimacion_limpia:17.2f} | {ganancia_K:.3f}")