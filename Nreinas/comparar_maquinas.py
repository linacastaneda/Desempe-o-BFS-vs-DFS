import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from graficas import cargar_resultados, calcular_promedios


def cargar_todos_resultados(carpeta_base="../resultados/nreinas/datos"):
    """
    Carga todos los archivos resultados_nreinas.csv que encuentra en subcarpetas
    o con sufijos de máquina (ej: resultados_nreinas_pc1.csv, resultados_nreinas_laptop.csv).
    
    Retorna:
        DataFrame combinado con columna 'fuente' indicando el archivo origen.
    """
    datos_lista = []
    
    # Buscar archivos CSV de resultados
    for archivo in os.listdir(carpeta_base):
        if archivo.startswith("resultados_nreinas") and archivo.endswith(".csv"):
            ruta = os.path.join(carpeta_base, archivo)
            try:
                df = pd.read_csv(ruta)
                fuente = archivo.replace("resultados_nreinas_", "").replace(".csv", "")
                if fuente == "resultados_nreinas" or fuente == "":
                    fuente = "default"
                df["fuente"] = fuente
                datos_lista.append(df)
                print(f"Cargado: {archivo} ({len(df)} filas)")
            except Exception as e:
                print(f"Error cargando {archivo}: {e}")
    
    if not datos_lista:
        print("No se encontraron archivos de resultados.")
        return None
    
    return pd.concat(datos_lista, ignore_index=True)


def comparar_maquinas(datos):
    """
    Compara los resultados entre diferentes máquinas.
    """
    if "fuente" not in datos.columns:
        print("Los datos no tienen información de fuente/máquina.")
        return
    
    maquinas = datos["fuente"].unique()
    print(f"\nMáquinas encontradas: {list(maquinas)}")
    
    # Promedios por máquina, N y algoritmo
    promedios = (
        datos
        .groupby(["fuente", "n", "algoritmo"], as_index=False)
        .agg(
            tiempo_promedio=("tiempo", "mean"),
            memoria_promedio=("memoria_kb", "mean"),
            nodos_promedio=("nodos", "mean")
        )
    )
    
    return promedios


