import os
import platform
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def obtener_info_maquina():
    """
    Obtiene información del hardware y software del equipo actual.
    En Windows usa WMI para obtener el nombre real del CPU (ej: AMD Ryzen 7 7445HS).
    """
    import sys
    import subprocess
    
    def get_cpu_name():
        """Obtiene el nombre real del procesador."""
        try:
            if platform.system() == "Windows":
                # Usar PowerShell (WMIC está deprecado en Windows 11/Server 2025)
                result = subprocess.run(
                    ["powershell", "-Command", 
                     "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"],
                    capture_output=True, text=True, timeout=10
                )
                name = result.stdout.strip()
                if name:
                    return name
            elif platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("model name"):
                            return line.split(":")[1].strip()
            elif platform.system() == "Darwin":
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True, text=True, timeout=5
                )
                return result.stdout.strip()
        except Exception:
            pass
        return platform.processor()
    
    cpu_name = get_cpu_name()
    
    info = {
        "hostname": platform.node(),
        "sistema": platform.system(),
        "version_sistema": platform.version(),
        "arquitectura": platform.machine(),
        "procesador": cpu_name,
        "python_version": sys.version.split()[0],
        "cpu_count": os.cpu_count(),
    }
    try:
        import psutil
        info["ram_total_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)
        freq = psutil.cpu_freq()
        info["cpu_freq_mhz"] = freq.current if freq else None
        info["cpu_freq_max_mhz"] = freq.max if freq else None
    except ImportError:
        info["ram_total_gb"] = None
        info["cpu_freq_mhz"] = None
        info["cpu_freq_max_mhz"] = None
    return info


def cargar_resultados():
    """
    Carga el archivo CSV generado por las simulaciones.

    Retorna:
        DataFrame de pandas con todos los resultados.
    """
    ruta = os.path.join("..", "resultados", "nreinas", "datos", "resultados.csv")
    datos = pd.read_csv(ruta)
    return datos


def calcular_promedios(datos):
    """
    Calcula los valores promedio de tiempo, memoria y nodos explorados.

    Los resultados se agrupan por:
        - Tamaño del tablero (N).
        - Algoritmo utilizado.

    Retorna:
        DataFrame con los promedios.
    """
    promedios = (
        datos
        .groupby(["n", "algoritmo"], as_index=False)
        .agg(
            tiempo_promedio=("tiempo", "mean"),
            memoria_promedio=("memoria_kb", "mean"),
            nodos_promedio=("nodos", "mean")
        )
    )
    return promedios


def grafica_barras_agrupadas(promedios, metrica, titulo, ylabel, guardar_como=None):
    """
    Gráfica de barras agrupadas: BFS vs DFS para cada N.
    Mucho mejor que líneas cuando las escalas son muy diferentes.
    """
    bfs = promedios[promedios["algoritmo"] == "BFS"].sort_values("n")
    dfs = promedios[promedios["algoritmo"] == "DFS"].sort_values("n")
    
    ns = sorted(promedios["n"].unique())
    x = np.arange(len(ns))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    # Barras BFS
    bars_bfs = ax.bar(x - width/2, 
                       bfs[metrica].values if len(bfs) == len(ns) else 
                       [bfs[bfs["n"]==n][metrica].values[0] if len(bfs[bfs["n"]==n]) > 0 else 0 for n in ns],
                       width, label='BFS', color='#3498db', alpha=0.85, edgecolor='#2980b9', linewidth=1)
    
    # Barras DFS
    bars_dfs = ax.bar(x + width/2,
                       dfs[metrica].values if len(dfs) == len(ns) else
                       [dfs[dfs["n"]==n][metrica].values[0] if len(dfs[dfs["n"]==n]) > 0 else 0 for n in ns],
                       width, label='DFS', color='#e74c3c', alpha=0.85, edgecolor='#c0392b', linewidth=1)
    
    # Valores encima de las barras
    for bar in bars_bfs:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height:.2e}' if height < 0.001 else f'{height:.4f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=45)
    
    for bar in bars_dfs:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height:.2e}' if height < 0.001 else f'{height:.4f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=45)
    
    ax.set_xlabel("Tamaño del tablero (N)", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"N={n}" for n in ns], fontsize=11)
    ax.legend(fontsize=11)
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def grafica_tiempo_por_n(promedios, guardar_como=None):
    """Barras agrupadas: tiempo promedio por N."""
    grafica_barras_agrupadas(
        promedios, "tiempo_promedio",
        "Tiempo promedio de ejecución según N (100 simulaciones)",
        "Tiempo promedio (segundos)",
        guardar_como
    )


