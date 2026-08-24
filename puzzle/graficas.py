"""
Gráficas comparativas de BFS y DFS
para el Puzzle 3x3.

Las visualizaciones permiten analizar:

- Tiempo de ejecución.
- Consumo de memoria.
- Nodos explorados.
- Ejecuciones que alcanzaron el límite.
- Tasa de finalización.
- Desempeño únicamente en ejecuciones exitosas.
- Distribución estadística mediante boxplots.

Se generan versiones en escala lineal y logarítmica
para tiempo y memoria cuando la diferencia entre BFS
y DFS es demasiado grande para observar ambos algoritmos
claramente en una escala lineal.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def cargar_datos(
    archivo="resultados/resultados_puzzle.csv"
):
    """
    Carga los resultados de las simulaciones
    del Puzzle 3x3.

    Parámetros:
        archivo:
            Ruta del archivo CSV.

    Retorna:
        DataFrame con los resultados.
    """

    datos = pd.read_csv(
        archivo
    )

    # Convierte limite_alcanzado a booleano
    # si pandas lo interpretó como texto.
    if datos["limite_alcanzado"].dtype != bool:

        datos["limite_alcanzado"] = (
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


def separar_algoritmos(datos):
    """
    Separa las filas correspondientes
    a BFS y DFS.
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
    nombre_archivo
):
    """
    Guarda la figura actual y posteriormente
    la muestra en pantalla.
    """

    plt.tight_layout()

    plt.savefig(
        carpeta / nombre_archivo,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()


def grafica_tiempo_global(
    datos,
    carpeta
):
    """
    Muestra el tiempo de ejecución de BFS y DFS
    en las 100 simulaciones utilizando escala lineal.

    Esta gráfica permite observar directamente
    la magnitud absoluta de la diferencia.
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
        "tiempo_global_puzzle.png"
    )


def grafica_tiempo_global_log(
    datos,
    carpeta
):
    """
    Muestra el tiempo de ejecución con escala logarítmica.

    La escala logarítmica permite visualizar
    simultáneamente los tiempos de BFS y DFS,
    aun cuando difieren por varios órdenes de magnitud.
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
        "Puzzle 3x3 - Tiempo BFS vs DFS "
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
        "tiempo_global_log_puzzle.png"
    )


def grafica_memoria_global(
    datos,
    carpeta
):
    """
    Muestra el consumo de memoria pico
    de BFS y DFS en escala lineal.

    Esta versión permite apreciar la magnitud
    absoluta de la diferencia.
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

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Memoria pico (KB)"
    )

    plt.title(
        "Puzzle 3x3 - Consumo de memoria BFS vs DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "memoria_global_puzzle.png"
    )


def grafica_memoria_global_log(
    datos,
    carpeta
):
    """
    Muestra el consumo de memoria utilizando
    escala logarítmica.

    Esta escala evita que los valores menores
    de BFS queden visualmente comprimidos
    cerca del eje horizontal.
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
        "Puzzle 3x3 - Consumo de memoria BFS vs DFS "
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
        "memoria_global_log_puzzle.png"
    )


def grafica_nodos(
    datos,
    carpeta
):
    """
    Compara la cantidad de nodos explorados
    por BFS y DFS.

    Se mantiene escala lineal porque interesa
    mostrar explícitamente el límite experimental
    de 50000 nodos.
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
        y=50000,
        linestyle="--",
        label="Límite de 50000 nodos"
    )

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Nodos explorados"
    )

    plt.title(
        "Puzzle 3x3 - Nodos explorados BFS vs DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "nodos_puzzle.png"
    )


def grafica_limites(
    datos,
    carpeta
):
    """
    Muestra mediante barras apiladas
    cuántas ejecuciones terminaron normalmente
    y cuántas alcanzaron el límite experimental.
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
                "algoritmo": algoritmo,
                "exitosas": exitosas,
                "limite": limite
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

    # Agrega los números dentro de cada barra.
    for indice, fila in resumen.iterrows():

        plt.text(
            indice,
            fila["exitosas"] / 2,
            str(fila["exitosas"]),
            ha="center",
            va="center"
        )

        if fila["limite"] > 0:

            plt.text(
                indice,
                fila["exitosas"]
                + fila["limite"] / 2,
                str(fila["limite"]),
                ha="center",
                va="center"
            )

    guardar_y_mostrar(
        carpeta,
        "limites_puzzle.png"
    )


def grafica_tasa_finalizacion(
    datos,
    carpeta
):
    """
    Muestra el porcentaje de ejecuciones
    que terminaron normalmente.

    Esta gráfica es útil especialmente
    para presentaciones porque comunica
    rápidamente la diferencia entre algoritmos.
    """

    algoritmos = [
        "BFS",
        "DFS"
    ]

    porcentajes = []

    for algoritmo in algoritmos:

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

        total = len(
            datos_algoritmo
        )

        porcentaje = (
            exitosas
            / total
        ) * 100

        porcentajes.append(
            porcentaje
        )

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        algoritmos,
        porcentajes
    )

    plt.ylabel(
        "Ejecuciones completadas (%)"
    )

    plt.ylim(
        0,
        110
    )

    plt.title(
        "Puzzle 3x3 - Tasa de finalización"
    )

    for indice, porcentaje in enumerate(
        porcentajes
    ):

        plt.text(
            indice,
            porcentaje + 2,
            f"{porcentaje:.0f}%",
            ha="center"
        )

    guardar_y_mostrar(
        carpeta,
        "tasa_finalizacion_puzzle.png"
    )


