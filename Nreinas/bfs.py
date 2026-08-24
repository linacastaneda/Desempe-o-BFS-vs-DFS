from collections import deque
from n_reinas import es_valida, es_solucion_completa


def resolver_bfs(n):
    """
    Resuelve el problema de N-Reinas utilizando búsqueda en anchura (BFS).

    Parámetros:
        n: tamaño del tablero (n x n) y número de reinas.

    Retorna:
        tupla: (solucion, nodos_explorados)
        - solucion: lista con la posición de las reinas o None si no hay solución.
        - nodos_explorados: cantidad de estados procesados durante la búsqueda.
    """
    cola = deque()
    cola.append(([], 0))
    nodos_explorados = 0

    while cola:
        tablero_parcial, columna = cola.popleft()
        nodos_explorados += 1

        if es_solucion_completa(tablero_parcial, n):
            return tablero_parcial, nodos_explorados

        if columna >= n:
            continue

        for fila in range(n):
            if es_valida(tablero_parcial, fila, columna):
                nuevo_tablero = tablero_parcial + [fila]
                cola.append((nuevo_tablero, columna + 1))

    return None, nodos_explorados


def resolver_bfs_todas(n):
    """
    Resuelve el problema de N-Reinas utilizando BFS y encuentra TODAS las soluciones.

    Parámetros:
        n: tamaño del tablero (n x n) y número de reinas.

    Retorna:
        tupla: (soluciones, nodos_explorados)
        - soluciones: lista de todas las soluciones encontradas.
        - nodos_explorados: cantidad de estados procesados durante la búsqueda.
    """
    cola = deque()
    cola.append(([], 0))
    nodos_explorados = 0
    soluciones = []

    while cola:
        tablero_parcial, columna = cola.popleft()
        nodos_explorados += 1

        if es_solucion_completa(tablero_parcial, n):
            soluciones.append(tablero_parcial)
            continue

        if columna >= n:
            continue

        for fila in range(n):
            if es_valida(tablero_parcial, fila, columna):
                nuevo_tablero = tablero_parcial + [fila]
                cola.append((nuevo_tablero, columna + 1))

    return soluciones, nodos_explorados


if __name__ == "__main__":
    n = 8
    solucion, nodos = resolver_bfs(n)
    print(f"BFS - {n} Reinas")
    print(f"Solución: {solucion}")
    print(f"Nodos explorados: {nodos}")