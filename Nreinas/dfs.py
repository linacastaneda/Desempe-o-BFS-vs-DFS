from n_reinas import es_valida, es_solucion_completa


def resolver_dfs(n):
    """
    Resuelve el problema de N-Reinas utilizando búsqueda en profundidad (DFS).

    Parámetros:
        n: tamaño del tablero (n x n) y número de reinas.

    Retorna:
        tupla: (solucion, nodos_explorados)
        - solucion: lista con la posición de las reinas o None si no hay solución.
        - nodos_explorados: cantidad de estados procesados durante la búsqueda.
    """
    pila = []
    pila.append(([], 0))
    nodos_explorados = 0

    while pila:
        tablero_parcial, columna = pila.pop()
        nodos_explorados += 1

        if es_solucion_completa(tablero_parcial, n):
            return tablero_parcial, nodos_explorados

        if columna >= n:
            continue

        for fila in range(n - 1, -1, -1):
            if es_valida(tablero_parcial, fila, columna):
                nuevo_tablero = tablero_parcial + [fila]
                pila.append((nuevo_tablero, columna + 1))

    return None, nodos_explorados


def resolver_dfs_todas(n):
    """
    Resuelve el problema de N-Reinas utilizando DFS y encuentra TODAS las soluciones.

    Parámetros:
        n: tamaño del tablero (n x n) y número de reinas.

    Retorna:
        tupla: (soluciones, nodos_explorados)
        - soluciones: lista de todas las soluciones encontradas.
        - nodos_explorados: cantidad de estados procesados durante la búsqueda.
    """
    pila = []
    pila.append(([], 0))
    nodos_explorados = 0
    soluciones = []

    while pila:
        tablero_parcial, columna = pila.pop()
        nodos_explorados += 1

        if es_solucion_completa(tablero_parcial, n):
            soluciones.append(tablero_parcial)
            continue

        if columna >= n:
            continue

        for fila in range(n - 1, -1, -1):
            if es_valida(tablero_parcial, fila, columna):
                nuevo_tablero = tablero_parcial + [fila]
                pila.append((nuevo_tablero, columna + 1))

    return soluciones, nodos_explorados


if __name__ == "__main__":
    n = 8
    solucion, nodos = resolver_dfs(n)
    print(f"DFS - {n} Reinas")
    print(f"Solución: {solucion}")
    print(f"Nodos explorados: {nodos}")