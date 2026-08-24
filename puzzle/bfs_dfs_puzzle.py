"""
Puzzle 3x3 - BFS y DFS

Basado en el notebook BFS_VS_DFS:
- El espacio vacío se representa con 0.
- BFS utiliza una cola.
- DFS utiliza una pila.
"""

from collections import deque

INICIO_PUZZLE = (1, 2, 3, 5, 0, 6, 4, 7, 8)
META_PUZZLE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def movimientos(estado):
    """Genera los estados que se obtienen con un movimiento válido."""
    resultado = []
    pos = estado.index(0)
    fila, col = pos // 3, pos % 3

    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nf, nc = fila + df, col + dc

        if 0 <= nf < 3 and 0 <= nc < 3:
            nueva = list(estado)
            nueva[pos], nueva[nf * 3 + nc] = (
                nueva[nf * 3 + nc],
                nueva[pos],
            )
            resultado.append(tuple(nueva))

    return resultado


def bfs(inicio=INICIO_PUZZLE, meta=META_PUZZLE):
    """Busca una solución utilizando BFS."""
    cola = deque([(inicio, [])])
    visitados = {inicio}
    nodos = 0

    while cola:
        estado, camino = cola.popleft()
        nodos += 1

        if estado == meta:
            return camino, nodos

        for nuevo in movimientos(estado):
            if nuevo not in visitados:
                visitados.add(nuevo)
                cola.append((nuevo, camino + [nuevo]))

    return None, nodos


def dfs(inicio=INICIO_PUZZLE, meta=META_PUZZLE):
    """Busca una solución utilizando DFS."""
    pila = [(inicio, [])]
    visitados = {inicio}
    nodos = 0

    while pila:
        estado, camino = pila.pop()
        nodos += 1

        if estado == meta:
            return camino, nodos

        for nuevo in movimientos(estado):
            if nuevo not in visitados:
                visitados.add(nuevo)
                pila.append((nuevo, camino + [nuevo]))

    return None, nodos


def resolver(algoritmo, inicio=INICIO_PUZZLE, meta=META_PUZZLE):
    """Ejecuta BFS o DFS."""
    algoritmo = algoritmo.upper()

    if algoritmo == "BFS":
        return bfs(inicio, meta)
    if algoritmo == "DFS":
        return dfs(inicio, meta)

    raise ValueError("El algoritmo debe ser BFS o DFS.")


if __name__ == "__main__":
    for algoritmo in ("BFS", "DFS"):
        solucion, nodos = resolver(algoritmo)
        print(f"\n{algoritmo}")
        print("Nodos:", nodos)
        print("Movimientos:", len(solucion) if solucion is not None else "Sin solución")
