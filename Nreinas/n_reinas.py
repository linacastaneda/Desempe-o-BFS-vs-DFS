def es_valida(tablero, fila, columna):
    """
    Verifica si se puede colocar una reina en (fila, columna)
    sin que sea atacada por las reinas ya colocadas.

    Parámetros:
        tablero: lista donde tablero[c] = fila de la reina en columna c.
        fila: fila candidata para la nueva reina.
        columna: columna donde se intenta colocar la reina.

    Retorna:
        True si la posición es válida, False en caso contrario.
    """
    for c in range(columna):
        f = tablero[c]
        if f == fila:
            return False
        if abs(f - fila) == abs(c - columna):
            return False
    return True


def tablero_a_matriz(tablero):
    """
    Convierte la representación compacta del tablero
    a una matriz visual para mostrar.

    Parámetros:
        tablero: lista donde tablero[c] = fila de la reina en columna c.

    Retorna:
        Matriz n x n con 1 donde hay reina y 0 en casillas vacías.
    """
    n = len(tablero)
    matriz = [[0] * n for _ in range(n)]
    for c, f in enumerate(tablero):
        matriz[f][c] = 1
    return matriz


def es_solucion_completa(tablero, n):
    """
    Verifica si el tablero tiene n reinas colocadas válidamente.
    """
    return len(tablero) == n