"""
100 simulaciones del Puzzle 3x3.

La versión original del notebook utilizaba un estado inicial fijo.
Para las simulaciones se generan estados solucionables a partir de la
meta realizando movimientos aleatorios. Esto permite comparar BFS y DFS
en diferentes instancias del mismo Puzzle.
"""

import csv
import random

from bfs_dfs_puzzle import META_PUZZLE
from medicion import medir_algoritmo


def generar_estado(movimientos_aleatorios=10):
    """Genera un Puzzle solucionable partiendo de la meta."""
    estado = META_PUZZLE
    anterior = None

    for _ in range(movimientos_aleatorios):
        opciones = [
            nuevo
            for nuevo in __import__("bfs_dfs_puzzle").movimientos(estado)
            if nuevo != anterior
        ]

        nuevo = random.choice(opciones)
        anterior, estado = estado, nuevo

    return estado


def ejecutar_simulaciones(cantidad=100, mezcla=10, semilla=42):
    """
    Ejecuta 'cantidad' simulaciones.

    Cada simulación usa el mismo estado inicial para BFS y DFS,
    de modo que la comparación sea justa.
    """
    random.seed(semilla)
    resultados = []

    for simulacion in range(1, cantidad + 1):
        inicio = generar_estado(mezcla)

        for algoritmo in ("BFS", "DFS"):
            resultado = medir_algoritmo(
                algoritmo,
                inicio,
                META_PUZZLE,
            )

            resultados.append({
                "simulacion": simulacion,
                "algoritmo": algoritmo,
                "inicio": inicio,
                "nodos": resultado["nodos"],
                "movimientos": resultado["movimientos"],
                "profundidad": resultado["profundidad"],
                "tiempo": resultado["tiempo"],
            })

    return resultados


def guardar_csv(resultados, archivo="resultados_puzzle.csv"):
    """Guarda las simulaciones en CSV."""
    campos = [
        "simulacion",
        "algoritmo",
        "inicio",
        "nodos",
        "movimientos",
        "profundidad",
        "tiempo",
    ]

    with open(archivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()

        for fila in resultados:
            fila = fila.copy()
            fila["inicio"] = str(fila["inicio"])
            escritor.writerow(fila)


if __name__ == "__main__":
    resultados = ejecutar_simulaciones(cantidad=100)
    guardar_csv(resultados)
    print(f"Se realizaron {len(resultados) // 2} simulaciones.")
    print("Archivo generado: resultados_puzzle.csv")