def grafica_comparativa_tiempo_maquinas(promedios, guardar_como=None):
    """
    Gráfica de líneas: tiempo vs N, una línea por máquina y algoritmo.
    """
    maquinas = sorted(promedios["fuente"].unique())
    ns = sorted(promedios["n"].unique())
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(maquinas)))
    
    for idx_alg, (algoritmo, ax) in enumerate([("BFS", axes[0]), ("DFS", axes[1])]):
        datos_alg = promedios[promedios["algoritmo"] == algoritmo]
        
        for idx_maq, maquina in enumerate(maquinas):
            datos_maq = datos_alg[datos_alg["fuente"] == maquina]
            if len(datos_maq) == 0:
                continue
            ax.plot(
                datos_maq["n"], datos_maq["tiempo_promedio"],
                marker="o", label=maquina, linewidth=2, markersize=6,
                color=colors[idx_maq]
            )
        
        ax.set_xlabel("Tamaño del tablero (N)", fontsize=11)
        ax.set_ylabel("Tiempo promedio (segundos)", fontsize=11)
        ax.set_title(f"{algoritmo} - Tiempo por máquina", fontsize=12, fontweight='bold')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=9)
        ax.set_xticks(ns)
    
    plt.suptitle("Comparación de tiempo entre máquinas (100 simulaciones)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def grafica_comparativa_memoria_maquinas(promedios, guardar_como=None):
    """
    Gráfica de líneas: memoria vs N, una línea por máquina y algoritmo.
    """
    maquinas = sorted(promedios["fuente"].unique())
    ns = sorted(promedios["n"].unique())
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(maquinas)))
    
    for idx_alg, (algoritmo, ax) in enumerate([("BFS", axes[0]), ("DFS", axes[1])]):
        datos_alg = promedios[promedios["algoritmo"] == algoritmo]
        
        for idx_maq, maquina in enumerate(maquinas):
            datos_maq = datos_alg[datos_alg["fuente"] == maquina]
            if len(datos_maq) == 0:
                continue
            ax.plot(
                datos_maq["n"], datos_maq["memoria_promedio"],
                marker="s", label=maquina, linewidth=2, markersize=6,
                color=colors[idx_maq]
            )
        
        ax.set_xlabel("Tamaño del tablero (N)", fontsize=11)
        ax.set_ylabel("Memoria promedio (KB)", fontsize=11)
        ax.set_title(f"{algoritmo} - Memoria por máquina", fontsize=12, fontweight='bold')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=9)
        ax.set_xticks(ns)
    
    plt.suptitle("Comparación de memoria entre máquinas (100 simulaciones)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def grafica_speedup_maquinas(promedios, guardar_como=None):
    """
    Gráfica de speedup: tiempo_DFS / tiempo_BFS por máquina.
    Valores > 1 significa DFS más rápido.
    """
    maquinas = sorted(promedios["fuente"].unique())
    ns = sorted(promedios["n"].unique())
    
    plt.figure(figsize=(10, 6))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(maquinas)))
    
    for idx_maq, maquina in enumerate(maquinas):
        datos_maq = promedios[promedios["fuente"] == maquina]
        bfs = datos_maq[datos_maq["algoritmo"] == "BFS"].set_index("n")
        dfs = datos_maq[datos_maq["algoritmo"] == "DFS"].set_index("n")
        
        # Speedup = tiempo_BFS / tiempo_DFS (cuántas veces más rápido es DFS)
        speedup = bfs["tiempo_promedio"] / dfs["tiempo_promedio"]
        
        plt.plot(
            speedup.index, speedup.values,
            marker="o", label=maquina, linewidth=2, markersize=8,
            color=colors[idx_maq]
        )
    
    plt.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='Igual rendimiento')
    plt.xlabel("Tamaño del tablero (N)", fontsize=12)
    plt.ylabel("Speedup (tiempo_BFS / tiempo_DFS)", fontsize=12)
    plt.title("Speedup de DFS sobre BFS por máquina\n(>1 = DFS más rápido)", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.yscale('log')
    plt.xticks(ns)
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def tabla_resumen_maquinas(promedios):
    """
    Muestra tabla comparativa en consola.
    """
    maquinas = sorted(promedios["fuente"].unique())
    
    print("\n" + "=" * 80)
    print("TABLA RESUMEN: TIEMPO PROMEDIO (segundos) POR MÁQUINA, N Y ALGORITMO")
    print("=" * 80)
    
    for maquina in maquinas:
        print(f"\n--- {maquina} ---")
        datos_maq = promedios[promedios["fuente"] == maquina]
        for alg in ["BFS", "DFS"]:
            datos_alg = datos_maq[datos_maq["algoritmo"] == alg]
            print(f"  {alg}:")
            for _, row in datos_alg.iterrows():
                print(f"    N={int(row['n'])}: {row['tiempo_promedio']:.6f}s  "
                      f"({row['memoria_promedio']:.1f}KB, {row['nodos_promedio']:.0f} nodos)")


def exportar_comparacion_csv(promedios, carpeta_salida="../resultados/nreinas/datos"):
    """
    Exporta la comparación entre máquinas a CSV.
    """
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Pivot table para fácil lectura
    pivot_tiempo = promedios.pivot_table(
        index=["fuente", "n"], columns="algoritmo", values="tiempo_promedio"
    ).reset_index()
    pivot_tiempo.columns.name = None
    
    pivot_memoria = promedios.pivot_table(
        index=["fuente", "n"], columns="algoritmo", values="memoria_promedio"
    ).reset_index()
    pivot_memoria.columns.name = None
    
    pivot_nodos = promedios.pivot_table(
        index=["fuente", "n"], columns="algoritmo", values="nodos_promedio"
    ).reset_index()
    pivot_nodos.columns.name = None
    
    pivot_tiempo.to_csv(
        os.path.join(carpeta_salida, "comparacion_maquinas_tiempo.csv"),
        index=False
    )
    pivot_memoria.to_csv(
        os.path.join(carpeta_salida, "comparacion_maquinas_memoria.csv"),
        index=False
    )
    pivot_nodos.to_csv(
        os.path.join(carpeta_salida, "comparacion_maquinas_nodos.csv"),
        index=False
    )
    
    print(f"\nArchivos de comparación exportados a {carpeta_salida}/")


def main():
    print("=" * 60)
    print("COMPARACIÓN MULTI-MÁQUINA: N-REINAS BFS vs DFS")
    print("=" * 60)
    
    datos = cargar_todos_resultados()
    if datos is None:
        return
    
    promedios = comparar_maquinas(datos)
    if promedios is None:
        return
    
    tabla_resumen_maquinas(promedios)
    exportar_comparacion_csv(promedios)
    
    print("\nGenerando gráficas comparativas...")
    grafica_comparativa_tiempo_maquinas(promedios)
    grafica_comparativa_memoria_maquinas(promedios)
    grafica_speedup_maquinas(promedios)
    
    print("\n¡Comparación multi-máquina completada!")


if __name__ == "__main__":
    main()