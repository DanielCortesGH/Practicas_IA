def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print("-" * 15)

def es_seguro(tablero, fila, col, N):
    """
    Verifica las restricciones: Revisa si poner una reina aquí rompe las reglas.
    Como vamos llenando de arriba hacia abajo, solo necesitamos revisar hacia arriba.
    """
    # Revisar la columna hacia arriba
    for i in range(fila):
        if tablero[i][col] == 'Q': return False
        
    # Revisar la diagonal superior izquierda
    for i, j in zip(range(fila - 1, -1, -1), range(col - 1, -1, -1)):
        if tablero[i][j] == 'Q': return False
        
    # Revisar la diagonal superior derecha
    for i, j in zip(range(fila - 1, -1, -1), range(col + 1, N)):
        if tablero[i][j] == 'Q': return False
        
    return True

def resolver_n_reinas_backtracking(tablero, fila, N):
    """
    TEMA 18: Algoritmo de Búsqueda de Vuelta Atrás (Backtracking).
    Intenta colocar una reina por fila de manera recursiva.
    """
    # 1. PRUEBA DE META: Si ya pasamos la última fila, colocamos todas las reinas
    if fila >= N:
        return True

    # 2. INTENTAR VALORES: Probamos cada columna en esta fila
    for col in range(N):
        print(f"[?] Probando Fila {fila}, Columna {col}...")
        
        if es_seguro(tablero, fila, col, N):
            # Asignamos temporalmente el valor (colocamos la reina)
            tablero[fila][col] = 'Q'
            print(f"  [+] Reina colocada en ({fila}, {col})")
            
            # Llamada recursiva para tratar de colocar la reina en la SIGUIENTE fila
            if resolver_n_reinas_backtracking(tablero, fila + 1, N):
                return True

            # ==========================================
            # BACKTRACKING (LA VUELTA ATRÁS)
            # ==========================================
            # Si el código llega a esta línea, la llamada recursiva de abajo falló.
            # ¡Tenemos que borrar nuestra reina y probar la siguiente columna!
            print(f"  [-] ERROR FUTURO. Haciendo Backtracking en ({fila}, {col})")
            tablero[fila][col] = '.' # Borramos la reina
            
        else:
            print(f"  [x] Posición bajo ataque.")

    # Si revisamos todas las columnas y ninguna funcionó, retrocedemos a la fila anterior
    return False

# ==========================================
# ZONA DE PRUEBAS (Tablero 4x4)
# ==========================================
N = 4
# Creamos un tablero vacío lleno de puntos '.'
tablero_ajedrez = [['.' for _ in range(N)] for _ in range(N)]

print(f"--- Iniciando Búsqueda de Vuelta Atrás ({N} Reinas) ---\n")

if resolver_n_reinas_backtracking(tablero_ajedrez, 0, N):
    print("\n ¡SOLUCIÓN ENCONTRADA!")
    imprimir_tablero(tablero_ajedrez)
else:
    print("\n No existe solución para este tablero.")