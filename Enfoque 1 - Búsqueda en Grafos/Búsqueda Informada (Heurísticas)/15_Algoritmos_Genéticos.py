import random

# Nuestro "ADN" (Todos los caracteres que un individuo puede tener)
GENES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"

def crear_individuo(longitud):
    """Crea una cadena de texto aleatoria (Un individuo de la población inicial)"""
    individuo = ""
    for _ in range(longitud):
        individuo += random.choice(GENES)
    return individuo

def calcular_aptitud(individuo, objetivo):
    """
    Función Fitness (h(n)).
    Compara letra por letra. Si la letra y la posición coinciden, suma 1 punto.
    """
    aptitud = 0
    for i in range(len(objetivo)):
        if individuo[i] == objetivo[i]:
            aptitud += 1
    return aptitud

def algoritmo_genetico(objetivo, tamano_poblacion, tasa_mutacion, max_generaciones):
    """
    Simula la evolución natural para encontrar una cadena de texto objetivo.
    """
    print(f"--- Iniciando Evolución Genética ---")
    print(f"Meta: '{objetivo}' | Población: {tamano_poblacion} | Mutación: {tasa_mutacion*100}%\n")

    longitud = len(objetivo)
    
    # ==========================================
    # SECCIÓN 1: CREACIÓN DE LA POBLACIÓN INICIAL
    # ==========================================
    poblacion = []
    for _ in range(tamano_poblacion):
        poblacion.append(crear_individuo(longitud))

    # ==========================================
    # SECCIÓN 2: EL CICLO DE LA VIDA (Generaciones)
    # ==========================================
    for generacion in range(max_generaciones):

        # 1. Evaluar a toda la población
        poblacion_evaluada = []
        for individuo in poblacion:
            aptitud = calcular_aptitud(individuo, objetivo)
            # Guardamos una tupla: (Calificación, "Texto_del_individuo")
            poblacion_evaluada.append((aptitud, individuo))

        # 2. Ordenar a los individuos del mejor al peor (usamos .sort nativo)
        poblacion_evaluada.sort(reverse=True, key=lambda x: x[0])

        mejor_aptitud = poblacion_evaluada[0][0]
        mejor_individuo = poblacion_evaluada[0][1]

        # Imprimimos el mejor espécimen de esta generación
        print(f"[Generación {generacion}] Mejor: {mejor_individuo} | Aptitud: {mejor_aptitud}/{longitud}")

        # Prueba de Meta: Si el mejor individuo es perfecto, ganamos
        if mejor_aptitud == longitud:
            print(f"\n✅ ¡Evolución completada exitosamente en la generación {generacion}!")
            return mejor_individuo

        # ==========================================
        # SECCIÓN 3: SELECCIÓN Y CRUCE (Reproducción)
        # ==========================================
        nueva_generacion = []

        # ELITISMO: Para no perder progreso, los 2 mejores de la generación 
        # actual pasan a la siguiente generación intactos.
        nueva_generacion.append(poblacion_evaluada[0][1])
        nueva_generacion.append(poblacion_evaluada[1][1])

        # Llenamos el resto de la población creando "hijos"
        while len(nueva_generacion) < tamano_poblacion:
            
            # SELECCIÓN: Elegimos a dos padres al azar, pero SOLO de entre
            # la mejor mitad de la población (los fuertes sobreviven).
            mitad_fuerte = tamano_poblacion // 2
            padre1 = random.choice(poblacion_evaluada[:mitad_fuerte])[1]
            padre2 = random.choice(poblacion_evaluada[:mitad_fuerte])[1]

            # CRUCE: Partimos el ADN. Una mitad del padre 1, otra del padre 2.
            punto_corte = random.randint(1, longitud - 1)
            hijo = padre1[:punto_corte] + padre2[punto_corte:]

            # ==========================================
            # SECCIÓN 4: MUTACIÓN (La magia del caos)
            # ==========================================
            hijo_mutado = ""
            for letra in hijo:
                # Lanzamos un dado de probabilidad para cada letra del hijo
                dado = random.random()
                if dado < tasa_mutacion:
                    # ¡Mutación! Cambiamos esta letra por una completamente al azar
                    hijo_mutado += random.choice(GENES)
                else:
                    # Sin mutación, la letra se hereda normal
                    hijo_mutado += letra

            # Agregamos al hijo a la nueva población
            nueva_generacion.append(hijo_mutado)

        # La nueva generación reemplaza a los viejos
        poblacion = nueva_generacion

    print(f"\n❌ Se alcanzó el límite de {max_generaciones} generaciones.")
    return mejor_individuo

# ==========================================
# ZONA DE PRUEBAS
# ==========================================
# ¡Intenta cambiar la frase objetivo!
meta_deseada = "Inteligencia Artificial"

# Parámetros del ecosistema
individuos_por_generacion = 150
probabilidad_mutacion = 0.05 # 5% de probabilidad de que una letra mute
limite_generaciones = 2000

algoritmo_genetico(
    objetivo=meta_deseada, 
    tamano_poblacion=individuos_por_generacion, 
    tasa_mutacion=probabilidad_mutacion, 
    max_generaciones=limite_generaciones
)