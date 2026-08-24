from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def cargar_resultados(
    archivo="resultados/mochila/datos/resultados.csv"
):
    """
    Carga las 100 simulaciones de Mochila.
    """

    return pd.read_csv(
        archivo
    )


def calcular_promedios(
    datos
):
    """
    Calcula los promedios por cantidad
    de objetos y algoritmo.
    """

    return (
        datos
        .groupby(
            [
                "objetos",
                "algoritmo"
            ],
            as_index=False
        )
        .agg(
            tiempo_promedio=(
                "tiempo",
                "mean"
            ),

            memoria_promedio=(
                "memoria_kb",
                "mean"
            ),

            nodos_promedio=(
                "nodos",
                "mean"
            )
        )
    )


def guardar_y_mostrar(
    carpeta,
    nombre_archivo
):
    """
    Guarda y muestra la figura actual.
    """

    plt.tight_layout()

    plt.savefig(
        carpeta / nombre_archivo,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()


def grafica_tiempo_simulaciones(
    datos,
    carpeta
):
    """
    Tiempo de BFS y DFS en las
    100 simulaciones.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]

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
        "Mochila 0/1 - Tiempo de ejecución BFS vs DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "01_tiempo_simulaciones.png"
    )


def grafica_memoria_simulaciones(
    datos,
    carpeta
):
    """
    Memoria pico de BFS y DFS
    en las 100 simulaciones.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]

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
        "Mochila 0/1 - Memoria BFS vs DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "02_memoria_simulaciones.png"
    )


def grafica_tiempo_por_objetos(
    promedios,
    carpeta
):
    """
    Tiempo promedio según cantidad
    de objetos.
    """

    bfs = promedios[
        promedios["algoritmo"] == "BFS"
    ]

    dfs = promedios[
        promedios["algoritmo"] == "DFS"
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        bfs["objetos"],
        bfs["tiempo_promedio"],
        marker="o",
        label="BFS"
    )

    plt.plot(
        dfs["objetos"],
        dfs["tiempo_promedio"],
        marker="o",
        label="DFS"
    )

    plt.xlabel(
        "Cantidad de objetos"
    )

    plt.ylabel(
        "Tiempo promedio (segundos)"
    )

    plt.title(
        "Mochila 0/1 - Tiempo promedio según tamaño"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "03_tiempo_por_objetos.png"
    )


def grafica_memoria_por_objetos(
    promedios,
    carpeta
):
    """
    Memoria promedio según cantidad
    de objetos.
    """

    bfs = promedios[
        promedios["algoritmo"] == "BFS"
    ]

    dfs = promedios[
        promedios["algoritmo"] == "DFS"
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        bfs["objetos"],
        bfs["memoria_promedio"],
        marker="o",
        label="BFS"
    )

    plt.plot(
        dfs["objetos"],
        dfs["memoria_promedio"],
        marker="o",
        label="DFS"
    )

    plt.xlabel(
        "Cantidad de objetos"
    )

    plt.ylabel(
        "Memoria promedio (KB)"
    )

    plt.title(
        "Mochila 0/1 - Memoria promedio según tamaño"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "04_memoria_por_objetos.png"
    )


def generar_graficas(
    archivo="resultados/mochila/datos/resultados.csv",
    carpeta="resultados/mochila/graficas/comparacion"
):
    """
    Genera las cuatro gráficas principales
    de Mochila.
    """

    datos = cargar_resultados(
        archivo
    )

    promedios = calcular_promedios(
        datos
    )

    carpeta = Path(
        carpeta
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    grafica_tiempo_simulaciones(
        datos,
        carpeta
    )

    grafica_memoria_simulaciones(
        datos,
        carpeta
    )

    grafica_tiempo_por_objetos(
        promedios,
        carpeta
    )

    grafica_memoria_por_objetos(
        promedios,
        carpeta
    )

    print()

    print(
        "Gráficas guardadas en:",
        carpeta
    )


if __name__ == "__main__":

    generar_graficas()