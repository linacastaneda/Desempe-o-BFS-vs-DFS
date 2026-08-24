import pandas as pd
import os


def cargar_datos():
    """
    Carga los resultados obtenidos en las simulaciones de N-Reinas.
    """
    ruta = os.path.join("..", "resultados", "nreinas", "datos", "resultados.csv")
    datos = pd.read_csv(ruta)
    return datos


def generar_resumen(datos):
    """
    Calcula estadísticas descriptivas para BFS y DFS según N.

    Se analizan:
        - Tiempo de ejecución (promedio, mediana, min, max, std).
        - Memoria pico (promedio, mediana, min, max, std).
        - Nodos explorados (promedio).
    """
    resumen = (
        datos
        .groupby(["n", "algoritmo"])
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

            nodos_promedio=("nodos", "mean"),
            nodos_mediana=("nodos", "median")
        )
        .reset_index()
    )
    return resumen


def comparar_algoritmos(resumen):
    """
    Calcula la diferencia porcentual entre BFS y DFS
    para tiempo, memoria y nodos en cada tamaño del problema.
    """
    bfs = resumen[resumen["algoritmo"] == "BFS"].copy()
    dfs = resumen[resumen["algoritmo"] == "DFS"].copy()

    comparacion = pd.merge(bfs, dfs, on="n", suffixes=("_bfs", "_dfs"))

    comparacion["diferencia_tiempo_porcentaje"] = (
        (comparacion["tiempo_promedio_bfs"] - comparacion["tiempo_promedio_dfs"])
        / comparacion["tiempo_promedio_dfs"]
    ) * 100

    comparacion["diferencia_memoria_porcentaje"] = (
        (comparacion["memoria_promedio_bfs"] - comparacion["memoria_promedio_dfs"])
        / comparacion["memoria_promedio_dfs"]
    ) * 100

    comparacion["diferencia_nodos_porcentaje"] = (
        (comparacion["nodos_promedio_bfs"] - comparacion["nodos_promedio_dfs"])
        / comparacion["nodos_promedio_dfs"]
    ) * 100

    return comparacion


def mostrar_resumen(resumen):
    """
    Muestra en consola las estadísticas principales de BFS y DFS.
    """
    print()
    print("RESUMEN ESTADÍSTICO - N-REINAS (100 simulaciones)")
    print("=" * 65)

    for _, fila in resumen.iterrows():
        n = int(fila['n'])
        alg = fila['algoritmo']
        print(f"\nN = {n} - {alg}")
        print(f"  Tiempo:  prom={fila['tiempo_promedio']:.6f}s  "
              f"med={fila['tiempo_mediana']:.6f}s  "
              f"std={fila['tiempo_desviacion']:.6f}")
        print(f"  Memoria: prom={fila['memoria_promedio']:.2f}KB  "
              f"med={fila['memoria_mediana']:.2f}KB  "
              f"std={fila['memoria_desviacion']:.2f}")
        print(f"  Nodos:   prom={fila['nodos_promedio']:.0f}  "
              f"med={fila['nodos_mediana']:.0f}")


def mostrar_comparacion(comparacion):
    """
    Muestra la diferencia porcentual entre BFS y DFS.
    """
    print()
    print("COMPARACIÓN BFS vs DFS - N-REINAS")
    print("=" * 65)

    for _, fila in comparacion.iterrows():
        n = int(fila["n"])
        print(f"\nN = {n}")
        dt = fila["diferencia_tiempo_porcentaje"]
        dm = fila["diferencia_memoria_porcentaje"]
        dn = fila["diferencia_nodos_porcentaje"]
        print(f"  Tiempo:  BFS {'usa' if dt > 0 else 'ahorra'} {abs(dt):.2f}% "
              f"{'más' if dt > 0 else 'menos'} que DFS")
        print(f"  Memoria: BFS {'usa' if dm > 0 else 'ahorra'} {abs(dm):.2f}% "
              f"{'más' if dm > 0 else 'menos'} que DFS")
        print(f"  Nodos:   BFS {'explora' if dn > 0 else 'explora'} {abs(dn):.2f}% "
              f"{'más' if dn > 0 else 'menos'} que DFS")


def analisis_big_o():
    """
    Explica la complejidad teórica esperada para N-Reinas con BFS y DFS.
    """
    print()
    print("ANÁLISIS DE COMPLEJIDAD (Big-O) - N-REINAS")
    print("=" * 65)
    print()
    print("PROBLEMA: Colocar N reinas en tablero N×N sin que se ataquen.")
    print("REPRESENTACIÓN: tablero = [fila_reina_col_0, fila_reina_col_1, ...]")
    print("ESTADOS: Cada nivel = una columna. Máximo N reinas.")
    print()
    print("DFS (Backtracking):")
    print("  - Tiempo: O(N!) en peor caso (explora todo el árbol)")
    print("  - Espacio: O(N) (profundidad máxima del stack)")
    print("  - Ventaja: Encuentra primera solución rápido, poca memoria")
    print()
    print("BFS:")
    print("  - Tiempo: O(N!) en peor caso (explora todo el árbol)")
    print("  - Espacio: O(N!) en peor caso (cola guarda nivel completo)")
    print("  - Desventaja: Memoria explota exponencialmente")
    print()
    print("EXPERIMENTALMENTE (100 simulaciones):")
    print("  - DFS: Tiempo crece moderadamente, memoria constante ~O(N)")
    print("  - BFS: Tiempo similar, pero memoria crece exponencial")
    print("  - Nodos: BFS explora más nodos (nivel por nivel)")
    print("  - BFS encuentra solución más 'corta' (menos profundidad)")


if __name__ == "__main__":
    datos = cargar_datos()
    resumen = generar_resumen(datos)
    comparacion = comparar_algoritmos(resumen)

    mostrar_resumen(resumen)
    mostrar_comparacion(comparacion)
    analisis_big_o()

    carpeta = os.path.join("..", "resultados", "nreinas", "datos")
    os.makedirs(carpeta, exist_ok=True)

    resumen.to_csv(
        os.path.join(carpeta, "resumen.csv"),
        index=False
    )
    comparacion.to_csv(
        os.path.join(carpeta, "comparacion.csv"),
        index=False
    )

    print("\nArchivos de análisis guardados correctamente.")


def exportar_resumenes(resumen, comparacion, carpeta="../resultados/nreinas/datos"):
    """
    Exporta resumen y comparación a CSV con nombres estándar.
    """
    carpeta = os.path.join("..", "resultados", "nreinas", "datos")
    os.makedirs(carpeta, exist_ok=True)

    resumen.to_csv(
        os.path.join(carpeta, "resumen.csv"),
        index=False
    )
    comparacion.to_csv(
        os.path.join(carpeta, "comparacion.csv"),
        index=False
    )
    print(f"\nArchivos de análisis guardados en resultados/nreinas/datos/")