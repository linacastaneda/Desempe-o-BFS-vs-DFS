import csv
import json
from pathlib import Path

from medicion import medir_algoritmo
from bfs import resolver_bfs
from dfs import resolver_dfs
from graficas import obtener_info_maquina


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_DATOS = RAIZ_PROYECTO / "resultados" / "nreinas" / "datos"

# Valores de N evaluados.
N_VALORES = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# Para N grandes se reduce el número de repeticiones porque
# el costo de BFS crece de forma muy pronunciada.
SIMULACIONES_POR_N = {
    4: 100,
    5: 100,
    6: 100,
    7: 100,
    8: 100,
    9: 100,
    10: 100,
    11: 50,
    12: 20,
    13: 10,
}


def obtener_simulaciones(n):
    """Retorna la cantidad de repeticiones definida para un valor de N."""
    return SIMULACIONES_POR_N.get(n, 100)


def ejecutar_simulaciones():
    """
    Ejecuta el experimento de N-Reinas para N entre 4 y 13.

    Para N de 4 a 10 se realizan 100 repeticiones por algoritmo.
    Para N=11 se realizan 50, para N=12 se realizan 20 y para
    N=13 se realizan 10, debido al elevado costo experimental de BFS.

    En cada repetición BFS y DFS resuelven exactamente el mismo
    problema de tamaño N y ambos buscan la primera solución completa.

    Retorna:
        resultados:
            Lista de diccionarios con las métricas de cada ejecución.

        info_maquina:
            Información del hardware y software del equipo utilizado.
    """

    info_maquina = obtener_info_maquina()

    print("\n=== Información del equipo ===")

    for clave, valor in info_maquina.items():
        print(f"  {clave}: {valor}")

    resultados = []
    numero_simulacion = 1

    for n in N_VALORES:

        simulaciones_n = obtener_simulaciones(n)

        print(
            f"\nEjecutando {simulaciones_n} repeticiones "
            f"por algoritmo con N = {n}..."
        )

        for simulacion_local in range(simulaciones_n):

            resultado_bfs = medir_algoritmo(
                resolver_bfs,
                n,
            )

            resultado_dfs = medir_algoritmo(
                resolver_dfs,
                n,
            )

            solucion_bfs = resultado_bfs["solucion"]
            solucion_dfs = resultado_dfs["solucion"]

            if (solucion_bfs is None) != (solucion_dfs is None):
                print(
                    "Advertencia: BFS y DFS difieren en la existencia "
                    f"de solución (simulación {numero_simulacion}, N={n})."
                )

            base = {
                "simulacion": numero_simulacion,
                "n": n,
                "hostname": info_maquina["hostname"],
                "procesador": info_maquina["procesador"],
                "ram_gb": info_maquina["ram_total_gb"],
                "python_version": info_maquina["python_version"],
            }

            resultados.append(
                {
                    **base,
                    "algoritmo": "BFS",
                    "tiempo": resultado_bfs["tiempo"],
                    "memoria_kb": resultado_bfs["memoria_kb"],
                    "nodos": resultado_bfs["nodos"],
                    "solucion_encontrada": solucion_bfs is not None,
                }
            )

            resultados.append(
                {
                    **base,
                    "algoritmo": "DFS",
                    "tiempo": resultado_dfs["tiempo"],
                    "memoria_kb": resultado_dfs["memoria_kb"],
                    "nodos": resultado_dfs["nodos"],
                    "solucion_encontrada": solucion_dfs is not None,
                }
            )

            if (simulacion_local + 1) % max(1, simulaciones_n // 5) == 0:
                print(
                    f"  Completadas {simulacion_local + 1}/"
                    f"{simulaciones_n} repeticiones"
                )

            numero_simulacion += 1

    return resultados, info_maquina


def guardar_resultados(resultados, info_maquina):
    """
    Guarda los resultados brutos y la información del equipo.

    Los archivos se escriben siempre dentro del repositorio,
    independientemente de la carpeta desde la cual se ejecute Python.
    """

    CARPETA_DATOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta_archivo = CARPETA_DATOS / "resultados.csv"

    columnas = [
        "simulacion",
        "n",
        "hostname",
        "procesador",
        "ram_gb",
        "python_version",
        "algoritmo",
        "tiempo",
        "memoria_kb",
        "nodos",
        "solucion_encontrada",
    ]

    with ruta_archivo.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas,
        )

        escritor.writeheader()
        escritor.writerows(resultados)

    ruta_info = CARPETA_DATOS / "info_maquina.json"

    with ruta_info.open(
        "w",
        encoding="utf-8",
    ) as archivo:

        json.dump(
            info_maquina,
            archivo,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nResultados guardados en: {ruta_archivo}")
    print(f"Info de máquina guardada en: {ruta_info}")


if __name__ == "__main__":

    resultados, info_maquina = ejecutar_simulaciones()

    guardar_resultados(
        resultados,
        info_maquina,
    )

    print("\nSimulaciones completadas correctamente.")
