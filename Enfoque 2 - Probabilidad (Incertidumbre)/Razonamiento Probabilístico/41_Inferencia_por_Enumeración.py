# ==========================================
# 1. LA RED BAYESIANA (Estructura y CPTs)
# ==========================================
red_neumatica = {
    'Fuga': {
        'padres': [],
        'prob': {(): 0.10} # 10% de probabilidad de que haya una fuga de aire
    },
    'Baja_Presion': {
        'padres': ['Fuga'],
        'prob': {
            (True,): 0.95,  # Si hay fuga, 95% de baja presión
            (False,): 0.05  # Si no hay fuga, 5% de fallo espontáneo del compresor
        }
    },
    'Alarma': {
        'padres': ['Baja_Presion'],
        'prob': {
            (True,): 0.90,  # Si la presión es baja, la alarma suena (90% confiable)
            (False,): 0.01  # Falsa alarma (1%)
        }
    }
}

def obtener_probabilidad_condicional(variable, valor, evidencia_actual, bn):
    """Extrae el número exacto de la tabla de probabilidad (CPT)."""
    padres = bn[variable]['padres']
    valores_padres = tuple(evidencia_actual[p] for p in padres)
    
    prob_verdadero = bn[variable]['prob'][valores_padres]
    return prob_verdadero if valor else (1.0 - prob_verdadero)

# ==========================================
# 2. EL ALGORITMO DE ENUMERACIÓN
# ==========================================
def enumerar_todos(variables, evidencia_actual, bn):
    """
    Función recursiva que recorre el árbol de probabilidades.
    Si la variable está oculta, suma las ramas True y False.
    """
    # Condición de parada: Si ya no hay variables, el cálculo de esta rama terminó (es 1.0)
    if not variables:
        return 1.0
        
    Y = variables[0]
    resto_variables = variables[1:]
    
    # CASO A: La variable ya es conocida (Es Consulta o Evidencia)
    if Y in evidencia_actual:
        prob = obtener_probabilidad_condicional(Y, evidencia_actual[Y], evidencia_actual, bn)
        # Multiplicamos (Regla de la cadena) y seguimos bajando
        return prob * enumerar_todos(resto_variables, evidencia_actual, bn)
        
    # CASO B: La variable es OCULTA. Tenemos que Marginalizar (Sumar)
    else:
        suma_total = 0.0
        for valor_hipotetico in [True, False]:
            # Clonamos la evidencia y le "inventamos" este valor hipotético
            nueva_evidencia = evidencia_actual.copy()
            nueva_evidencia[Y] = valor_hipotetico
            
            prob = obtener_probabilidad_condicional(Y, valor_hipotetico, nueva_evidencia, bn)
            # Acumulamos el resultado de explorar esta rama
            suma_total += prob * enumerar_todos(resto_variables, nueva_evidencia, bn)
            
        return suma_total

def inferencia_por_enumeracion(variable_consulta, evidencia, bn):
    """
    Calcula P(Consulta | Evidencia) probando Consulta=True y Consulta=False,
    y luego normalizando los resultados usando a (Alpha).
    """
    print(f"--- Ejecutando Inferencia: P({variable_consulta} | {evidencia}) ---")
    distribucion_Q = {}
    
    todas_las_variables = list(bn.keys()) # ['Fuga', 'Baja_Presion', 'Alarma']
    
    for valor_consulta in [True, False]:
        evidencia_extendida = evidencia.copy()
        evidencia_extendida[variable_consulta] = valor_consulta
        
        # Desatamos la recursividad para este valor
        resultado_suma = enumerar_todos(todas_las_variables, evidencia_extendida, bn)
        distribucion_Q[valor_consulta] = resultado_suma
        print(f"  > Σ(Universos donde {variable_consulta}={valor_consulta}) = {resultado_suma:.6f}")
        
    # FACTOR DE NORMALIZACIÓN (Alpha)
    suma_alpha = distribucion_Q[True] + distribucion_Q[False]
    prob_final_true = distribucion_Q[True] / suma_alpha
    prob_final_false = distribucion_Q[False] / suma_alpha
    
    print("-" * 40)
    print(f"✅ Probabilidad Normalizada:")
    print(f"   P({variable_consulta} = Verdadero) : {prob_final_true*100:.2f}%")
    print(f"   P({variable_consulta} = Falso)     : {prob_final_false*100:.2f}%")
    
    return prob_final_true

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Pregunta: ¿Cuál es la probabilidad de que haya una fuga real (Consulta),
# dado que escuchamos la Alarma sonando (Evidencia)?
# *Nota: La "Baja_Presion" es una variable oculta, el algoritmo la marginará automáticamente.

evidencia_sensores = {'Alarma': True}
inferencia_por_enumeracion('Fuga', evidencia_sensores, red_neumatica)