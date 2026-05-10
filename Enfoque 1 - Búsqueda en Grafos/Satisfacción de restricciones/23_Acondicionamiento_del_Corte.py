def es_color_valido(estado, color_propuesto, asignaciones_actuales, fronteras):
    """Verifica que el color no choque con los vecinos ya pintados."""
    for vecino in fronteras.get(estado, []):
        if vecino in asignaciones_actuales and asignaciones_actuales[vecino] == color_propuesto:
            return False
    return True

def resolver_arbol_sin_ciclos(variables_arbol, dominios, fronteras, asignaciones):
    """
    Subrutina rápida. 
    Asume que las variables restantes ya NO forman ciclos (son un árbol lógico).
    Si es un árbol, una simple pasada lineal suele ser suficiente.
    """
    for estado in variables_arbol:
        pintado = False
        for color in dominios:
            if es_color_valido(estado, color, asignaciones, fronteras):
                asignaciones[estado] = color
                pintado = True
                break # Pasamos al siguiente nodo del árbol sin mirar atrás
                
        if not pintado:
            # Si un nodo de un árbol puro se queda sin colores, el color raíz era malo
            return False 
            
    return True

def acondicionamiento_de_corte(variables, dominios, fronteras, nodo_corte):
    """
    TEMA 23: Acondicionamiento del Corte.
    Fija un nodo estratégico para destruir los ciclos y resolver el resto como un árbol.
    """
    print(f"--- Iniciando Acondicionamiento de Corte ---")
    print(f" Nodo seleccionado como Corte (Cutset): '{nodo_corte}'\n")
    
    # Separamos el grafo: El nodo de corte vs el resto del "árbol"
    variables_arbol = [v for v in variables if v != nodo_corte]
    
    # 1. Probamos colores SOLO para el nodo de corte
    for color_raiz in dominios:
        print(f"[?] Condicionando el corte: Asignando '{color_raiz}' a {nodo_corte}...")
        
        asignaciones = {nodo_corte: color_raiz}
        
        # 2. Al fijar el corte, el resto del grafo se vuelve un árbol simple.
        # Intentamos resolverlo linealmente.
        exito_arbol = resolver_arbol_sin_ciclos(variables_arbol, dominios, fronteras, asignaciones)
        
        if exito_arbol:
            print(f"  [+] ÉXITO. El árbol restante se resolvió fácilmente.")
            return asignaciones
        else:
            print(f"  [-] FALLO. El color '{color_raiz}' en el corte colapsó el árbol. Intentando otro...")
            
    return None

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Nuestro pequeño mapa con un ciclo
estados = ['Jalisco', 'Nayarit', 'Zacatecas', 'Aguascalientes']
colores = ['Rojo', 'Verde', 'Azul']

# Jalisco, Nayarit y Zacatecas forman un triángulo (Un ciclo).
# Aguascalientes solo conecta a Zacatecas (Es una rama de árbol).
fronteras_ciclo = {
    'Jalisco': ['Nayarit', 'Zacatecas'],
    'Nayarit': ['Jalisco', 'Zacatecas'],
    'Zacatecas': ['Jalisco', 'Nayarit', 'Aguascalientes'],
    'Aguascalientes': ['Zacatecas']
}

# Al aislar a 'Jalisco', el ciclo se rompe. 
# La estructura restante queda: Nayarit <-> Zacatecas <-> Aguascalientes (¡Un árbol perfecto lineal!)
nodo_estrategico = 'Jalisco'

solucion = acondicionamiento_de_corte(estados, colores, fronteras_ciclo, nodo_estrategico)

if solucion:
    print("\n✅ ¡MAPA RESUELTO MEDIANTE CORTE!")
    for estado, color in solucion.items():
        print(f" {estado}: {color}")