def grafica_memoria_por_n(promedios, guardar_como=None):
    """Barras agrupadas: memoria promedio por N."""
    grafica_barras_agrupadas(
        promedios, "memoria_promedio",
        "Memoria promedio pico según N (100 simulaciones)",
        "Memoria promedio (KB)",
        guardar_como
    )


def grafica_nodos_por_n(promedios, guardar_como=None):
    """Barras agrupadas: nodos explorados promedio por N."""
    grafica_barras_agrupadas(
        promedios, "nodos_promedio",
        "Nodos explorados promedio según N (100 simulaciones)",
        "Nodos explorados promedio",
        guardar_como
    )


def grafica_subplots_escalas_separadas(promedios, metrica, titulo, ylabel, guardar_como=None):
    """
    Dos subplots: uno para BFS, uno para DFS, cada uno con su propia escala.
    Permite ver el comportamiento de ambos algoritmos claramente.
    """
    bfs = promedios[promedios["algoritmo"] == "BFS"].sort_values("n")
    dfs = promedios[promedios["algoritmo"] == "DFS"].sort_values("n")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharex=True)
    
    # BFS subplot
    ax1.plot(bfs["n"], bfs[metrica], marker='o', linewidth=2.5, markersize=8,
             color='#3498db', label='BFS')
    ax1.fill_between(bfs["n"], bfs[metrica], alpha=0.15, color='#3498db')
    ax1.set_ylabel(ylabel, fontsize=11)
    ax1.set_title("BFS", fontsize=12, fontweight='bold', color='#2980b9')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(fontsize=10)
    
    # DFS subplot
    ax2.plot(dfs["n"], dfs[metrica], marker='s', linewidth=2.5, markersize=8,
             color='#e74c3c', label='DFS')
    ax2.fill_between(dfs["n"], dfs[metrica], alpha=0.15, color='#e74c3c')
    ax2.set_ylabel(ylabel, fontsize=11)
    ax2.set_title("DFS", fontsize=12, fontweight='bold', color='#c0392b')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(fontsize=10)
    
    for ax in [ax1, ax2]:
        ax.set_xlabel("Tamaño del tablero (N)", fontsize=11)
        ax.set_xticks(sorted(promedios["n"].unique()))
    
    plt.suptitle(titulo, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def grafica_tiempo_subplots(promedios, guardar_como=None):
    """Subplots con escalas separadas para tiempo."""
    grafica_subplots_escalas_separadas(
        promedios, "tiempo_promedio",
        "Tiempo promedio: BFS vs DFS (escalas independientes)",
        "Tiempo (segundos)",
        guardar_como
    )


def grafica_memoria_subplots(promedios, guardar_como=None):
    """Subplots con escalas separadas para memoria."""
    grafica_subplots_escalas_separadas(
        promedios, "memoria_promedio",
        "Memoria promedio: BFS vs DFS (escalas independientes)",
        "Memoria (KB)",
        guardar_como
    )


def grafica_nodos_subplots(promedios, guardar_como=None):
    """Subplots con escalas separadas para nodos."""
    grafica_subplots_escalas_separadas(
        promedios, "nodos_promedio",
        "Nodos explorados: BFS vs DFS (escalas independientes)",
        "Nodos explorados",
        guardar_como
    )


def grafica_ratio_bfs_dfs(promedios, guardar_como=None):
    """
    Gráfica de ratio BFS/DFS: cuántas veces más lento/más memoria usa BFS.
    Esta es la MÁS IMPORTANTE para la comparación.
    """
    bfs = promedios[promedios["algoritmo"] == "BFS"].set_index("n").sort_index()
    dfs = promedios[promedios["algoritmo"] == "DFS"].set_index("n").sort_index()
    
    ns = sorted(promedios["n"].unique())
    
    ratio_tiempo = bfs.loc[ns, "tiempo_promedio"] / dfs.loc[ns, "tiempo_promedio"]
    ratio_memoria = bfs.loc[ns, "memoria_promedio"] / dfs.loc[ns, "memoria_promedio"]
    ratio_nodos = bfs.loc[ns, "nodos_promedio"] / dfs.loc[ns, "nodos_promedio"]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # Ratio tiempo
    bars1 = ax1.bar(ns, ratio_tiempo, color='#3498db', alpha=0.8, edgecolor='#2980b9', width=0.6)
    ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.7, linewidth=1)
    ax1.set_ylabel("Ratio BFS/DFS", fontsize=11)
    ax1.set_title("Ratio de TIEMPO: BFS ÷ DFS\n(>1 = BFS más lento)", fontsize=12, fontweight='bold', color='#2980b9')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    for bar, val in zip(bars1, ratio_tiempo):
        ax1.annotate(f'{val:.0f}x', xy=(bar.get_x() + bar.get_width()/2, val),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',
                     fontsize=10, fontweight='bold', color='#2980b9')
    
    # Ratio memoria
    bars2 = ax2.bar(ns, ratio_memoria, color='#e74c3c', alpha=0.8, edgecolor='#c0392b', width=0.6)
    ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.7, linewidth=1)
    ax2.set_ylabel("Ratio BFS/DFS", fontsize=11)
    ax2.set_title("Ratio de MEMORIA: BFS ÷ DFS\n(>1 = BFS usa más memoria)", fontsize=12, fontweight='bold', color='#c0392b')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    for bar, val in zip(bars2, ratio_memoria):
        ax2.annotate(f'{val:.0f}x', xy=(bar.get_x() + bar.get_width()/2, val),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',
                     fontsize=10, fontweight='bold', color='#c0392b')
    
    # Ratio nodos
    bars3 = ax3.bar(ns, ratio_nodos, color='#f39c12', alpha=0.8, edgecolor='#d68910', width=0.6)
    ax3.axhline(y=1, color='gray', linestyle='--', alpha=0.7, linewidth=1)
    ax3.set_xlabel("Tamaño del tablero (N)", fontsize=11)
    ax3.set_ylabel("Ratio BFS/DFS", fontsize=11)
    ax3.set_title("Ratio de NODOS EXPLORADOS: BFS ÷ DFS\n(>1 = BFS explora más)", fontsize=12, fontweight='bold', color='#d68910')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    for bar, val in zip(bars3, ratio_nodos):
        ax3.annotate(f'{val:.0f}x', xy=(bar.get_x() + bar.get_width()/2, val),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',
                     fontsize=10, fontweight='bold', color='#d68910')
    
    plt.suptitle("Comparación relativa BFS vs DFS (Ratio = BFS / DFS)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def grafica_boxplot_agrupado(datos, metrica, titulo, ylabel, guardar_como=None):
    """
    Genera un diagrama de caja agrupado por N (BFS y DFS lado a lado).
    """
    ns = sorted(datos["n"].unique())
    x = np.arange(len(ns))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, n in enumerate(ns):
        bfs_vals = datos[(datos["n"] == n) & (datos["algoritmo"] == "BFS")][metrica].values
        dfs_vals = datos[(datos["n"] == n) & (datos["algoritmo"] == "DFS")][metrica].values
        
        bp_bfs = ax.boxplot(bfs_vals, positions=[x[i] - width/2], widths=width,
                            patch_artist=True, showfliers=False,
                            boxprops=dict(facecolor='#3498db', alpha=0.7),
                            medianprops=dict(color='white', linewidth=2),
                            whiskerprops=dict(color='#3498db'),
                            capprops=dict(color='#3498db'))
        bp_dfs = ax.boxplot(dfs_vals, positions=[x[i] + width/2], widths=width,
                            patch_artist=True, showfliers=False,
                            boxprops=dict(facecolor='#e74c3c', alpha=0.7),
                            medianprops=dict(color='white', linewidth=2),
                            whiskerprops=dict(color='#e74c3c'),
                            capprops=dict(color='#e74c3c'))

    ax.set_xticks(x)
    ax.set_xticklabels([f"N={n}" for n in ns], fontsize=11)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.set_axisbelow(True)
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', alpha=0.7, label='BFS'),
        Patch(facecolor='#e74c3c', alpha=0.7, label='DFS')
    ]
    ax.legend(handles=legend_elements, fontsize=11)
    
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def grafica_boxplot_tiempo(datos, guardar_como=None):
    grafica_boxplot_agrupado(
        datos, "tiempo",
        "Distribución del tiempo de ejecución por N",
        "Tiempo (segundos)",
        guardar_como
    )


