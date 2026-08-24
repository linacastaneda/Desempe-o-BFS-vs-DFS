"""
Análisis estadístico de los resultados obtenidos
por BFS y DFS en el Puzzle 3x3.

El objetivo principal es comparar:

- Tiempo de ejecución.
- Consumo de memoria.

También se utilizan como métricas auxiliares:

- Nodos explorados.
- Cantidad de movimientos.
- Profundidad de la solución.
- Ejecuciones que alcanzaron el límite de nodos.
"""

import os

import pandas as pd


def cargar_datos(
    archivo="resultados/resultados_puzzle.csv"
):
    """
    Carga el archivo CSV generado por las
    100 simulaciones del Puzzle 3x3.

    Retorna:
        DataFrame de pandas con los resultados.
    """

    datos = pd.read_csv(
        archivo
    )

    # Se asegura que la columna limite_alcanzado
    # sea interpretada correctamente como booleano.
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


def generar_resumen(datos):
    """
    Calcula estadísticas descriptivas utilizando
    todas las ejecuciones realizadas.

    Esto incluye tanto las ejecuciones que encontraron
    solución como las que alcanzaron el límite
    máximo de nodos.
    """

    resumen = (
        datos
        .groupby(
            "algoritmo"
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
            ),

            movimientos_promedio=(
                "movimientos",
                "mean"
            ),

            profundidad_promedio=(
                "profundidad",
                "mean"
            )
        )
        .reset_index()
    )

    return resumen


def comparar_algoritmos(resumen):
    """
    Compara los promedios globales de BFS y DFS.

    En lugar de mostrar porcentajes negativos,
    los resultados se expresan de manera más
    comprensible:

        - Cuánto menos tiempo utiliza BFS.
        - Cuánto menos memoria utiliza BFS.
        - Cuántas veces más tarda DFS.
        - Cuántas veces más memoria utiliza DFS.
    """

    bfs = resumen[
        resumen["algoritmo"] == "BFS"
    ].iloc[0]

    dfs = resumen[
        resumen["algoritmo"] == "DFS"
    ].iloc[0]

    porcentaje_menos_tiempo_bfs = (
        (
            dfs["tiempo_promedio"]
            - bfs["tiempo_promedio"]
        )
        / dfs["tiempo_promedio"]
    ) * 100

    porcentaje_menos_memoria_bfs = (
        (
            dfs["memoria_promedio"]
            - bfs["memoria_promedio"]
        )
        / dfs["memoria_promedio"]
    ) * 100

    veces_tiempo_dfs = (
        dfs["tiempo_promedio"]
        / bfs["tiempo_promedio"]
    )

    veces_memoria_dfs = (
        dfs["memoria_promedio"]
        / bfs["memoria_promedio"]
    )

    return {
        "porcentaje_menos_tiempo_bfs":
            porcentaje_menos_tiempo_bfs,

        "porcentaje_menos_memoria_bfs":
            porcentaje_menos_memoria_bfs,

        "veces_tiempo_dfs":
            veces_tiempo_dfs,

        "veces_memoria_dfs":
            veces_memoria_dfs
    }


def analizar_limites(datos):
    """
    Cuenta cuántas ejecuciones alcanzaron
    el límite máximo de nodos.

    Esto es importante porque una ejecución
    detenida por el límite no debe interpretarse
    igual que una búsqueda que terminó normalmente.

    Retorna:
        DataFrame con el número de ejecuciones
        exitosas y limitadas para cada algoritmo.
    """

    resultados = []

    print()
    print("EJECUCIONES QUE ALCANZARON EL LÍMITE")
    print()

    for algoritmo in [
        "BFS",
        "DFS"
    ]:

        datos_algoritmo = datos[
            datos["algoritmo"] == algoritmo
        ]

        limite = datos_algoritmo[
            datos_algoritmo["limite_alcanzado"] == True
        ]

        exitosas = datos_algoritmo[
            datos_algoritmo["limite_alcanzado"] == False
        ]

        total = len(
            datos_algoritmo
        )

        cantidad_limite = len(
            limite
        )

        cantidad_exitosas = len(
            exitosas
        )

        porcentaje_limite = (
            cantidad_limite
            / total
        ) * 100

        print(
            f"{algoritmo}:"
        )

        print(
            f"  Ejecuciones totales: "
            f"{total}"
        )

        print(
            f"  Terminaron normalmente: "
            f"{cantidad_exitosas}"
        )

        print(
            f"  Alcanzaron el límite: "
            f"{cantidad_limite}"
        )

        print(
            f"  Porcentaje con límite: "
            f"{porcentaje_limite:.2f}%"
        )

        print()

        resultados.append(
            {
                "algoritmo": algoritmo,
                "total": total,
                "exitosas": cantidad_exitosas,
                "limite": cantidad_limite,
                "porcentaje_limite":
                    porcentaje_limite
            }
        )

    return pd.DataFrame(
        resultados
    )


