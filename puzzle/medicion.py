"""
Medición de BFS y DFS para Puzzle 3x3.

Se mide:

- Tiempo de ejecución.
- Memoria pico utilizada.
- Nodos explorados.
- Cantidad de movimientos.
- Profundidad de la solución.
"""

import time
import tracemalloc

from bfs_dfs_puzzle import resolver


def medir_algoritmo(
    algoritmo,
    inicio,
    meta,
    max_nodos=50000,
):
    """
    Ejecuta BFS o DFS sobre una instancia del Puzzle 3x3
    y obtiene métricas de desempeño.

    Parámetros:
        algoritmo:
            Nombre del algoritmo: "BFS" o "DFS".

        inicio:
            Estado inicial del puzzle.

        meta:
            Estado objetivo.

        max_nodos:
            Cantidad máxima de nodos que puede explorar
            el algoritmo antes de detenerse.

    Retorna:
        Diccionario con:
            - algoritmo
            - nodos
            - movimientos
            - profundidad
            - tiempo
            - memoria_kb
            - solucion
    """

    # Inicia el seguimiento de memoria.
    tracemalloc.start()

    # Se registra el instante antes
    # de ejecutar el algoritmo.
    inicio_tiempo = time.perf_counter()

    solucion, nodos = resolver(
        algoritmo,
        inicio,
        meta,
        max_nodos=max_nodos,
    )

    # Calcula el tiempo total de ejecución.
    tiempo = time.perf_counter() - inicio_tiempo

    # Obtiene la memoria actual y el pico máximo
    # alcanzado durante la búsqueda.
    memoria_actual, memoria_pico = (
        tracemalloc.get_traced_memory()
    )

    # Detiene la medición de memoria.
    tracemalloc.stop()

    # Convierte bytes a kilobytes.
    memoria_pico_kb = memoria_pico / 1024

    # Si existe solución, la cantidad de movimientos
    # corresponde a la longitud de la ruta encontrada.
    movimientos_solucion = (
        len(solucion)
        if solucion is not None
        else None
    )

    return {
        "algoritmo": algoritmo.upper(),
        "nodos": nodos,
        "movimientos": movimientos_solucion,
        "profundidad": movimientos_solucion,
        "tiempo": tiempo,
        "memoria_kb": memoria_pico_kb,
        "solucion": solucion,
    }


def comparar(
    inicio,
    meta,
    max_nodos=50000,
):
    """
    Ejecuta BFS y DFS utilizando exactamente
    el mismo estado inicial y la misma meta.

    Esto permite comparar ambos algoritmos
    bajo las mismas condiciones.
    """

    resultado_bfs = medir_algoritmo(
        "BFS",
        inicio,
        meta,
        max_nodos,
    )

    resultado_dfs = medir_algoritmo(
        "DFS",
        inicio,
        meta,
        max_nodos,
    )

    return [
        resultado_bfs,
        resultado_dfs,
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

        print()

        print(
            "Algoritmo:",
            resultado["algoritmo"]
        )

        print(
            "Nodos explorados:",
            resultado["nodos"]
        )

        print(
            "Movimientos:",
            resultado["movimientos"]
        )

        print(
            "Profundidad:",
            resultado["profundidad"]
        )

        print(
            "Tiempo:",
            resultado["tiempo"],
            "segundos"
        )

        print(
            "Memoria pico:",
            resultado["memoria_kb"],
            "KB"
        )