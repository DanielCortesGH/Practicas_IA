import random

# ==========================================
# 1. LA RED BAYESIANA (CPTs)
# ==========================================
# P(Lluvia)
P_Lluvia = 0.20 

# P(Trafico | Lluvia)
def prob_trafico(lluvia):
    return 0.90 if lluvia else 0.30

# P(Tarde | Trafico)
def prob_tarde(trafico):
    return 0.80 if trafico else 0.10

def tirar_dado(probabilidad):
    return random.random() < probabilidad

# ==========================================
# 2. EL MOTOR MCMC (Gibbs Sampling)
# ==========================================
def muestreo_gibbs(consulta, evidencia, iteraciones=10000):
    print(f"--- Iniciando Muestreo de Gibbs ({iteraciones} pasos) ---")
    
    # 1. ESTADO INICIAL (El Universo Mutante)
    # Las variables de evidencia se quedan fijas. 
    # Las variables ocultas y la consulta se inicializan al azar.
    universo = {
        'Lluvia': random.choice([True, False]),
        'Trafico': random.choice([True, False]),
        'Llegar_Tarde': evidencia['Llegar_Tarde'] # ¡PEGAMENTO! Esta no cambia.
    }
    
    conteo_consulta_true = 0
    
    # El Período de "Calentamiento" (Burn-in)
    # Dejamos que el universo mute un poco antes de empezar a tomar fotos
    for _ in range(100):
        mutar_universo(universo)
        
    # 2. LA CADENA DE MARKOV (Tomando fotos)
    for _ in range(iteraciones):
        mutar_universo(universo)
        
        # Tomamos la "Foto" y contamos
        if universo[consulta] == True:
            conteo_consulta_true += 1
            
    probabilidad_final = conteo_consulta_true / iteraciones
    return probabilidad_final

def mutar_universo(universo):
    """
    El corazón de Gibbs: Toma UNA variable no-evidencia a la vez,
    y tira un dado para cambiarla basándose ÚNICAMENTE en su Manto de Markov.
    """
    # 1. Intentamos mutar la Lluvia
    # El Manto de Markov de Lluvia es el Trafico (su hijo). 
    # Por el Teorema de Bayes: P(Lluvia|Trafico) = P(Lluvia) * P(Trafico|Lluvia) / P(Trafico)
    
    # Calculamos el peso de que Lluvia sea True en las condiciones actuales
    peso_true = P_Lluvia * (prob_trafico(True) if universo['Trafico'] else (1 - prob_trafico(True)))
    # Calculamos el peso de que Lluvia sea False
    peso_false = (1 - P_Lluvia) * (prob_trafico(False) if universo['Trafico'] else (1 - prob_trafico(False)))
    
    # Normalizamos para obtener la probabilidad de tirar el dado
    prob_mutar_lluvia = peso_true / (peso_true + peso_false)
    universo['Lluvia'] = tirar_dado(prob_mutar_lluvia)
    
    
    # 2. Intentamos mutar el Tráfico
    # El Manto de Markov de Tráfico es Lluvia (padre) y Llegar_Tarde (hijo).
    
    # Peso de que Trafico sea True
    p_t_true = prob_trafico(universo['Lluvia']) * (prob_tarde(True) if universo['Llegar_Tarde'] else (1 - prob_tarde(True)))
    # Peso de que Trafico sea False
    p_t_false = (1 - prob_trafico(universo['Lluvia'])) * (prob_tarde(False) if universo['Llegar_Tarde'] else (1 - prob_tarde(False)))
    
    prob_mutar_trafico = p_t_true / (p_t_true + p_t_false)
    universo['Trafico'] = tirar_dado(prob_mutar_trafico)
    
    # *Nota: No intentamos mutar 'Llegar_Tarde' porque es nuestra EVIDENCIA (está pegada).

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

evidencia_sensores = {'Llegar_Tarde': True}
resultado = muestreo_gibbs(consulta='Lluvia', evidencia=evidencia_sensores, iteraciones=20000)

print("-" * 50)
print(f"📊 DIAGNÓSTICO MCMC: P(Lluvia | Llegar_Tarde) ≈ {resultado * 100:.2f}%")