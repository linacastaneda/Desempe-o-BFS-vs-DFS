from pathlib import Path

import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_DATOS = RAIZ_PROYECTO / "resultados" / "nreinas" / "datos"


def cargar_datos(
    archivo=None
):
    """
    Carga los resultados obtenidos en las ejecuciones de N-Reinas.

    Si no se indica una ruta, utiliza el archivo estándar del proyecto.
    """

    ruta = (
        Path(archivo)
        if archivo is not None
        else CARPETA_DATOS / "resultados.csv"
    )

    return pd.read_csv(ruta)


def generar_resumen(datos):
    """
    Calcula estadísticas descriptivas para BFS y DFS según N.

    Se incluyen:
        - Tiempo: promedio, mediana, mínimo, máximo y desviación estándar.
        - Memoria pico: promedio, mediana, mínimo, máximo y desviación estándar.
        - Nodos explorados: promedio y mediana.
        - Cantidad de repeticiones disponibles para cada N y algoritmo.
    """

    resumen = (
        datos
        .groupby(["n", "algoritmo"])
        .agg(
            repeticiones=("simulacion", "count"),
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
            nodos_promedio=("nodos", "mean"),
            nodos_mediana=("nodos", "median"),
        )
        .reset_index()
    )

    return resumen


def comparar_algoritmos(resumen):
    """
    Compara BFS y DFS para cada valor de N.

    Los porcentajes indican cuánto mayor es el promedio de BFS
    respecto al promedio de DFS en tiempo, memoria y nodos.
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
        on="n",
        suffixes=("_bfs", "_dfs"),
    )

    comparacion["ratio_tiempo_bfs_dfs"] = (
        comparacion["tiempo_promedio_bfs"]
        / comparacion["tiempo_promedio_dfs"]
    )

    comparacion["ratio_memoria_bfs_dfs"] = (
        comparacion["memoria_promedio_bfs"]
        / comparacion["memoria_promedio_dfs"]
    )

    comparacion["ratio_nodos_bfs_dfs"] = (
        comparacion["nodos_promedio_bfs"]
        / comparacion["nodos_promedio_dfs"]
    )

    comparacion["diferencia_tiempo_porcentaje"] = (
        comparacion["ratio_tiempo_bfs_dfs"] - 1
    ) * 100

    comparacion["diferencia_memoria_porcentaje"] = (
        comparacion["ratio_memoria_bfs_dfs"] - 1
    ) * 100

    comparacion["diferencia_nodos_porcentaje"] = (
        comparacion["ratio_nodos_bfs_dfs"] - 1
    ) * 100

    return comparacion


def mostrar_resumen(resumen):
    """Muestra en consola las estadísticas principales."""

    print()
    print("RESUMEN ESTADÍSTICO - N-REINAS")
    print("=" * 65)

    for _, fila in resumen.iterrows():

        print(
            f"\nN = {int(fila['n'])} - {fila['algoritmo']} "
            f"({int(fila['repeticiones'])} repeticiones)"
        )

        print(
            f"  Tiempo:  prom={fila['tiempo_promedio']:.6f}s  "
            f"med={fila['tiempo_mediana']:.6f}s  "
            f"std={fila['tiempo_desviacion']:.6f}"
        )

        print(
            f"  Memoria: prom={fila['memoria_promedio']:.2f}KB  "
            f"med={fila['memoria_mediana']:.2f}KB  "
            f"std={fila['memoria_desviacion']:.2f}"
        )

        print(
            f"  Nodos:   prom={fila['nodos_promedio']:.0f}  "
            f"med={fila['nodos_mediana']:.0f}"
        )


def mostrar_comparacion(comparacion):
    """Muestra ratios y diferencias entre BFS y DFS."""

    print()
    print("COMPARACIÓN BFS VS DFS - N-REINAS")
    print("=" * 65)

    for _, fila in comparacion.iterrows():

        print(f"\nN = {int(fila['n'])}")

        print(
            f"  Tiempo:  BFS/DFS = "
            f"{fila['ratio_tiempo_bfs_dfs']:.2f}x"
        )

        print(
            f"  Memoria: BFS/DFS = "
            f"{fila['ratio_memoria_bfs_dfs']:.2f}x"
        )

        print(
            f"  Nodos:   BFS/DFS = "
            f"{fila['ratio_nodos_bfs_dfs']:.2f}x"
        )


def mostrar_complejidad_teorica():
    """
    Presenta una interpretación teórica prudente del comportamiento esperado.

    La comparación experimental del proyecto no depende de asignar una única
    fórmula Big-O exacta a toda la implementación. El factor de ramificación
    disminuye por las restricciones del problema y el criterio de terminación
    es encontrar la primera solución.
    """

    print()
    print("INTERPRETACIÓN TEÓRICA - N-REINAS")
    print("=" * 65)
    print()
    print("Cada nivel corresponde a colocar una reina en una nueva columna.")
    print("Las posiciones inválidas se descartan al generar sucesores.")
    print()
    print("BFS:")
    print("  - Explora todos los estados de niveles anteriores antes de profundizar.")
    print("  - Puede mantener una frontera muy grande en memoria.")
    print("  - Para hallar una primera solución completa debe alcanzar el nivel N.")
    print()
    print("DFS:")
    print("  - Profundiza una rama válida antes de regresar a otras alternativas.")
    print("  - Suele mantener una frontera mucho menor que BFS.")
    print("  - En estas implementaciones encuentra la primera solución con pocos nodos.")
    print()
    print(
        "El costo exacto depende del orden de generación, la poda por posiciones "
        "inválidas y el criterio de detenerse en la primera solución."
    )


def exportar_resumenes(
    resumen,
    comparacion,
    carpeta=CARPETA_DATOS,
):
    """Exporta el resumen y la comparación a CSV."""

    carpeta = Path(carpeta)

    carpeta.mkdir(
        parents=True,
        exist_ok=True,
    )

    resumen.to_csv(
        carpeta / "resumen.csv",
        index=False,
    )

    comparacion.to_csv(
        carpeta / "comparacion.csv",
        index=False,
    )

    print(f"\nArchivos de análisis guardados en: {carpeta}")


if __name__ == "__main__":

    datos = cargar_datos()

    resumen = generar_resumen(datos)

    comparacion = comparar_algoritmos(resumen)

    mostrar_resumen(resumen)

    mostrar_comparacion(comparacion)

    mostrar_complejidad_teorica()

    exportar_resumenes(
        resumen,
        comparacion,
    )
