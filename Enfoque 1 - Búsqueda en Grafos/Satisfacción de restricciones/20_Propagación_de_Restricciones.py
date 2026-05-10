def revisar_arco(estado_i, estado_j, dominios):
    """
    Revisa la relación (arco) entre el estado I y el estado J.
    Si el estado I tiene un color en su lista que SIEMPRE chocaría con TODAS 
    las opciones posibles del estado J, eliminamos ese color del estado I.
    """
    borrado = False
    
    # Revisamos cada color que el estado_i está considerando usar
    for color_i in dominios[estado_i][:]:
        
        # ¿Existe ALGÚN color en el estado_j que sea diferente a color_i?
        # Si la respuesta es No, entonces usar color_i es un suicidio.
        hay_opcion_segura = False
        for color_j in dominios[estado_j]:
            if color_i != color_j:
                hay_opcion_segura = True
                break
                
        # Si usar color_i nos asegura un choque con estado_j, lo borramos de las opciones
        if not hay_opcion_segura:
            dominios[estado_i].remove(color_i)
            borrado = True
            
    return borrado

def algoritmo_ac3(variables, dominios, fronteras):
    """
    TEMA 20: Algoritmo de Consistencia de Arco 3 (AC-3).
    Aplica una reacción en cadena para podar las opciones imposibles.
    """
    print("--- Iniciando Propagación de Restricciones (AC-3) ---\n")
    
    # 1. Crear una cola con TODOS los arcos (todas las fronteras del mapa)
    cola_arcos = []
    for estado in variables:
        for vecino in fronteras.get(estado, []):
            cola_arcos.append((estado, vecino))

    paso = 1
    # 2. El ciclo de reacción en cadena
    while len(cola_arcos) > 0:
        estado_i, estado_j = cola_arcos.pop(0)
        
        # Si logramos borrar una opción inútil del estado_i...
        if revisar_arco(estado_i, estado_j, dominios):
            print(f"[Paso {paso}] 🧹 Limpieza lógica: Se redujeron las opciones de '{estado_i}' por culpa de '{estado_j}'.")
            print(f"    -> Nuevas opciones de {estado_i}: {dominios[estado_i]}")
            paso += 1
            
            # Si a estado_i ya no le quedan opciones, el problema no tiene solución
            if len(dominios[estado_i]) == 0:
                print(f"🛑 ERROR FATAL: '{estado_i}' se quedó sin opciones. El mapa es imposible.")
                return False
                
            # LA REACCIÓN EN CADENA: 
            # Como le quitamos opciones a estado_i, tenemos que volver a revisar a TODOS 
            # sus vecinos (excepto a estado_j que es el que causó esto) para ver si esta 
            # nueva limitación les afecta a ellos también.
            for vecino_k in fronteras.get(estado_i, []):
                if vecino_k != estado_j:
                    cola_arcos.append((vecino_k, estado_i))

    print("\n✅ Propagación terminada. El tablero ha sido optimizado al máximo.")
    return True

# ==========================================
# ZONA DE PRUEBAS (El poder de la deducción)
# ==========================================

estados_mexico = ['Jalisco', 'Nayarit', 'Zacatecas']

# Fronteras (Grafo en forma de triángulo, todos conectan con todos)
fronteras = {
    'Jalisco': ['Nayarit', 'Zacatecas'],
    'Nayarit': ['Jalisco', 'Zacatecas'],
    'Zacatecas': ['Nayarit', 'Jalisco']
}

# Supongamos que por reglas previas del juego, Nayarit ya solo puede ser Rojo
# y Zacatecas solo puede ser Verde.
# Jalisco empieza pensando que puede ser los 3.
libreta_dominios = {
    'Jalisco': ['Rojo', 'Verde', 'Azul'],
    'Nayarit': ['Rojo'],
    'Zacatecas': ['Verde']
}

print(f"Libreta INICIAL de Jalisco: {libreta_dominios['Jalisco']}\n")

exito = algoritmo_ac3(estados_mexico, libreta_dominios, fronteras)

if exito:
    print(f"\nLibreta FINAL de Jalisco: {libreta_dominios['Jalisco']}")