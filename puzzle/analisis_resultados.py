"""
Análisis de resultados del Puzzle 3x3.
"""

import pandas as pd


def analizar(archivo="resultados_puzzle.csv"):
    """Calcula promedios de BFS y DFS."""
    df = pd.read_csv(archivo)

    columnas = ["nodos", "tiempo", "movimientos", "profundidad"]

    resumen = (
        df.groupby("algoritmo")[columnas]
        .mean()
        .round(6)
    )

    print("=== ANÁLISIS PUZZLE 3x3 ===")
    print("\nPromedios:")
    print(resumen)

    print("\nInterpretación:")
    print(
        "BFS explora el problema por niveles, mientras que DFS "
        "profundiza en un camino antes de regresar. "
        "BFS normalmente encuentra una solución con menor cantidad "
        "de movimientos, mientras que DFS puede encontrar otra ruta."
    )

    print(
        "\nLa comparación debe considerar el tiempo de ejecución, "
        "los nodos explorados y la profundidad de las soluciones."
    )

    resumen.to_csv("resumen_puzzle.csv")
    return resumen


if __name__ == "__main__":
    analizar()
