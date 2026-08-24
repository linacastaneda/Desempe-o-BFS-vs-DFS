from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def cargar_resultados(
    archivo="resultados/resultados_mochila.csv"
):
    """
    Carga el archivo CSV generado por las
    100 simulaciones del problema de la mochila.
    """

    datos = pd.read_csv(
        archivo
    )

    return datos


def calcular_promedios(datos):
    """
    Calcula los promedios de tiempo,
    memoria y nodos explorados.

    Los resultados se agrupan por:

        - Cantidad de objetos.
        - Algoritmo.
    """

    promedios = (
        datos
        .groupby(
            ["objetos", "algoritmo"],
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

    return promedios


def guardar_y_mostrar(
    carpeta,
    nombre_archivo
):
    """
    Guarda la gráfica actual y posteriormente
    la muestra en pantalla.
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
    Compara el tiempo de BFS y DFS
    en cada una de las 100 simulaciones.
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
        "tiempo_simulaciones_mochila.png"
    )


def grafica_memoria_simulaciones(
    datos,
    carpeta
):
    """
    Compara la memoria pico utilizada
    por BFS y DFS en las 100 simulaciones.
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
        "Mochila 0/1 - Consumo de memoria BFS vs DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "memoria_simulaciones_mochila.png"
    )


def grafica_tiempo_por_objetos(
    promedios,
    carpeta
):
    """
    Muestra cómo cambia el tiempo promedio
    cuando aumenta la cantidad de objetos.

    Esta gráfica es especialmente importante
    para analizar la escalabilidad.
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
        "Mochila 0/1 - Tiempo promedio "
        "según la cantidad de objetos"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "tiempo_por_objetos_mochila.png"
    )


def grafica_memoria_por_objetos(
    promedios,
    carpeta
):
    """
    Muestra cómo cambia el consumo promedio
    de memoria cuando aumenta la cantidad
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
        "Mochila 0/1 - Memoria promedio "
        "según la cantidad de objetos"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    guardar_y_mostrar(
        carpeta,
        "memoria_por_objetos_mochila.png"
    )


def mostrar_resumen(
    promedios
):
    """
    Muestra en consola los resultados promedio
    para cada tamaño del problema.
    """

    print()
    print(
        "PROMEDIOS DE LAS SIMULACIONES - MOCHILA"
    )
    print()

    for _, fila in promedios.iterrows():

        print(
            f"{int(fila['objetos'])} objetos - "
            f"{fila['algoritmo']}"
        )

        print(
            f"Tiempo promedio: "
            f"{fila['tiempo_promedio']:.8f} segundos"
        )

        print(
            f"Memoria promedio: "
            f"{fila['memoria_promedio']:.4f} KB"
        )

        print(
            f"Nodos promedio: "
            f"{fila['nodos_promedio']:.2f}"
        )

        print()


def generar_graficas(
    archivo="resultados/resultados_mochila.csv",
    carpeta="resultados/graficas_mochila"
):
    """
    Genera y guarda las cuatro gráficas principales
    del análisis del problema de la mochila.
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

    mostrar_resumen(
        promedios
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
        "Se generaron las 4 gráficas principales."
    )

    print(
        "Carpeta:",
        carpeta
    )


if __name__ == "__main__":

    generar_graficas()