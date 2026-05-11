def obtener_manto_markov(red_bayesiana, nodo_objetivo):
    """
    TEMA 40: Calcula el Manto de Markov de un nodo.
    Retorna los Padres, Hijos y Copadres.
    """
    padres = set()
    hijos = set(red_bayesiana.get(nodo_objetivo, []))
    copadres = set()
    
    # 1. Encontrar los PADRES (¿Quién apunta a mi nodo objetivo?)
    for nodo, lista_hijos in red_bayesiana.items():
        if nodo_objetivo in lista_hijos:
            padres.add(nodo)
            
    # 2. Encontrar los COPADRES (¿Quién más apunta a mis hijos?)
    for hijo in hijos:
        for nodo_potencial_copadre, lista_hijos in red_bayesiana.items():
            if hijo in lista_hijos and nodo_potencial_copadre != nodo_objetivo:
                copadres.add(nodo_potencial_copadre)
                
    # El Manto es la unión de estos tres conjuntos
    manto_completo = padres | hijos | copadres
    
    return {
        'Padres': list(padres),
        'Hijos': list(hijos),
        'Copadres': list(copadres),
        'Manto_Total': list(manto_completo)
    }

# ==========================================
# ZONA DE PRUEBAS (La Red de Judea Pearl)
# ==========================================

# Definimos el grafo dirigido: Diccionario donde Clave = Padre, Valor = [Hijos]
grafo_causal = {
    'Robo': ['Alarma'],
    'Terremoto': ['Alarma', 'Noticias_Radio'],
    'Alarma': ['Juan_Llama', 'Maria_Llama'],
    'Noticias_Radio': [],
    'Juan_Llama': [],
    'Maria_Llama': []
}

print("--- Análisis de Aislamiento Bayesiano (Markov Blanket) ---")

# CASO 1: Queremos aislar el nodo 'Robo'
objetivo = 'Robo'
resultado = obtener_manto_markov(grafo_causal, objetivo)

print(f"\n🔍 Analizando el nodo: '{objetivo}'")
print(f"  👨‍👦 Padres: {resultado['Padres']}")
print(f"  👶 Hijos: {resultado['Hijos']}")
print(f"  🤝 Copadres: {resultado['Copadres']}")
print(f"🛡️  MANTO DE MARKOV: {resultado['Manto_Total']}")
print("💡 Conclusión: Si conoces el estado de la Alarma y del Terremoto, puedes ignorar el resto de la red para calcular la probabilidad de Robo.")

# CASO 2: Queremos aislar el nodo 'Alarma'
objetivo = 'Alarma'
resultado = obtener_manto_markov(grafo_causal, objetivo)

print(f"\n🔍 Analizando el nodo: '{objetivo}'")
print(f"🛡️  MANTO DE MARKOV: {resultado['Manto_Total']}")
print("💡 Conclusión: Si conoces si hubo Robo, Terremoto y si llamaron Juan y María, las Noticias de Radio son irrelevantes para saber si la Alarma sonó.")