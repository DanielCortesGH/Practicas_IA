class MotorInferenciaTemporal:
    def __init__(self, prob_inicial, modelo_transicion, modelo_sensor):
        self.creencia_actual = prob_inicial
        self.transicion = modelo_transicion
        self.sensor = modelo_sensor
        
    def normalizar(self, distribucion):
        total = sum(distribucion.values())
        return {k: v / total for k, v in distribucion.items()}

    def filtrado(self, evidencia_actual):
        """
        Calcula P(X_t | e_{1:t}).
        Paso 1: Predice a dónde me llevó el tiempo.
        Paso 2: Actualiza con lo que dice el sensor de HOY.
        """
        estados = list(self.creencia_actual.keys())
        nueva_creencia = {e: 0.0 for e in estados}
        
        for estado_t in estados:
            # 1. Componente de Tiempo (Transición desde t-1)
            suma_tiempo = sum(
                self.transicion[estado_pasado][estado_t] * self.creencia_actual[estado_pasado]
                for estado_pasado in estados
            )
            
            # 2. Componente de Evidencia (Sensor en tiempo t)
            prob_evidencia = self.sensor[estado_t][evidencia_actual]
            
            # Combinamos usando la Ecuación de Filtrado (Regla de Bayes)
            nueva_creencia[estado_t] = prob_evidencia * suma_tiempo
            
        self.creencia_actual = self.normalizar(nueva_creencia)
        return self.creencia_actual

    def prediccion(self, dias_k):
        """
        Calcula P(X_{t+k} | e_{1:t}).
        Avanza el reloj 'k' pasos sin usar ninguna evidencia nueva.
        """
        estados = list(self.creencia_actual.keys())
        creencia_futura = self.creencia_actual.copy()
        
        for k in range(1, dias_k + 1):
            creencia_temporal = {e: 0.0 for e in estados}
            
            for estado_futuro in estados:
                creencia_temporal[estado_futuro] = sum(
                    self.transicion[estado_pasado][estado_futuro] * creencia_futura[estado_pasado]
                    for estado_pasado in estados
                )
            # Como no hay sensores en el futuro, no multiplicamos por evidencia ni normalizamos extra
            creencia_futura = creencia_temporal
            print(f"  -> Predicción a {k} día(s): {creencia_futura['Sano']*100:.1f}% Sano | {creencia_futura['Roto']*100:.1f}% Roto")
            
        return creencia_futura

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# 1. MODELOS FÍSICOS
estado_dia_0 = {'Sano': 0.90, 'Roto': 0.10}

transicion = {
    'Sano': {'Sano': 0.85, 'Roto': 0.15},  # Si está sano, 15% de romperse
    'Roto': {'Sano': 0.00, 'Roto': 1.00}   # Si está roto, se queda roto
}

sensores = {
    'Sano': {'Alta': 0.20, 'Baja': 0.80},  # Motor sano casi no vibra
    'Roto': {'Alta': 0.90, 'Baja': 0.10}   # Motor roto vibra muchísimo
}

IA = MotorInferenciaTemporal(estado_dia_0, transicion, sensores)

# 2. SIMULACIÓN DE OPERACIÓN DIARIA
secuencia_sensores = ['Baja', 'Baja', 'Alta']

print("--- Ejecutando FILTRADO en Tiempo Real ---")
for t, lectura in enumerate(secuencia_sensores, start=1):
    creencia_filtrada = IA.filtrado(lectura)
    print(f"Día {t} | Sensor leyó Vibración '{lectura}' -> Estado Estimado: {creencia_filtrada['Sano']*100:.1f}% Sano")

print("\n--- Ejecutando PREDICCIÓN hacia el Futuro ---")
print("El motor se apagará en 3 días. ¿Cuáles son los riesgos si no medimos nada más?")
IA.prediccion(dias_k=3)