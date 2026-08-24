import matplotlib.pyplot as plt
import numpy as np
from n_reinas import tablero_a_matriz


def mostrar_tablero(solucion, titulo="Tablero N-Reinas", guardar_como=None):
    """
    Muestra visualmente la solución del problema N-Reinas.

    Parámetros:
        solucion: lista donde solucion[c] = fila de la reina en columna c.
        titulo: título que se mostrará en la gráfica.
        guardar_como: ruta opcional para guardar la imagen en lugar de mostrarla.
    """
    if solucion is None:
        print("No hay solución para mostrar.")
        return

    n = len(solucion)
    matriz = tablero_a_matriz(solucion)

    fig, ax = plt.subplots(figsize=(8, 8))

    tablero_colors = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                tablero_colors[i, j] = [0.9, 0.9, 0.9]
            else:
                tablero_colors[i, j] = [0.3, 0.3, 0.3]

    ax.imshow(tablero_colors, extent=[0, n, 0, n], origin='lower')

    for fila in range(n):
        for col in range(n):
            if matriz[fila][col] == 1:
                circle = plt.Circle(
                    (col + 0.5, n - fila - 0.5),
                    0.4,
                    color='red',
                    zorder=10
                )
                ax.add_patch(circle)
                ax.text(
                    col + 0.5, n - fila - 0.5, '♛',
                    ha='center', va='center',
                    fontsize=24, color='white', zorder=11
                )

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([chr(ord('a') + i) for i in range(n)])
    ax.set_yticklabels([str(n - i) for i in range(n)])
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, color='black', linewidth=1.5)

    plt.tight_layout()

    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        print(f"Tablero guardado en: {guardar_como}")
        plt.close()
    else:
        plt.show()


def mostrar_comparacion(solucion_dfs, solucion_bfs, n, guardar_como=None):
    """
    Muestra lado a lado las soluciones encontradas por DFS y BFS.

    Parámetros:
        solucion_dfs: solución encontrada por DFS.
        solucion_bfs: solución encontrada por BFS.
        n: tamaño del tablero.
        guardar_como: ruta opcional para guardar la imagen.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    for ax, solucion, titulo in [(ax1, solucion_dfs, "DFS"), (ax2, solucion_bfs, "BFS")]:
        if solucion is None:
            ax.text(0.5, 0.5, 'Sin solución', ha='center', va='center', fontsize=16)
            ax.set_title(f"{titulo} - {n} Reinas")
            continue

        matriz = tablero_a_matriz(solucion)
        tablero_colors = np.zeros((n, n, 3))
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 0:
                    tablero_colors[i, j] = [0.9, 0.9, 0.9]
                else:
                    tablero_colors[i, j] = [0.3, 0.3, 0.3]

        ax.imshow(tablero_colors, extent=[0, n, 0, n], origin='lower')

        for fila in range(n):
            for col in range(n):
                if matriz[fila][col] == 1:
                    circle = plt.Circle(
                        (col + 0.5, n - fila - 0.5),
                        0.4,
                        color='red',
                        zorder=10
                    )
                    ax.add_patch(circle)
                    ax.text(
                        col + 0.5, n - fila - 0.5, '♛',
                        ha='center', va='center',
                        fontsize=24, color='white', zorder=11
                    )

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels([chr(ord('a') + i) for i in range(n)])
        ax.set_yticklabels([str(n - i) for i in range(n)])
        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_aspect('equal')
        ax.set_title(f"{titulo} - {n} Reinas", fontsize=14, fontweight='bold', pad=15)
        ax.grid(True, color='black', linewidth=1.5)

    plt.tight_layout()

    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        print(f"Comparación guardada en: {guardar_como}")
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    solucion = [1, 3, 0, 2]
    mostrar_tablero(solucion, "DFS - 4 Reinas")