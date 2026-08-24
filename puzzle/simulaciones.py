"""
100 simulaciones del Puzzle 3x3.

Se generan diferentes estados iniciales solucionables
y se compara BFS contra DFS.

En cada simulación ambos algoritmos reciben exactamente
el mismo estado inicial.

Se registran:

- Tiempo de ejecución.
- Memoria pico.
- Nodos explorados.
- Movimientos.
- Profundidad.
"""

import csv
import os
import random

from bfs_dfs_puzzle import (
    META_PUZZLE,
    movimientos,
)

from medicion import medir_algoritmo


# Límite máximo de nodos permitidos
# para cada ejecución.
MAX_NODOS = 50000


def generar_estado(
    movimientos_aleatorios=6
):
    """
    Genera un estado solucionable del Puzzle 3x3.

    El proceso comienza desde el estado meta
    y realiza movimientos válidos aleatorios.

    Debido a que el estado se obtiene mediante
    movimientos válidos desde la meta, se garantiza
    que el problema tenga solución.

    Parámetros:
        movimientos_aleatorios:
            Cantidad de movimientos utilizados
            para mezclar el puzzle.

    Retorna:
        Estado inicial solucionable.
    """

    estado = META_PUZZLE

    anterior = None

    for _ in range(
        movimientos_aleatorios
    ):

        opciones = [
            nuevo
            for nuevo in movimientos(estado)
            if nuevo != anterior
        ]

        nuevo = random.choice(
            opciones
        )

        anterior = estado

        estado = nuevo

    return estado


def medir_seguro(
    algoritmo,
    inicio
):
    """
    Ejecuta BFS o DFS con un límite máximo
    de nodos.

    Si el algoritmo alcanza el límite,
    la ejecución queda marcada mediante
    la variable limite_alcanzado.
    """

    resultado = medir_algoritmo(
        algoritmo,
        inicio,
        META_PUZZLE,
        max_nodos=MAX_NODOS,
    )

    resultado["limite_alcanzado"] = (
        resultado["nodos"]
        >= MAX_NODOS
        and resultado["solucion"] is None
    )

    return resultado


def ejecutar_simulaciones(
    cantidad=100,
    mezcla=6,
    semilla=42,
):
    """
    Ejecuta las simulaciones del Puzzle 3x3.

    Para cada simulación:

        1. Se genera un estado inicial solucionable.
        2. Se ejecuta BFS.
        3. Se ejecuta DFS.
        4. Se registran sus métricas.

    BFS y DFS utilizan exactamente el mismo
    estado inicial.
    """

    random.seed(
        semilla
    )

    resultados = []

    for simulacion in range(
        1,
        cantidad + 1
    ):

        inicio = generar_estado(
            mezcla
        )

        print(
            f"Simulación "
            f"{simulacion}/{cantidad}",
            end="\r"
        )

        for algoritmo in (
            "BFS",
            "DFS"
        ):

            resultado = medir_seguro(
                algoritmo,
                inicio
            )

            resultados.append(
                {
                    "simulacion": simulacion,
                    "algoritmo": algoritmo,
                    "inicio": inicio,
                    "mezcla": mezcla,
                    "nodos": resultado["nodos"],
                    "movimientos": resultado["movimientos"],
                    "profundidad": resultado["profundidad"],
                    "tiempo": resultado["tiempo"],
                    "memoria_kb": resultado["memoria_kb"],
                    "limite_alcanzado": (
                        resultado[
                            "limite_alcanzado"
                        ]
                    ),
                }
            )

    print()

    return resultados


def guardar_csv(
    resultados,
    archivo=os.path.join(
        "resultados",
        "resultados_puzzle.csv"
    ),
):
    """
    Guarda los resultados obtenidos
    en un archivo CSV.
    """

    carpeta = os.path.dirname(
        archivo
    )

    if carpeta:

        os.makedirs(
            carpeta,
            exist_ok=True
        )

    campos = [
        "simulacion",
        "algoritmo",
        "inicio",
        "mezcla",
        "nodos",
        "movimientos",
        "profundidad",
        "tiempo",
        "memoria_kb",
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

            escritor.writerow(
                fila
            )


if __name__ == "__main__":

    resultados = ejecutar_simulaciones(
        cantidad=100,
        mezcla=6,
        semilla=42,
    )

    guardar_csv(
        resultados
    )

    print(
        "Se realizaron 100 simulaciones."
    )

    print(
        "Se compararon BFS y DFS "
        "en cada simulación."
    )

    print(
        "Archivo generado: "
        "resultados/resultados_puzzle.csv"
    )