import os

import pandas as pd


def cargar_datos():
    """
    Carga los resultados de las simulaciones
    de la mochila.
    """

    ruta = os.path.join(
        "resultados",
        "mochila",
        "datos",
        "resultados.csv"
    )

    datos = pd.read_csv(
        ruta
    )

    return datos


def generar_resumen(
    datos
):
    """
    Calcula estadísticas descriptivas
    para BFS y DFS según la cantidad
    de objetos.
    """

    resumen = (
        datos
        .groupby(
            [
                "objetos",
                "algoritmo"
            ]
        )
        .agg(
            tiempo_promedio=(
                "tiempo",
                "mean"
            ),
            tiempo_mediana=(
                "tiempo",
                "median"
            ),
            tiempo_minimo=(
                "tiempo",
                "min"
            ),
            tiempo_maximo=(
                "tiempo",
                "max"
            ),
            tiempo_desviacion=(
                "tiempo",
                "std"
            ),

            memoria_promedio=(
                "memoria_kb",
                "mean"
            ),
            memoria_mediana=(
                "memoria_kb",
                "median"
            ),
            memoria_minima=(
                "memoria_kb",
                "min"
            ),
            memoria_maxima=(
                "memoria_kb",
                "max"
            ),
            memoria_desviacion=(
                "memoria_kb",
                "std"
            ),

            nodos_promedio=(
                "nodos",
                "mean"
            )
        )
        .reset_index()
    )

    return resumen


def comparar_algoritmos(
    resumen
):
    """
    Compara BFS y DFS para cada
    cantidad de objetos.
    """

    bfs = resumen[
        resumen["algoritmo"] == "BFS"
    ].copy()

    dfs = resumen[
        resumen["algoritmo"] == "DFS"
    ].copy()

    comparacion = pd.merge(
        bfs,
        dfs,
        on="objetos",
        suffixes=(
            "_bfs",
            "_dfs"
        )
    )

    comparacion[
        "diferencia_tiempo_porcentaje"
    ] = (
        (
            comparacion[
                "tiempo_promedio_bfs"
            ]
            - comparacion[
                "tiempo_promedio_dfs"
            ]
        )
        / comparacion[
            "tiempo_promedio_dfs"
        ]
    ) * 100

    comparacion[
        "diferencia_memoria_porcentaje"
    ] = (
        (
            comparacion[
                "memoria_promedio_bfs"
            ]
            - comparacion[
                "memoria_promedio_dfs"
            ]
        )
        / comparacion[
            "memoria_promedio_dfs"
        ]
    ) * 100

    return comparacion


def mostrar_resumen(
    resumen
):
    """
    Muestra las estadísticas principales.
    """

    print()

    print(
        "RESUMEN ESTADÍSTICO - MOCHILA"
    )

    print()

    for _, fila in resumen.iterrows():

        print(
            f"{int(fila['objetos'])} objetos - "
            f"{fila['algoritmo']}"
        )

        print(
            f"Tiempo promedio: "
            f"{fila['tiempo_promedio']:.8f} s"
        )

        print(
            f"Tiempo mediana: "
            f"{fila['tiempo_mediana']:.8f} s"
        )

        print(
            f"Memoria promedio: "
            f"{fila['memoria_promedio']:.4f} KB"
        )

        print(
            f"Memoria mediana: "
            f"{fila['memoria_mediana']:.4f} KB"
        )

        print(
            f"Nodos promedio: "
            f"{fila['nodos_promedio']:.2f}"
        )

        print()


def mostrar_comparacion(
    comparacion
):
    """
    Presenta la comparación entre
    BFS y DFS.
    """

    print()

    print(
        "COMPARACIÓN BFS VS DFS - MOCHILA"
    )

    print()

    for _, fila in comparacion.iterrows():

        objetos = int(
            fila["objetos"]
        )

        diferencia_tiempo = fila[
            "diferencia_tiempo_porcentaje"
        ]

        diferencia_memoria = fila[
            "diferencia_memoria_porcentaje"
        ]

        print(
            f"{objetos} objetos"
        )

        if diferencia_tiempo >= 0:

            print(
                f"BFS utilizó "
                f"{diferencia_tiempo:.2f}% "
                f"más tiempo que DFS."
            )

        else:

            print(
                f"BFS utilizó "
                f"{abs(diferencia_tiempo):.2f}% "
                f"menos tiempo que DFS."
            )

        if diferencia_memoria >= 0:

            print(
                f"BFS utilizó "
                f"{diferencia_memoria:.2f}% "
                f"más memoria que DFS."
            )

        else:

            print(
                f"BFS utilizó "
                f"{abs(diferencia_memoria):.2f}% "
                f"menos memoria que DFS."
            )

        print()


def guardar_analisis(
    resumen,
    comparacion
):
    """
    Guarda los archivos de análisis en:

        resultados/mochila/datos/
    """

    carpeta = os.path.join(
        "resultados",
        "mochila",
        "datos"
    )

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    resumen.to_csv(
        os.path.join(
            carpeta,
            "resumen.csv"
        ),
        index=False
    )

    comparacion.to_csv(
        os.path.join(
            carpeta,
            "comparacion.csv"
        ),
        index=False
    )


if __name__ == "__main__":

    datos = cargar_datos()

    resumen = generar_resumen(
        datos
    )

    comparacion = comparar_algoritmos(
        resumen
    )

    mostrar_resumen(
        resumen
    )

    mostrar_comparacion(
        comparacion
    )

    guardar_analisis(
        resumen,
        comparacion
    )

    print(
        "Archivos de análisis guardados en "
        "resultados/mochila/datos/"
    )