def grafica_boxplot_memoria(datos, guardar_como=None):
    grafica_boxplot_agrupado(
        datos, "memoria_kb",
        "Distribución del consumo de memoria por N",
        "Memoria pico (KB)",
        guardar_como
    )


def grafica_boxplot_nodos(datos, guardar_como=None):
    grafica_boxplot_agrupado(
        datos, "nodos",
        "Distribución de nodos explorados por N",
        "Nodos explorados",
        guardar_como
    )


def mostrar_resumen(promedios):
    print()
    print("PROMEDIOS DE LAS SIMULACIONES (100 ejecuciones cada una)")
    print("=" * 60)

    for _, fila in promedios.iterrows():
        print(f"\nN = {int(fila['n'])} - {fila['algoritmo']}")
        print(f"  Tiempo promedio:   {fila['tiempo_promedio']:.6f} s")
        print(f"  Memoria promedio:  {fila['memoria_promedio']:.2f} KB")
        print(f"  Nodos promedio:    {fila['nodos_promedio']:.0f}")


def generar_tablas_comparacion(promedios):
    bfs = promedios[promedios["algoritmo"] == "BFS"].copy()
    dfs = promedios[promedios["algoritmo"] == "DFS"].copy()

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

    print()
    print("COMPARACIÓN BFS vs DFS")
    print("=" * 60)

    for _, fila in comparacion.iterrows():
        n = int(fila["n"])
        print(f"\nN = {n}")
        print(f"  Tiempo:  BFS {fila['diferencia_tiempo_porcentaje']:+.2f}% vs DFS")
        print(f"  Memoria: BFS {fila['diferencia_memoria_porcentaje']:+.2f}% vs DFS")
        print(f"  Nodos:   BFS {fila['diferencia_nodos_porcentaje']:+.2f}% vs DFS")

    carpeta = os.path.join("..", "resultados", "nreinas", "datos")
    os.makedirs(carpeta, exist_ok=True)

    comparacion.to_csv(
        os.path.join(carpeta, "comparacion.csv"),
        index=False
    )

    promedios.to_csv(
        os.path.join(carpeta, "resumen.csv"),
        index=False
    )

    print("\nArchivos de análisis guardados en resultados/nreinas/datos/")
    return comparacion


