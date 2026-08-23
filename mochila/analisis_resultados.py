import pandas as pd


def cargar_datos():
    """
    Carga los resultados obtenidos en las
    100 simulaciones de la mochila.
    """

    ruta = "resultados/resultados_mochila.csv"

    datos = pd.read_csv(ruta)

    return datos


def generar_resumen(datos):
    """
    Calcula estadísticas descriptivas para
    BFS y DFS según la cantidad de objetos.

    Se analizan principalmente:

        - Tiempo de ejecución.
        - Memoria pico utilizada.

    También se incluye la cantidad de nodos
    explorados como información auxiliar.
    """

    resumen = (
        datos
        .groupby(
            ["objetos", "algoritmo"]
        )
        .agg(
            tiempo_promedio=("tiempo", "mean"),
            tiempo_mediana=("tiempo", "median"),
            tiempo_minimo=("tiempo", "min"),
            tiempo_maximo=("tiempo", "max"),
            tiempo_desviacion=("tiempo", "std"),

            memoria_promedio=("memoria_kb", "mean"),
            memoria_mediana=("memoria_kb", "median"),
            memoria_minima=("memoria_kb", "min"),
            memoria_maxima=("memoria_kb", "max"),
            memoria_desviacion=("memoria_kb", "std"),

            nodos_promedio=("nodos", "mean")
        )
        .reset_index()
    )

    return resumen


def comparar_algoritmos(resumen):
    """
    Calcula la diferencia porcentual entre BFS y DFS
    para tiempo y memoria en cada tamaño del problema.

    El porcentaje indica cuánto mayor es el valor de BFS
    respecto a DFS.
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
        suffixes=("_bfs", "_dfs")
    )

    comparacion["diferencia_tiempo_porcentaje"] = (
        (
            comparacion["tiempo_promedio_bfs"]
            - comparacion["tiempo_promedio_dfs"]
        )
        / comparacion["tiempo_promedio_dfs"]
    ) * 100

    comparacion["diferencia_memoria_porcentaje"] = (
        (
            comparacion["memoria_promedio_bfs"]
            - comparacion["memoria_promedio_dfs"]
        )
        / comparacion["memoria_promedio_dfs"]
    ) * 100

    return comparacion


def mostrar_resumen(resumen):
    """
    Muestra en consola las estadísticas
    principales de BFS y DFS.
    """

    print()
    print("RESUMEN ESTADÍSTICO")
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


def mostrar_comparacion(comparacion):
    """
    Muestra la diferencia porcentual
    entre BFS y DFS.
    """

    print()
    print("COMPARACIÓN BFS VS DFS")
    print()

    for _, fila in comparacion.iterrows():

        print(
            f"{int(fila['objetos'])} objetos"
        )

        print(
            f"BFS usa "
            f"{fila['diferencia_tiempo_porcentaje']:.2f}% "
            f"más tiempo que DFS"
        )

        print(
            f"BFS usa "
            f"{fila['diferencia_memoria_porcentaje']:.2f}% "
            f"más memoria que DFS"
        )

        print()


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

    resumen.to_csv(
        "resultados/resumen_mochila.csv",
        index=False
    )

    comparacion.to_csv(
        "resultados/comparacion_mochila.csv",
        index=False
    )

    print(
        "Archivos de análisis guardados correctamente."
    )