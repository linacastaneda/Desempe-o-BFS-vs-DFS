"""
100 simulaciones del Puzzle 3x3.

Genera diferentes estados iniciales solucionables y compara BFS y DFS.
Se utiliza un límite de nodos para evitar que una ejecución se quede
indefinidamente explorando el espacio de estados.
"""

import csv
import random

from bfs_dfs_puzzle import META_PUZZLE, movimientos
from medicion import medir_algoritmo


# Límite de seguridad para cada ejecución.
MAX_NODOS = 50000


def generar_estado(movimientos_aleatorios=6):
    """
    Genera un estado solucionable partiendo de la meta.

    Al partir de la meta y realizar movimientos válidos, todos los
    estados generados son solucionables.
    """
    estado = META_PUZZLE
    anterior = None

    for _ in range(movimientos_aleatorios):
        opciones = [
            nuevo
            for nuevo in movimientos(estado)
            if nuevo != anterior
        ]

        nuevo = random.choice(opciones)
        anterior = estado
        estado = nuevo

    return estado


def medir_seguro(algoritmo, inicio):
    """
    Ejecuta BFS o DFS con un límite de nodos.

    Si alcanza el límite, la simulación queda marcada como
    'limite_alcanzado' en lugar de quedarse ejecutándose.
    """

    resultado = medir_algoritmo(
        algoritmo,
        inicio,
        META_PUZZLE,
    )

    resultado["limite_alcanzado"] = (
        resultado["nodos"] >= MAX_NODOS
    )

    return resultado


def ejecutar_simulaciones(
    cantidad=100,
    mezcla=6,
    semilla=42,
):
    """
    Ejecuta 100 simulaciones.

    Para cada simulación:
        1. Se genera un estado inicial.
        2. Se ejecuta BFS.
        3. Se ejecuta DFS.
        4. Se guardan las métricas.
    """

    random.seed(semilla)
    resultados = []

    for simulacion in range(1, cantidad + 1):

        inicio = generar_estado(mezcla)

        print(
            f"Simulación {simulacion}/{cantidad}...",
            end="\r",
        )

        for algoritmo in ("BFS", "DFS"):

            resultado = medir_seguro(
                algoritmo,
                inicio,
            )

            resultados.append({
                "simulacion": simulacion,
                "algoritmo": algoritmo,
                "inicio": inicio,
                "nodos": resultado["nodos"],
                "movimientos": resultado["movimientos"],
                "profundidad": resultado["profundidad"],
                "tiempo": resultado["tiempo"],
                "limite_alcanzado": resultado[
                    "limite_alcanzado"
                ],
            })

    print()
    return resultados


def guardar_csv(
    resultados,
    archivo="resultados_puzzle.csv",
):
    """Guarda los resultados en un archivo CSV."""

    campos = [
        "simulacion",
        "algoritmo",
        "inicio",
        "nodos",
        "movimientos",
        "profundidad",
        "tiempo",
        "limite_alcanzado",
    ]

    with open(
        archivo,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        escritor = csv.DictWriter(
            f,
            fieldnames=campos,
        )

        escritor.writeheader()

        for fila in resultados:

            fila = fila.copy()

            fila["inicio"] = str(
                fila["inicio"]
            )

            escritor.writerow(fila)


if __name__ == "__main__":

    resultados = ejecutar_simulaciones(
        cantidad=100,
        mezcla=6,
        semilla=42,
    )

    guardar_csv(resultados)

    print(
        "Se realizaron 100 simulaciones."
    )

    print(
        "Se compararon BFS y DFS en cada simulación."
    )

    print(
        "Archivo generado: "
        "resultados_puzzle.csv"
    )
