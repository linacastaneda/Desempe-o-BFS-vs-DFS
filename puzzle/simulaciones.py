import csv
import os
import random

from bfs_dfs_puzzle import (
    META_PUZZLE,
    movimientos,
)

from medicion import medir_algoritmo


MAX_NODOS = 50000


def generar_estado(
    movimientos_aleatorios=6
):
    """
    Genera un estado solucionable
    partiendo desde la meta.
    """

    estado = META_PUZZLE

    anterior = None

    for _ in range(
        movimientos_aleatorios
    ):

        opciones = [
            nuevo
            for nuevo
            in movimientos(estado)
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
    Ejecuta un algoritmo respetando
    el límite de 50.000 nodos.
    """

    resultado = medir_algoritmo(
        algoritmo,
        inicio,
        META_PUZZLE,
        max_nodos=MAX_NODOS
    )

    resultado[
        "limite_alcanzado"
    ] = (
        resultado["nodos"] >= MAX_NODOS
        and resultado["solucion"] is None
    )

    return resultado


def ejecutar_simulaciones(
    cantidad=100,
    mezcla=6,
    semilla=42
):
    """
    Ejecuta las simulaciones del Puzzle.
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

        for algoritmo in [
            "BFS",
            "DFS"
        ]:

            resultado = medir_seguro(
                algoritmo,
                inicio
            )

            resultados.append(
                {
                    "simulacion":
                        simulacion,

                    "algoritmo":
                        algoritmo,

                    "inicio":
                        inicio,

                    "mezcla":
                        mezcla,

                    "nodos":
                        resultado["nodos"],

                    "movimientos":
                        resultado["movimientos"],

                    "profundidad":
                        resultado["profundidad"],

                    "tiempo":
                        resultado["tiempo"],

                    "memoria_kb":
                        resultado["memoria_kb"],

                    "limite_alcanzado":
                        resultado[
                            "limite_alcanzado"
                        ]
                }
            )

    print()

    return resultados


def guardar_csv(
    resultados,
    archivo=os.path.join(
        "resultados",
        "puzzle",
        "datos",
        "resultados.csv"
    )
):
    """
    Guarda los resultados en CSV.
    """

    carpeta = os.path.dirname(
        archivo
    )

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
        "limite_alcanzado"
    ]

    with open(
        archivo,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo_csv:

        escritor = csv.DictWriter(
            archivo_csv,
            fieldnames=campos
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
        semilla=42
    )

    guardar_csv(
        resultados
    )

    print(
        "Resultados guardados en "
        "resultados/puzzle/datos/resultados.csv"
    )