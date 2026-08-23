import time
import tracemalloc

from bfs_dfs_mochila import bfs_mochila, dfs_mochila


def medir_algoritmo(
    algoritmo,
    pesos,
    valores,
    capacidad
):
    """
    Ejecuta un algoritmo de búsqueda y mide:

    - Tiempo de ejecución.
    - Memoria pico consumida.

    Retorna los resultados del algoritmo
    junto con las métricas obtenidas.
    """

    # Inicia el seguimiento de memoria.
    tracemalloc.start()

    # Se registra el instante inicial.
    inicio = time.perf_counter()

    resultado = algoritmo(
        pesos,
        valores,
        capacidad
    )

    # Se registra el instante final.
    fin = time.perf_counter()

    # Obtiene la memoria actual y la memoria máxima
    # utilizada durante la ejecución.
    memoria_actual, memoria_pico = (
        tracemalloc.get_traced_memory()
    )

    tracemalloc.stop()

    tiempo_ejecucion = fin - inicio

    # La memoria entregada por tracemalloc está en bytes.
    # Se convierte a kilobytes.
    memoria_pico_kb = memoria_pico / 1024

    mejor_valor, seleccionados, nodos_explorados = resultado

    return {
        "valor": mejor_valor,
        "seleccionados": seleccionados,
        "nodos": nodos_explorados,
        "tiempo": tiempo_ejecucion,
        "memoria_kb": memoria_pico_kb
    }


if __name__ == "__main__":

    pesos = [2, 3, 4, 5]
    valores = [3, 4, 5, 8]
    capacidad = 8

    resultado_bfs = medir_algoritmo(
        bfs_mochila,
        pesos,
        valores,
        capacidad
    )

    resultado_dfs = medir_algoritmo(
        dfs_mochila,
        pesos,
        valores,
        capacidad
    )

    print()
    print("RESULTADOS BFS")
    print("Valor óptimo:", resultado_bfs["valor"])
    print(
        "Tiempo:",
        resultado_bfs["tiempo"],
        "segundos"
    )
    print(
        "Memoria pico:",
        resultado_bfs["memoria_kb"],
        "KB"
    )
    print(
        "Nodos explorados:",
        resultado_bfs["nodos"]
    )

    print()
    print("RESULTADOS DFS")
    print("Valor óptimo:", resultado_dfs["valor"])
    print(
        "Tiempo:",
        resultado_dfs["tiempo"],
        "segundos"
    )
    print(
        "Memoria pico:",
        resultado_dfs["memoria_kb"],
        "KB"
    )
    print(
        "Nodos explorados:",
        resultado_dfs["nodos"]
    )