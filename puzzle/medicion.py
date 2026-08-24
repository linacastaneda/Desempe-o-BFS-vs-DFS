"""
Medición de BFS y DFS para Puzzle 3x3.

Métricas utilizadas en el notebook:
- Tiempo de ejecución.
- Nodos explorados.
- Profundidad de la solución.
"""

import time

from bfs_dfs_puzzle import resolver


def medir_algoritmo(algoritmo, inicio, meta):
    """Ejecuta un algoritmo y devuelve sus métricas."""
    inicio_tiempo = time.perf_counter()
    solucion, nodos = resolver(algoritmo, inicio, meta)
    tiempo = time.perf_counter() - inicio_tiempo

    return {
        "algoritmo": algoritmo.upper(),
        "nodos": nodos,
        "movimientos": len(solucion) if solucion is not None else None,
        "profundidad": len(solucion) if solucion is not None else None,
        "tiempo": tiempo,
        "solucion": solucion,
    }


def comparar(inicio, meta):
    """Compara BFS y DFS para el mismo Puzzle."""
    return [
        medir_algoritmo("BFS", inicio, meta),
        medir_algoritmo("DFS", inicio, meta),
    ]


if __name__ == "__main__":
    from bfs_dfs_puzzle import INICIO_PUZZLE, META_PUZZLE

    for resultado in comparar(INICIO_PUZZLE, META_PUZZLE):
        print(resultado)