def obtener_exitosas(
    datos
):
    """
    Retorna únicamente las ejecuciones
    que no alcanzaron el límite.
    """

    return datos[
        datos["limite_alcanzado"] == False
    ].copy()


def grafica_tiempo_exitosas(
    datos,
    carpeta
):
    """
    Compara el tiempo de ejecución únicamente
    en búsquedas que terminaron normalmente.

    Se utiliza scatter porque DFS no posee
    observaciones exitosas en todas las simulaciones.
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

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Tiempo de ejecución (segundos)"
    )

    plt.title(
        "Puzzle 3x3 - Tiempo en ejecuciones exitosas"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "tiempo_exitosas_puzzle.png"
    )


def grafica_tiempo_exitosas_log(
    datos,
    carpeta
):
    """
    Compara el tiempo de las ejecuciones exitosas
    utilizando escala logarítmica.
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
        "tiempo_exitosas_log_puzzle.png"
    )


def grafica_memoria_exitosas(
    datos,
    carpeta
):
    """
    Compara la memoria pico únicamente
    en las búsquedas que terminaron normalmente.
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

    plt.xlabel(
        "Número de simulación"
    )

    plt.ylabel(
        "Memoria pico (KB)"
    )

    plt.title(
        "Puzzle 3x3 - Memoria en ejecuciones exitosas"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "memoria_exitosas_puzzle.png"
    )


def grafica_memoria_exitosas_log(
    datos,
    carpeta
):
    """
    Compara la memoria de las ejecuciones exitosas
    utilizando escala logarítmica.
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
        "memoria_exitosas_log_puzzle.png"
    )


def boxplot_tiempo(
    datos,
    carpeta
):
    """
    Muestra la distribución global
    de los tiempos de ejecución.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.boxplot(
        [
            bfs["tiempo"],
            dfs["tiempo"]
        ],
        tick_labels=[
            "BFS",
            "DFS"
        ]
    )

    plt.ylabel(
        "Tiempo de ejecución (segundos)"
    )

    plt.title(
        "Puzzle 3x3 - Distribución del tiempo"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "boxplot_tiempo_puzzle.png"
    )


def boxplot_tiempo_log(
    datos,
    carpeta
):
    """
    Boxplot del tiempo utilizando
    escala logarítmica.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.boxplot(
        [
            bfs["tiempo"],
            dfs["tiempo"]
        ],
        tick_labels=[
            "BFS",
            "DFS"
        ]
    )

    plt.yscale(
        "log"
    )

    plt.ylabel(
        "Tiempo de ejecución (segundos)"
    )

    plt.title(
        "Puzzle 3x3 - Distribución del tiempo "
        "(escala logarítmica)"
    )

    plt.grid(
        True,
        alpha=0.3,
        which="both"
    )

    guardar_y_mostrar(
        carpeta,
        "boxplot_tiempo_log_puzzle.png"
    )


def boxplot_memoria(
    datos,
    carpeta
):
    """
    Muestra la distribución global
    del consumo de memoria.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.boxplot(
        [
            bfs["memoria_kb"],
            dfs["memoria_kb"]
        ],
        tick_labels=[
            "BFS",
            "DFS"
        ]
    )

    plt.ylabel(
        "Memoria pico (KB)"
    )

    plt.title(
        "Puzzle 3x3 - Distribución de memoria"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "boxplot_memoria_puzzle.png"
    )


def boxplot_memoria_log(
    datos,
    carpeta
):
    """
    Boxplot del consumo de memoria
    utilizando escala logarítmica.
    """

    bfs, dfs = separar_algoritmos(
        datos
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.boxplot(
        [
            bfs["memoria_kb"],
            dfs["memoria_kb"]
        ],
        tick_labels=[
            "BFS",
            "DFS"
        ]
    )

    plt.yscale(
        "log"
    )

    plt.ylabel(
        "Memoria pico (KB)"
    )

    plt.title(
        "Puzzle 3x3 - Distribución de memoria "
        "(escala logarítmica)"
    )

    plt.grid(
        True,
        alpha=0.3,
        which="both"
    )

    guardar_y_mostrar(
        carpeta,
        "boxplot_memoria_log_puzzle.png"
    )


def generar_graficas(
    archivo="resultados/resultados_puzzle.csv",
    carpeta="resultados/graficas_puzzle"
):
    """
    Genera únicamente las gráficas principales
    utilizadas en el análisis del Puzzle 3x3.
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
        "Se generaron las 6 gráficas principales."
    )

    print(
        "Carpeta:",
        carpeta
    )
if __name__ == "__main__":

    generar_graficas()