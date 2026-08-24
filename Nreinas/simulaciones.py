import csv
import os
import json
from medicion import medir_algoritmo
from bfs import resolver_bfs
from dfs import resolver_dfs
from graficas import obtener_info_maquina


# Valores de N a probar. BFS crece exponencialmente en memoria/tiempo.
# N=13 toma ~2 min y 230MB en BFS. N=14+ BFS sería muy costoso.
N_VALORES = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# Simulaciones por N. Para N>=11 reducimos porque BFS es muy lento.
SIMULACIONES_POR_N = {
    4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100, 10: 100,
    11: 50, 12: 20, 13: 10
}

def obtener_simulaciones(n):
    return SIMULACIONES_POR_N.get(n, 100)


def ejecutar_simulaciones():
    """
    Ejecuta 100 simulaciones del problema de N-Reinas para cada valor de N.

    Para cada N se ejecutan 100 veces tanto BFS como DFS.

    Retorna:
        tupla: (resultados, info_maquina)
        - resultados: Lista de diccionarios con los resultados de cada simulación.
        - info_maquina: Diccionario con información del hardware/software.
    """
    info_maquina = obtener_info_maquina()
    print(f"\n=== Información del equipo ===")
    for k, v in info_maquina.items():
        print(f"  {k}: {v}")

    resultados = []
    numero_simulacion = 1

    for n in N_VALORES:
        simulaciones_n = obtener_simulaciones(n)
        print(f"\nEjecutando {simulaciones_n} simulaciones con N = {n}...")

        for sim in range(simulaciones_n):
            resultado_bfs = medir_algoritmo(resolver_bfs, n)
            resultado_dfs = medir_algoritmo(resolver_dfs, n)

            solucion_bfs = resultado_bfs["solucion"]
            solucion_dfs = resultado_dfs["solucion"]

            if (solucion_bfs is None) != (solucion_dfs is None):
                print(
                    f"Advertencia: BFS y DFS difieren en existencia de solución "
                    f"(simulación {numero_simulacion}, N={n})"
                )

            base = {
                "simulacion": numero_simulacion,
                "n": n,
                "hostname": info_maquina["hostname"],
                "procesador": info_maquina["procesador"],
                "ram_gb": info_maquina["ram_total_gb"],
                "python_version": info_maquina["python_version"],
            }

            resultados.append({
                **base,
                "algoritmo": "BFS",
                "tiempo": resultado_bfs["tiempo"],
                "memoria_kb": resultado_bfs["memoria_kb"],
                "nodos": resultado_bfs["nodos"],
                "solucion_encontrada": solucion_bfs is not None
            })

            resultados.append({
                **base,
                "algoritmo": "DFS",
                "tiempo": resultado_dfs["tiempo"],
                "memoria_kb": resultado_dfs["memoria_kb"],
                "nodos": resultado_dfs["nodos"],
                "solucion_encontrada": solucion_dfs is not None
            })

            if (sim + 1) % max(1, simulaciones_n // 5) == 0:
                print(f"  Completadas {sim + 1}/{simulaciones_n} simulaciones")

            numero_simulacion += 1

    return resultados, info_maquina


def guardar_resultados(resultados, info_maquina):
    """
    Guarda en un archivo CSV los resultados obtenidos durante las simulaciones.
    Incluye información de la máquina en cada fila.
    """
    carpeta_resultados = os.path.join("..", "resultados", "nreinas", "datos")
    os.makedirs(carpeta_resultados, exist_ok=True)

    ruta_archivo = os.path.join(carpeta_resultados, "resultados.csv")

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
        "solucion_encontrada"
    ]

    with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados)

    # También guardamos la info de la máquina en un JSON separado
    ruta_info = os.path.join(carpeta_resultados, "info_maquina.json")
    with open(ruta_info, "w", encoding="utf-8") as f:
        json.dump(info_maquina, f, indent=2, ensure_ascii=False)

    print(f"\nResultados guardados en: {ruta_archivo}")
    print(f"Info de máquina guardada en: {ruta_info}")


if __name__ == "__main__":
    resultados, info_maquina = ejecutar_simulaciones()
    guardar_resultados(resultados, info_maquina)
    print("\nSimulaciones completadas correctamente.")