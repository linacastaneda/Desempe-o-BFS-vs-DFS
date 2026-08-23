import os

import pandas as pd
import matplotlib.pyplot as plt


def cargar_resultados():
    """
    Carga el archivo CSV generado por las 100 simulaciones.

    Retorna:
        DataFrame de pandas con todos los resultados.
    """

    ruta = os.path.join(
        "resultados",
        "resultados_mochila.csv"
    )

    datos = pd.read_csv(ruta)

    return datos


def calcular_promedios(datos):
    """
    Calcula los valores promedio de tiempo,
    memoria y nodos explorados.

    Los resultados se agrupan por:

        - Cantidad de objetos.
        - Algoritmo utilizado.

    Retorna:
        DataFrame con los promedios.
    """

    promedios = (
        datos
        .groupby(
            ["objetos", "algoritmo"],
            as_index=False
        )
        .agg(
            tiempo_promedio=("tiempo", "mean"),
            memoria_promedio=("memoria_kb", "mean"),
            nodos_promedio=("nodos", "mean")
        )
    )

    return promedios


def grafica_tiempo_simulaciones(datos):
    """
    Genera una gráfica con el tiempo obtenido
    por BFS y DFS en cada una de las 100 simulaciones.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]

    plt.figure(figsize=(12, 6))

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

    plt.xlabel("Número de simulación")
    plt.ylabel("Tiempo de ejecución (segundos)")

    plt.title(
        "Tiempo de ejecución de BFS y DFS "
        "en 100 simulaciones"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def grafica_memoria_simulaciones(datos):
    """
    Genera una gráfica con la memoria pico utilizada
    por BFS y DFS en las 100 simulaciones.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]

    plt.figure(figsize=(12, 6))

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

    plt.xlabel("Número de simulación")
    plt.ylabel("Memoria pico (KB)")

    plt.title(
        "Consumo de memoria de BFS y DFS "
        "en 100 simulaciones"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def grafica_tiempo_por_objetos(promedios):
    """
    Muestra cómo aumenta el tiempo promedio
    cuando aumenta la cantidad de objetos.

    Esta gráfica permite observar la escalabilidad
    de BFS y DFS.
    """

    bfs = promedios[
        promedios["algoritmo"] == "BFS"
    ]

    dfs = promedios[
        promedios["algoritmo"] == "DFS"
    ]

    plt.figure(figsize=(9, 6))

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

    plt.xlabel("Cantidad de objetos")
    plt.ylabel("Tiempo promedio (segundos)")

    plt.title(
        "Tiempo promedio según "
        "la cantidad de objetos"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def grafica_memoria_por_objetos(promedios):
    """
    Muestra cómo aumenta el consumo promedio
    de memoria cuando aumenta la cantidad
    de objetos.
    """

    bfs = promedios[
        promedios["algoritmo"] == "BFS"
    ]

    dfs = promedios[
        promedios["algoritmo"] == "DFS"
    ]

    plt.figure(figsize=(9, 6))

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

    plt.xlabel("Cantidad de objetos")
    plt.ylabel("Memoria promedio (KB)")

    plt.title(
        "Memoria promedio según "
        "la cantidad de objetos"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def grafica_boxplot_tiempo(datos):
    """
    Genera un diagrama de caja para comparar
    la distribución de los tiempos de BFS y DFS
    en las 100 simulaciones.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]["tiempo"]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]["tiempo"]

    plt.figure(figsize=(8, 6))

    plt.boxplot(
        [bfs, dfs],
        labels=["BFS", "DFS"]
    )

    plt.ylabel("Tiempo de ejecución (segundos)")

    plt.title(
        "Distribución del tiempo de ejecución"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def grafica_boxplot_memoria(datos):
    """
    Genera un diagrama de caja para comparar
    la distribución del consumo de memoria
    entre BFS y DFS.
    """

    bfs = datos[
        datos["algoritmo"] == "BFS"
    ]["memoria_kb"]

    dfs = datos[
        datos["algoritmo"] == "DFS"
    ]["memoria_kb"]

    plt.figure(figsize=(8, 6))

    plt.boxplot(
        [bfs, dfs],
        labels=["BFS", "DFS"]
    )

    plt.ylabel("Memoria pico (KB)")

    plt.title(
        "Distribución del consumo de memoria"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def mostrar_resumen(promedios):
    """
    Muestra en consola los resultados promedio
    obtenidos para cada tamaño de problema.
    """

    print()
    print("PROMEDIOS DE LAS SIMULACIONES")
    print()

    for _, fila in promedios.iterrows():

        print(
            f"{int(fila['objetos'])} objetos - "
            f"{fila['algoritmo']}"
        )

        print(
            "Tiempo promedio:",
            fila["tiempo_promedio"],
            "segundos"
        )

        print(
            "Memoria promedio:",
            fila["memoria_promedio"],
            "KB"
        )

        print(
            "Nodos promedio:",
            fila["nodos_promedio"]
        )

        print()


if __name__ == "__main__":

    datos = cargar_resultados()

    promedios = calcular_promedios(datos)

    mostrar_resumen(promedios)

    grafica_tiempo_simulaciones(datos)

    grafica_memoria_simulaciones(datos)

    grafica_tiempo_por_objetos(promedios)

    grafica_memoria_por_objetos(promedios)

    grafica_boxplot_tiempo(datos)

    grafica_boxplot_memoria(datos)