# ==========================================
# 1. LOS MODELOS ESTADÍSTICOS (El Cerebro del Asistente Virtual)
# ==========================================

# MODELO ACÚSTICO: P(Audio | Fonema)
# ¿Qué tan probable es que el micrófono escuche este 'Audio' si yo quise decir 'Fonema'?
modelo_acustico = {
    '/o/': {'O': 0.8, 'L': 0.1, 'I': 0.0, 'A': 0.1},
    '/l/': {'O': 0.1, 'L': 0.8, 'I': 0.0, 'A': 0.1},
    '/i/': {'O': 0.0, 'L': 0.1, 'I': 0.8, 'A': 0.1},
    '/a/': {'O': 0.1, 'L': 0.0, 'I': 0.1, 'A': 0.8},
}

# MODELO DE PRONUNCIACIÓN: Diccionario
# Mapeo de palabras a sus secuencias de fonemas exactas
diccionario = {
    'hola': ['/o/', '/l/', '/a/'], # Ignoramos la H muda
    'ola':  ['/o/', '/l/', '/a/'],
    'ia':   ['/i/', '/a/'],
    'dia':  ['/d/', '/i/', '/a/'] # Asumimos que la /d/ acústica falló
}

# MODELO DE LENGUAJE (Cadena de Markov / Bigramas)
# P(Palabra_Actual | Palabra_Anterior)
modelo_lenguaje = {
    'hola': {'ia': 0.60, 'dia': 0.05}, # "Hola IA" es muy probable
    'ola':  {'ia': 0.01, 'dia': 0.20}, # "Ola dia" no tiene mucho sentido gramatical
}

prob_inicial_palabra = {'hola': 0.5, 'ola': 0.5}

# ==========================================
# 2. EL MOTOR DE RECONOCIMIENTO (Viterbi Simplificado a nivel frase)
# ==========================================
def reconocer_voz(secuencia_audio, candidato_1, candidato_2):
    """
    Evalúa matemáticamente dos frases candidatas usando 
    el Teorema de Bayes: P(Frase) * P(Audio | Frase)
    """
    print(f"--- Decodificando Audio Acústico ---")
    print(f"🎤 Secuencia capturada: {secuencia_audio}")
    
    resultados = {}
    
    for frase in [candidato_1, candidato_2]:
        palabras = frase.split()
        prob_frase_total = 1.0
        
        # 1. EVALUAR EL MODELO DE LENGUAJE (P_Frase)
        prob_lenguaje = prob_inicial_palabra[palabras[0]]
        if len(palabras) > 1:
            prob_lenguaje *= modelo_lenguaje[palabras[0]][palabras[1]]
            
        print(f"\nAnalizando candidato: '{frase}'")
        print(f"  -> P(Lenguaje/Gramática): {prob_lenguaje:.4f}")
        
        # 2. EVALUAR EL MODELO ACÚSTICO + PRONUNCIACIÓN (P_Audio | Frase)
        prob_acustica = 1.0
        fonemas_esperados = []
        for p in palabras:
            fonemas_esperados.extend(diccionario[p]) # Concatenamos los fonemas de ambas palabras
            
        # Alineación temporal (Asumimos 1 sonido = 1 fonema para simplificar)
        if len(fonemas_esperados) == len(secuencia_audio):
            for t in range(len(secuencia_audio)):
                sonido = secuencia_audio[t]
                fonema = fonemas_esperados[t]
                
                if fonema in modelo_acustico:
                    prob_acustica *= modelo_acustico[fonema][sonido]
                else:
                    prob_acustica *= 0.01 # Penalización severa si falta el fonema (ej. la /d/)
        else:
            prob_acustica = 0.0 # Las longitudes no coinciden
            
        print(f"  -> P(Acústica/Onda): {prob_acustica:.4f}")
        
        # 3. RESULTADO FINAL (Teorema de Bayes sin normalizar)
        score_final = prob_lenguaje * prob_acustica
        resultados[frase] = score_final
        print(f"  🏆 Score Combinado: {score_final:.6f}")
        
    mejor_frase = max(resultados, key=resultados.get)
    return mejor_frase

# ==========================================
# ZONA DE PRUEBAS
# ==========================================

# El micrófono escupe este array (que parece que dice "O-L-I-A")
audio_crudo = ['O', 'L', 'I', 'A']

frase_ganadora = reconocer_voz(audio_crudo, "hola ia", "ola dia")

print("-" * 50)
print(f"✅ EL ASISTENTE DE VOZ ENTENDIÓ: '{frase_ganadora.upper()}'")