"""
Medición de BFS y DFS para Puzzle 3x3.
"""

import time

from bfs_dfs_puzzle import resolver


def medir_algoritmo(
    algoritmo,
    inicio,
    meta,
    max_nodos=50000,
):
    """
    Ejecuta BFS o DFS y mide:

    - Nodos explorados
    - Movimientos de la solución
    - Profundidad
    - Tiempo de ejecución

    max_nodos evita que una ejecución se prolongue demasiado.
    """

    inicio_tiempo = time.perf_counter()

    solucion, nodos = resolver(
        algoritmo,
        inicio,
        meta,
        max_nodos=max_nodos,
    )

    tiempo = time.perf_counter() - inicio_tiempo

    return {
        "algoritmo": algoritmo.upper(),
        "nodos": nodos,
        "movimientos": (
            len(solucion)
            if solucion is not None
            else None
        ),
        "profundidad": (
            len(solucion)
            if solucion is not None
            else None
        ),
        "tiempo": tiempo,
        "solucion": solucion,
    }


def comparar(
    inicio,
    meta,
    max_nodos=50000,
):
    """
    Compara BFS y DFS usando el mismo estado inicial.
    """

    return [
        medir_algoritmo(
            "BFS",
            inicio,
            meta,
            max_nodos,
        ),
        medir_algoritmo(
            "DFS",
            inicio,
            meta,
            max_nodos,
        ),
    ]


if __name__ == "__main__":

    from bfs_dfs_puzzle import (
        INICIO_PUZZLE,
        META_PUZZLE,
    )

    resultados = comparar(
        INICIO_PUZZLE,
        META_PUZZLE,
    )

    for resultado in resultados:
        print(resultado)
