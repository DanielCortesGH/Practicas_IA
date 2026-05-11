# ==========================================
# 1. DEFINICIÓN DE FACTORES (Tablas sueltas)
# ==========================================
# Factor 1: P(Lluvia)
f_lluvia = {
    'Lluvia_True': 0.20,
    'Lluvia_False': 0.80
}

# Factor 2: P(Trafico | Lluvia)
f_trafico = {
    ('Lluvia_True', 'Trafico_True'): 0.90,
    ('Lluvia_True', 'Trafico_False'): 0.10,
    ('Lluvia_False', 'Trafico_True'): 0.30,
    ('Lluvia_False', 'Trafico_False'): 0.70
}

# Factor 3: P(Tarde | Trafico)
f_tarde = {
    ('Trafico_True', 'Tarde_True'): 0.80,
    ('Trafico_True', 'Tarde_False'): 0.20,
    ('Trafico_False', 'Tarde_True'): 0.10,
    ('Trafico_False', 'Tarde_False'): 0.90
}

def multiplicar_y_eliminar(factor_A, factor_B, variable_a_eliminar):
    """
    TEMA 42: El corazón del algoritmo.
    Primero multiplica los factores que comparten la variable, 
    y luego suma (elimina) esa variable para crear un factor nuevo y más pequeño.
    """
    print(f"\n⚙️ Iniciando Eliminación de la variable oculta: '{variable_a_eliminar}'")
    
    # PASO 1: Multiplicar los dos factores (Ej. P(Trafico|Lluvia) * P(Tarde|Trafico))
    factor_combinado = {}
    
    # Buscamos coincidencias de la variable compartida
    for key_a, prob_a in factor_A.items():
        for key_b, prob_b in factor_B.items():
            
            # Encontramos el estado de la variable en ambos factores (True o False)
            estado_var_a = [k for k in key_a if variable_a_eliminar in k][0]
            estado_var_b = [k for k in key_b if variable_a_eliminar in k][0]
            
            # Si coinciden (Ej. ambos dicen 'Trafico_True'), se multiplican
            if estado_var_a == estado_var_b:
                # Extraemos las variables restantes (Las que NO vamos a eliminar)
                resto_a = [k for k in key_a if k != estado_var_a][0]
                resto_b = [k for k in key_b if k != estado_var_b][0]
                
                nueva_llave = (resto_a, resto_b, estado_var_a)
                factor_combinado[nueva_llave] = prob_a * prob_b
                
    print("  [1] Factores multiplicados exitosamente.")

    # PASO 2: Sum Out (Eliminar / Marginalizar)
    factor_reducido = {}
    
    for llave, prob in factor_combinado.items():
        # Separamos las variables que sobreviven de la que va a morir
        vars_sobrevivientes = (llave[0], llave[1]) # (Lluvia_x, Tarde_x)
        
        # Sumamos las probabilidades (Agrupando 'Trafico_True' y 'Trafico_False')
        if vars_sobrevivientes in factor_reducido:
            factor_reducido[vars_sobrevivientes] += prob
        else:
            factor_reducido[vars_sobrevivientes] = prob
            
    print(f"  [2] Variable '{variable_a_eliminar}' marginalizada y eliminada.")
    return factor_reducido

# ==========================================
# ZONA DE PRUEBAS (Ejecutando el Algoritmo)
# ==========================================
print("--- Algoritmo de Eliminación de Variables ---")

# Nuestro objetivo es calcular P(Lluvia, Tarde) sin que nos importe el Tráfico.
# Le pasamos el Factor 2 y Factor 3 para que los fusione y elimine el 'Trafico'
nuevo_factor_f3_f2 = multiplicar_y_eliminar(f_trafico, f_tarde, variable_a_eliminar='Trafico')

print("\n📊 RESULTADO (El Nuevo Factor):")
# Este nuevo factor relaciona Lluvia DIRECTAMENTE con Llegar Tarde, 
# habiendo absorbido la incertidumbre del tráfico.
for llave, prob in nuevo_factor_f3_f2.items():
    print(f"  P({llave[0]}, {llave[1]}) = {prob:.4f}")