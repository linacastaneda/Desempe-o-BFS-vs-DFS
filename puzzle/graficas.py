from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


MAX_NODOS = 50000


def cargar_datos(
    archivo="resultados/puzzle/datos/resultados.csv"
):
    """
    Carga los resultados del Puzzle.
    """

    datos = pd.read_csv(
        archivo
    )

    if (
        datos["limite_alcanzado"].dtype
        != bool
    ):

        datos[
            "limite_alcanzado"
        ] = (
            datos["limite_alcanzado"]
            .astype(str)
            .str.lower()
            .map(
                {
                    "true": True,
                    "false": False
                }
            )
        )

    return datos


def separar_algoritmos(
    datos
):
    """
    Separa BFS y DFS.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]

    return bfs, dfs


def guardar_y_mostrar(
    carpeta,
    nombre
):
    """
    Guarda y muestra la gráfica.
    """

    plt.tight_layout()

    plt.savefig(
        carpeta / nombre,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()


def grafica_tiempo_global(
    datos,
    carpeta
):
    """
    Tiempo de las 100 ejecuciones.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        bfs["simulacion"],
        bfs["tiempo"],
        label="BFS"
    )

    plt.plot(
        dfs["simulacion"],
        dfs["tiempo"],
        label="DFS"
    )

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Tiempo de ejecución (segundos)"
    )

    plt.title(
        "Puzzle 3x3 - Tiempo de ejecución BFS vs DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "01_tiempo_global.png"
    )


def grafica_memoria_global_log(
    datos,
    carpeta
):
    """
    Memoria pico en escala logarítmica.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        bfs["simulacion"],
        bfs["memoria_kb"],
        label="BFS"
    )

    plt.plot(
        dfs["simulacion"],
        dfs["memoria_kb"],
        label="DFS"
    )

    plt.yscale(
        "log"
    )

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Memoria pico (KB)"
    )

    plt.title(
        "Puzzle 3x3 - Memoria BFS vs DFS "
        "(escala logarítmica)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
        which="both"
    )

    guardar_y_mostrar(
        carpeta,
        "02_memoria_global_log.png"
    )


def grafica_nodos(
    datos,
    carpeta
):
    """
    Nodos explorados y límite experimental.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        bfs["simulacion"],
        bfs["nodos"],
        label="BFS"
    )

    plt.plot(
        dfs["simulacion"],
        dfs["nodos"],
        label="DFS"
    )

    plt.axhline(
        y=MAX_NODOS,
        linestyle="--",
        label="Límite de 50.000 nodos"
    )

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Nodos explorados"
    )

    plt.title(
        "Puzzle 3x3 - Nodos explorados"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "03_nodos.png"
    )


def grafica_limites(
    datos,
    carpeta
):
    """
    Ejecuciones completadas y limitadas.
    """

    resultados = []

    for algoritmo in [
        "BFS",
        "DFS"
    ]:

        datos_algoritmo = datos[
            datos["algoritmo"] == algoritmo
        ]

        exitosas = len(
            datos_algoritmo[
                datos_algoritmo[
                    "limite_alcanzado"
                ] == False
            ]
        )

        limite = len(
            datos_algoritmo[
                datos_algoritmo[
                    "limite_alcanzado"
                ] == True
            ]
        )

        resultados.append(
            {
                "algoritmo":
                    algoritmo,

                "exitosas":
                    exitosas,

                "limite":
                    limite
            }
        )

    resumen = pd.DataFrame(
        resultados
    )

    posiciones = range(
        len(resumen)
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        posiciones,
        resumen["exitosas"],
        label="Terminó normalmente"
    )

    plt.bar(
        posiciones,
        resumen["limite"],
        bottom=resumen["exitosas"],
        label="Alcanzó el límite"
    )

    plt.xticks(
        posiciones,
        resumen["algoritmo"]
    )

    plt.ylabel(
        "Cantidad de simulaciones"
    )

    plt.title(
        "Puzzle 3x3 - Resultado de las 100 simulaciones"
    )

    plt.legend()

    for indice, fila in resumen.iterrows():

        plt.text(
            indice,
            fila["exitosas"] / 2,
            str(
                fila["exitosas"]
            ),
            ha="center",
            va="center"
        )

        if fila["limite"] > 0:

            plt.text(
                indice,
                (
                    fila["exitosas"]
                    + fila["limite"] / 2
                ),
                str(
                    fila["limite"]
                ),
                ha="center",
                va="center"
            )

    guardar_y_mostrar(
        carpeta,
        "04_limites.png"
    )


def obtener_exitosas(
    datos
):
    """
    Retorna únicamente búsquedas
    terminadas normalmente.
    """

    return datos[
        datos["limite_alcanzado"] == False
    ].copy()


def grafica_tiempo_exitosas_log(
    datos,
    carpeta
):
    """
    Tiempo solamente de búsquedas exitosas.
    """

    exitosas = obtener_exitosas(
        datos
    )

    bfs = exitosas[
        exitosas["algoritmo"] == "BFS"
    ]

    dfs = exitosas[
        exitosas["algoritmo"] == "DFS"
    ]

    plt.figure(
        figsize=(12, 6)
    )

    plt.scatter(
        bfs["simulacion"],
        bfs["tiempo"],
        label="BFS"
    )

    plt.scatter(
        dfs["simulacion"],
        dfs["tiempo"],
        label="DFS"
    )

    plt.yscale(
        "log"
    )

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Tiempo de ejecución (segundos)"
    )

    plt.title(
        "Puzzle 3x3 - Tiempo en ejecuciones exitosas "
        "(escala logarítmica)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
        which="both"
    )

    guardar_y_mostrar(
        carpeta,
        "05_tiempo_exitosas_log.png"
    )


def grafica_memoria_exitosas_log(
    datos,
    carpeta
):
    """
    Memoria solamente de búsquedas exitosas.
    """

    exitosas = obtener_exitosas(
        datos
    )

    bfs = exitosas[
        exitosas["algoritmo"] == "BFS"
    ]

    dfs = exitosas[
        exitosas["algoritmo"] == "DFS"
    ]

    plt.figure(
        figsize=(12, 6)
    )

    plt.scatter(
        bfs["simulacion"],
        bfs["memoria_kb"],
        label="BFS"
    )

    plt.scatter(
        dfs["simulacion"],
        dfs["memoria_kb"],
        label="DFS"
    )

    plt.yscale(
        "log"
    )

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Memoria pico (KB)"
    )

    plt.title(
        "Puzzle 3x3 - Memoria en ejecuciones exitosas "
        "(escala logarítmica)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
        which="both"
    )

    guardar_y_mostrar(
        carpeta,
        "06_memoria_exitosas_log.png"
    )


def generar_graficas(
    archivo="resultados/puzzle/datos/resultados.csv",
    carpeta="resultados/puzzle/graficas/comparacion"
):
    """
    Genera las seis gráficas principales.
    """

    datos = cargar_datos(
        archivo
    )

    carpeta = Path(
        carpeta
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    grafica_tiempo_global(
        datos,
        carpeta
    )

    grafica_memoria_global_log(
        datos,
        carpeta
    )

    grafica_nodos(
        datos,
        carpeta
    )

    grafica_limites(
        datos,
        carpeta
    )

    grafica_tiempo_exitosas_log(
        datos,
        carpeta
    )

    grafica_memoria_exitosas_log(
        datos,
        carpeta
    )

    print()

    print(
        "Las 6 gráficas fueron guardadas en:",
        carpeta
    )


if __name__ == "__main__":

    generar_graficas()