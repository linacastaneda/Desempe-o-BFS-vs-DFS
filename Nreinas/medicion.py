import time
import tracemalloc
from bfs import resolver_bfs
from dfs import resolver_dfs


def medir_algoritmo(algoritmo, n):
    """
    Ejecuta un algoritmo de búsqueda y mide:
    - Tiempo de ejecución.
    - Memoria pico consumida.
    - Nodos explorados.

    Parámetros:
        algoritmo: función a medir (resolver_bfs o resolver_dfs).
        n: tamaño del tablero.

    Retorna:
        dict con las métricas: solucion, nodos, tiempo, memoria_kb
    """
    tracemalloc.start()
    inicio = time.perf_counter()

    solucion, nodos = algoritmo(n)

    fin = time.perf_counter()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tiempo_ejecucion = fin - inicio
    memoria_pico_kb = memoria_pico / 1024

    return {
        "solucion": solucion,
        "nodos": nodos,
        "tiempo": tiempo_ejecucion,
        "memoria_kb": memoria_pico_kb
    }


if __name__ == "__main__":
    n = 8

    print(f"Midiendo algoritmos para {n} reinas...\n")

    resultado_bfs = medir_algoritmo(resolver_bfs, n)
    resultado_dfs = medir_algoritmo(resolver_dfs, n)

    print("RESULTADOS BFS")
    print(f"  Solución: {resultado_bfs['solucion']}")
    print(f"  Tiempo: {resultado_bfs['tiempo']:.6f} segundos")
    print(f"  Memoria pico: {resultado_bfs['memoria_kb']:.2f} KB")
    print(f"  Nodos explorados: {resultado_bfs['nodos']}")

    print()

    print("RESULTADOS DFS")
    print(f"  Solución: {resultado_dfs['solucion']}")
    print(f"  Tiempo: {resultado_dfs['tiempo']:.6f} segundos")
    print(f"  Memoria pico: {resultado_dfs['memoria_kb']:.2f} KB")
    print(f"  Nodos explorados: {resultado_dfs['nodos']}")