def generar_todas_graficas(promedios, datos, carpeta_salida=None):
    """
    Genera y guarda TODAS las gráficas mejoradas en la carpeta especificada.
    """
    if carpeta_salida:
        carpeta_graficas = os.path.join("..", "resultados", "nreinas", "graficas", carpeta_salida)
        os.makedirs(carpeta_graficas, exist_ok=True)
        
        # 1. Barras agrupadas (principal)
        grafica_tiempo_por_n(promedios, os.path.join(carpeta_graficas, "01_tiempo_barras.png"))
        grafica_memoria_por_n(promedios, os.path.join(carpeta_graficas, "02_memoria_barras.png"))
        grafica_nodos_por_n(promedios, os.path.join(carpeta_graficas, "03_nodos_barras.png"))
        
        # 2. Subplots escalas separadas
        grafica_tiempo_subplots(promedios, os.path.join(carpeta_graficas, "04_tiempo_subplots.png"))
        grafica_memoria_subplots(promedios, os.path.join(carpeta_graficas, "05_memoria_subplots.png"))
        grafica_nodos_subplots(promedios, os.path.join(carpeta_graficas, "06_nodos_subplots.png"))
        
        # 3. Ratios BFS/DFS (LA MÁS IMPORTANTE)
        grafica_ratio_bfs_dfs(promedios, os.path.join(carpeta_graficas, "07_ratio_bfs_dfs.png"))
        
        # 4. Boxplots
        grafica_boxplot_tiempo(datos, os.path.join(carpeta_graficas, "08_boxplot_tiempo.png"))
        grafica_boxplot_memoria(datos, os.path.join(carpeta_graficas, "09_boxplot_memoria.png"))
        grafica_boxplot_nodos(datos, os.path.join(carpeta_graficas, "10_boxplot_nodos.png"))
        
        print(f"[OK] 10 gráficas guardadas en: {carpeta_graficas}")
    else:
        # Modo interactivo: mostrar las 3 principales + ratios
        grafica_tiempo_por_n(promedios)
        grafica_memoria_por_n(promedios)
        grafica_nodos_por_n(promedios)
        grafica_ratio_bfs_dfs(promedios)
        grafica_boxplot_tiempo(datos)
        grafica_boxplot_memoria(datos)
        grafica_boxplot_nodos(datos)


if __name__ == "__main__":
    datos = cargar_resultados()
    promedios = calcular_promedios(datos)

    mostrar_resumen(promedios)
    generar_tablas_comparacion(promedios)

    grafica_tiempo_por_n(promedios)
    grafica_memoria_por_n(promedios)
    grafica_nodos_por_n(promedios)
    grafica_ratio_bfs_dfs(promedios)

    grafica_boxplot_tiempo(datos)
    grafica_boxplot_memoria(datos)
    grafica_boxplot_nodos(datos)