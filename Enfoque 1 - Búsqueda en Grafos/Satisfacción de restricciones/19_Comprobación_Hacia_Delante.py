# ==========================================
# SECCIÓN 1: EL MOTOR DE VISIÓN A FUTURO
# ==========================================

def actualizar_dominios_futuros(estado_actual, color_asignado, dominios_actuales, fronteras):
    """
    TEMA 19: Comprobación Hacia Delante (Forward Checking).
    Crea un nuevo registro de dominios donde elimina el color que 
    acabamos de usar de las listas de opciones de todos sus vecinos.
    """
    # 1. Creamos una copia fresca de la libreta para no alterar el pasado si hacemos Backtracking
    nuevos_dominios = {estado: list(colores) for estado, colores in dominios_actuales.items()}
    
    vecinos = fronteras.get(estado_actual, [])
    
    # 2. Revisamos a cada vecino
    for vecino in vecinos:
        if vecino in nuevos_dominios: # Si el vecino aún no tiene color final
            
            # Si el color que usamos estaba en su lista de opciones, se lo quitamos
            if color_asignado in nuevos_dominios[vecino]:
                nuevos_dominios[vecino].remove(color_asignado)
                
                # 3. DETECCIÓN TEMPRANA DE FALLOS
                # ¡Peligro! Al quitarle este color, el vecino se quedó en cero opciones.
                if len(nuevos_dominios[vecino]) == 0:
                    return None # Devolvemos None como señal de alerta máxima
                    
    # Si ningún vecino se quedó en ceros, los nuevos dominios son seguros
    return nuevos_dominios

# ==========================================
# SECCIÓN 2: ALGORITMO BACKTRACKING + FORWARD CHECKING
# ==========================================

def resolver_csp_forward_checking(variables, fronteras, asignaciones, dominios_actuales):
    """
    Motor de resolución que aborta caminos condenados gracias a la visión a futuro.
    """
    # 1. Prueba de Meta: ¿Ya pintamos todos?
    if len(asignaciones) == len(variables):
        return asignaciones

    # 2. Seleccionamos el siguiente estado a pintar
    estados_sin_pintar = [v for v in variables if v not in asignaciones]
    estado_actual = estados_sin_pintar[0]

    print(f"\n[?] Analizando: {estado_actual}")
    print(f"    Opciones disponibles en su libreta: {dominios_actuales[estado_actual]}")

    # 3. Probar los colores que AÚN están permitidos en su dominio actual
    for color in dominios_actuales[estado_actual]:
        print(f"  -> Asignando '{color}' a {estado_actual}...")
        
        # Asignamos temporalmente
        asignaciones[estado_actual] = color

        # ==========================================
        # EJECUTAR LA COMPROBACIÓN HACIA DELANTE
        # ==========================================
        nuevos_dominios = actualizar_dominios_futuros(estado_actual, color, dominios_actuales, fronteras)

        if nuevos_dominios is not None:
            print(f"  [+] Seguro. Ningún vecino quedó acorralado.")
            
            # Llamada recursiva usando la NUEVA libreta de dominios más estrictos
            resultado = resolver_csp_forward_checking(variables, fronteras, asignaciones, nuevos_dominios)
            
            if resultado is not None:
                return resultado
        else:
            print(f"  [!] ALERTA FUTURA. Usar '{color}' condenaría a un vecino a quedarse sin colores.")

        # Si falló la recursión o saltó la alerta futura, hacemos Backtracking
        print(f"  [-] Retroceso (Backtracking). Borrando '{color}' de {estado_actual}")
        del asignaciones[estado_actual]

    return None

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# Variables
estados_mexico = ['Jalisco', 'Nayarit', 'Zacatecas', 'Aguascalientes', 'Guanajuato', 'Michoacan', 'Colima']

# Restricciones
fronteras = {
    'Jalisco': ['Nayarit', 'Zacatecas', 'Aguascalientes', 'Guanajuato', 'Michoacan', 'Colima'],
    'Nayarit': ['Jalisco', 'Zacatecas'],
    'Zacatecas': ['Nayarit', 'Jalisco', 'Aguascalientes'],
    'Aguascalientes': ['Zacatecas', 'Jalisco'],
    'Guanajuato': ['Jalisco', 'Michoacan'],
    'Michoacan': ['Jalisco', 'Guanajuato', 'Colima'],
    'Colima': ['Jalisco', 'Michoacan']
}

# 1. LA LIBRETA INICIAL (El estado en tiempo cero)
# Al principio, todos los estados tienen permitidos los 3 colores
colores_disponibles = ['Rojo', 'Verde', 'Azul']
libreta_dominios_inicial = {estado: list(colores_disponibles) for estado in estados_mexico}

print("--- Iniciando CSP con Comprobación Hacia Delante (Forward Checking) ---")

# Arrancamos con las asignaciones vacías {}
mapa_resuelto = resolver_csp_forward_checking(estados_mexico, fronteras, {}, libreta_dominios_inicial)

if mapa_resuelto:
    print("\n ¡MAPA COLOREADO EXITOSAMENTE!")
    for estado, color in mapa_resuelto.items():
        print(f" {estado}: {color}")