def generar_resumen_exitosas(datos):
    """
    Calcula las estadísticas únicamente sobre
    las ejecuciones que terminaron normalmente.

    De esta manera se puede distinguir:

        1. El comportamiento global del algoritmo.
        2. El comportamiento cuando realmente
           logra completar la búsqueda sin alcanzar
           el límite experimental.
    """

    exitosas = datos[
        datos["limite_alcanzado"] == False
    ].copy()

    resumen = (
        exitosas
        .groupby(
            "algoritmo"
        )
        .agg(
            cantidad_ejecuciones=(
                "simulacion",
                "count"
            ),

            tiempo_promedio=(
                "tiempo",
                "mean"
            ),

            tiempo_mediana=(
                "tiempo",
                "median"
            ),

            memoria_promedio=(
                "memoria_kb",
                "mean"
            ),

            memoria_mediana=(
                "memoria_kb",
                "median"
            ),

            nodos_promedio=(
                "nodos",
                "mean"
            ),

            movimientos_promedio=(
                "movimientos",
                "mean"
            ),

            profundidad_promedio=(
                "profundidad",
                "mean"
            )
        )
        .reset_index()
    )

    return resumen


def mostrar_resumen(resumen):
    """
    Muestra en consola las estadísticas
    obtenidas utilizando todas las simulaciones.
    """

    print()
    print(
        "RESUMEN ESTADÍSTICO GLOBAL "
        "PUZZLE 3x3"
    )

    for _, fila in resumen.iterrows():

        print()
        print(
            fila["algoritmo"]
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
            f"Tiempo mínimo: "
            f"{fila['tiempo_minimo']:.8f} s"
        )

        print(
            f"Tiempo máximo: "
            f"{fila['tiempo_maximo']:.8f} s"
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
            f"Memoria mínima: "
            f"{fila['memoria_minima']:.4f} KB"
        )

        print(
            f"Memoria máxima: "
            f"{fila['memoria_maxima']:.4f} KB"
        )

        print(
            f"Nodos promedio: "
            f"{fila['nodos_promedio']:.2f}"
        )

        print(
            f"Movimientos promedio: "
            f"{fila['movimientos_promedio']:.2f}"
        )

        print(
            f"Profundidad promedio: "
            f"{fila['profundidad_promedio']:.2f}"
        )


def mostrar_comparacion(comparacion):
    """
    Presenta de manera legible la comparación
    global entre BFS y DFS.
    """

    print()
    print("COMPARACIÓN GLOBAL BFS VS DFS")
    print()

    print(
        f"BFS utilizó aproximadamente "
        f"{comparacion['porcentaje_menos_tiempo_bfs']:.2f}% "
        f"menos tiempo que DFS."
    )

    print(
        f"BFS utilizó aproximadamente "
        f"{comparacion['porcentaje_menos_memoria_bfs']:.2f}% "
        f"menos memoria que DFS."
    )

    print(
        f"DFS tardó aproximadamente "
        f"{comparacion['veces_tiempo_dfs']:.2f} "
        f"veces lo que tardó BFS."
    )

    print(
        f"DFS utilizó aproximadamente "
        f"{comparacion['veces_memoria_dfs']:.2f} "
        f"veces la memoria utilizada por BFS."
    )


def mostrar_resumen_exitosas(
    resumen_exitosas
):
    """
    Muestra las estadísticas correspondientes
    únicamente a las ejecuciones que no alcanzaron
    el límite máximo de nodos.
    """

    print()
    print(
        "RESUMEN DE EJECUCIONES "
        "QUE TERMINARON NORMALMENTE"
    )

    for _, fila in resumen_exitosas.iterrows():

        print()
        print(
            fila["algoritmo"]
        )

        print(
            f"Cantidad de ejecuciones: "
            f"{int(fila['cantidad_ejecuciones'])}"
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

        print(
            f"Movimientos promedio: "
            f"{fila['movimientos_promedio']:.2f}"
        )

        print(
            f"Profundidad promedio: "
            f"{fila['profundidad_promedio']:.2f}"
        )


def guardar_resultados_analisis(
    resumen,
    resumen_exitosas,
    resumen_limites
):
    """
    Guarda los resultados estadísticos
    en archivos CSV.
    """

    os.makedirs(
        "resultados",
        exist_ok=True
    )

    resumen.to_csv(
        "resultados/resumen_puzzle.csv",
        index=False
    )

    resumen_exitosas.to_csv(
        "resultados/resumen_puzzle_exitosas.csv",
        index=False
    )

    resumen_limites.to_csv(
        "resultados/limites_puzzle.csv",
        index=False
    )


if __name__ == "__main__":

    # Carga los resultados de las 100 simulaciones.
    datos = cargar_datos()

    # Calcula el resumen utilizando
    # todas las ejecuciones.
    resumen = generar_resumen(
        datos
    )

    # Compara BFS y DFS globalmente.
    comparacion = comparar_algoritmos(
        resumen
    )

    # Analiza cuántas ejecuciones llegaron
    # al límite experimental.
    resumen_limites = analizar_limites(
        datos
    )

    # Calcula estadísticas únicamente
    # de las ejecuciones normales.
    resumen_exitosas = (
        generar_resumen_exitosas(
            datos
        )
    )

    # Muestra los resultados.
    mostrar_resumen(
        resumen
    )

    mostrar_comparacion(
        comparacion
    )

    mostrar_resumen_exitosas(
        resumen_exitosas
    )

    # Guarda los resultados estadísticos.
    guardar_resultados_analisis(
        resumen,
        resumen_exitosas,
        resumen_limites
    )

    print()
    print(
        "Archivos generados:"
    )

    print(
        "resultados/resumen_puzzle.csv"
    )

    print(
        "resultados/resumen_puzzle_exitosas.csv"
    )

    print(
        "resultados/limites_puzzle.csv"
    )