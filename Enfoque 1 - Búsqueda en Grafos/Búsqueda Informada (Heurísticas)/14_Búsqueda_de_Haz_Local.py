def busqueda_haz_local(grafo, altitudes, puntos_inicio, k_haces, max_iteraciones):
    """
    Algoritmo de Haz Local (Local Beam Search).
    Mantiene 'k' estados paralelos. En cada paso, genera TODOS los vecinos 
    de los 'k' estados, y selecciona a los 'k' mejores de toda esa piscina de opciones.
    """
    print(f"--- Iniciando Haz Local (Escuadrón de {k_haces} exploradores) ---\n")
    print(f"Puntos de despliegue inicial: {puntos_inicio}\n")
    
    # ==========================================
    # SECCIÓN 1: INICIALIZACIÓN
    # ==========================================
    # Nuestra lista de posiciones actuales del escuadrón
    estados_actuales = list(puntos_inicio)
    
    # Llevamos un registro del punto más alto visto por cualquier explorador
    mejor_global = estados_actuales[0]
    
    # ==========================================
    # SECCIÓN 2: CICLO DE EXPLORACIÓN CONJUNTA
    # ==========================================
    for iteracion in range(max_iteraciones):
        print(f"[Turno {iteracion}] Posiciones del escuadrón: {estados_actuales}")
        
        # 1. Agrupar todos los vecinos descubiertos por todo el equipo
        todos_los_vecinos_descubiertos = []
        for estado in estados_actuales:
            vecinos = grafo.get(estado, [])
            for vecino in vecinos:
                # Evitamos duplicados en nuestra lista compartida
                if vecino not in todos_los_vecinos_descubiertos:
                    todos_los_vecinos_descubiertos.append(vecino)
                    
        if not todos_los_vecinos_descubiertos:
            print(" Ningún explorador encontró nuevos caminos. Fin de la misión.")
            break

        # ==========================================
        # SECCIÓN 3: SELECCIÓN DE LAS MEJORES 'k' POSICIONES
        # ==========================================
        siguientes_estados = []
        candidatos = list(todos_los_vecinos_descubiertos)
        
        # Extraemos manualmente los 'k' mejores candidatos
        for _ in range(k_haces):
            # Si ya no hay más candidatos que revisar, rompemos el ciclo
            if not candidatos:
                break
                
            # Búsqueda manual del nodo más alto
            mejor_candidato = candidatos[0]
            mejor_altitud = altitudes[mejor_candidato]
            
            for c in candidatos[1:]:
                if altitudes[c] > mejor_altitud:
                    mejor_altitud = altitudes[c]
                    mejor_candidato = c
            
            # Reasignamos a un explorador a este excelente lugar
            siguientes_estados.append(mejor_candidato)
            # Quitamos este lugar de la lista para buscar el segundo mejor, tercer mejor, etc.
            candidatos.remove(mejor_candidato)
            
            # Verificamos si este lugar rompió el récord mundial
            if mejor_altitud > altitudes[mejor_global]:
                mejor_global = mejor_candidato
                print(f"     ¡Alerta en la radio! Nuevo récord global en '{mejor_global}' (Alt: {mejor_altitud})")

        # Actualizamos las posiciones del escuadrón para el siguiente turno
        estados_actuales = siguientes_estados

    return mejor_global, altitudes[mejor_global]

# ==========================================
# ZONA DE PRUEBAS (El poder del trabajo en equipo)
# ==========================================

# Grafo estratégico:
# - La rama izquierda (A1 -> A2 -> A3) es una colina pequeña.
# - La rama derecha (B1 -> B2 -> B3) es el Monte Everest.
grafo_montañas = {
    'Inicio_Malo': ['A1'],
    'A1': ['A2', 'C1'], # C1 es un puente secreto entre las montañas
    'A2': ['A3'],
    'A3': [], # Cima falsa (Altura 50)
    
    'Inicio_Bueno': ['B1'],
    'B1': ['B2'],
    'C1': ['B2'], # El puente conecta con la montaña gigante
    'B2': ['B3'],
    'B3': [] # Cima real (Altura 100)
}

altitudes_terreno = {
    'Inicio_Malo': 10, 'A1': 20, 'A2': 40, 'A3': 50,
    'C1': 30, # Puente de altura media
    'Inicio_Bueno': 15, 'B1': 25, 'B2': 70, 'B3': 100
}

# Desplegamos a 2 exploradores (k=2).
# Uno cae en un lugar pésimo, el otro en un lugar decente.
despliegue_inicial = ['Inicio_Malo', 'Inicio_Bueno']
tamaño_escuadron = 2
turnos = 5

mejor_nodo, mejor_altitud = busqueda_haz_local(
    grafo_montañas, 
    altitudes_terreno, 
    despliegue_inicial, 
    tamaño_escuadron, 
    turnos
)

print(f"\n Operación finalizada. El punto más alto conquistado fue '{mejor_nodo}' con altura de {mejor_altitud}.")