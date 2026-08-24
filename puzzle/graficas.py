"""
Gráficas comparativas BFS vs DFS para Puzzle 3x3.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def graficar(archivo="resultados_puzzle.csv", carpeta="graficas_puzzle"):
    """Genera gráficas de nodos, tiempo y profundidad."""
    df = pd.read_csv(archivo)
    carpeta = Path(carpeta)
    carpeta.mkdir(exist_ok=True)

    metricas = [
        ("nodos", "Nodos explorados", "nodos_explorados.png"),
        ("tiempo", "Tiempo de ejecución (segundos)", "tiempo_ejecucion.png"),
        ("profundidad", "Profundidad de la solución", "profundidad.png"),
    ]

    for columna, etiqueta_y, nombre in metricas:
        plt.figure(figsize=(9, 5))

        for algoritmo in ("BFS", "DFS"):
            datos = df[df["algoritmo"] == algoritmo]
            promedio = datos.groupby("simulacion")[columna].mean()
            plt.plot(
                promedio.index,
                promedio.values,
                label=algoritmo,
                marker=".",
            )

        plt.title(f"BFS vs DFS - {etiqueta_y}")
        plt.xlabel("Simulación")
        plt.ylabel(etiqueta_y)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(carpeta / nombre, dpi=150)
        plt.show()


if __name__ == "__main__":
    graficar()
