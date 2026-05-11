def encontrar_equilibrio_nash(acciones_j1, acciones_j2, matriz_pagos):
    """
    TEMA 32 (Parte 1): Buscador de Equilibrios de Nash.
    Un equilibrio de Nash ocurre cuando la acción de J1 es la mejor respuesta 
    contra la de J2, Y la acción de J2 es la mejor respuesta contra la de J1.
    """
    print("--- Analizando Matriz de Pagos ---")
    equilibrios = []

    for a1 in acciones_j1:
        for a2 in acciones_j2:
            pago_j1, pago_j2 = matriz_pagos[a1][a2]
            
            # 1. ¿Es 'a1' la mejor respuesta de J1 dado que J2 jugó 'a2'?
            es_mejor_j1 = True
            for alternativa_a1 in acciones_j1:
                pago_alternativo_j1, _ = matriz_pagos[alternativa_a1][a2]
                if pago_alternativo_j1 > pago_j1:
                    es_mejor_j1 = False
                    break
                    
            # 2. ¿Es 'a2' la mejor respuesta de J2 dado que J1 jugó 'a1'?
            es_mejor_j2 = True
            for alternativa_a2 in acciones_j2:
                _, pago_alternativo_j2 = matriz_pagos[a1][alternativa_a2]
                if pago_alternativo_j2 > pago_j2:
                    es_mejor_j2 = False
                    break
                    
            # Si nadie se arrepiente de su decisión... ¡Es un Equilibrio de Nash!
            if es_mejor_j1 and es_mejor_j2:
                equilibrios.append((a1, a2))
                
    return equilibrios

# ==========================================
# ZONA DE PRUEBAS (El Dilema del Prisionero)
# ==========================================

# Acciones posibles para los Jugadores 1 y 2
opciones = ["Callar", "Delatar"]

# matriz_pagos[Accion_J1][Accion_J2] = (Utilidad_J1, Utilidad_J2)
# Nota: Como es cárcel, los años son utilidades NEGATIVAS (menos es mejor)
pagos_prisionero = {
    "Callar": {
        "Callar":  (-1, -1),   # Ambos callan: 1 año cada uno
        "Delatar": (-10, 0)    # J1 calla, J2 delata: J1 recibe 10 años, J2 sale libre
    },
    "Delatar": {
        "Callar":  (0, -10),   # J1 delata, J2 calla: J1 sale libre, J2 recibe 10 años
        "Delatar": (-5, -5)    # Ambos delatan: 5 años cada uno
    }
}

nash = encontrar_equilibrio_nash(opciones, opciones, pagos_prisionero)

print("\n⚖️ Equilibrios de Nash encontrados:")
for eq in nash:
    print(f"  -> Jugador 1: '{eq[0]}' | Jugador 2: '{eq[1]}'")