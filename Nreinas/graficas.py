from pathlib import Path
import os
import platform
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_DATOS = RAIZ_PROYECTO / "resultados" / "nreinas" / "datos"
CARPETA_GRAFICAS = RAIZ_PROYECTO / "resultados" / "nreinas" / "graficas"


def obtener_info_maquina():
    """Obtiene información básica del equipo utilizado en el experimento."""

    def obtener_nombre_cpu():
        try:
            if platform.system() == "Windows":
                resultado = subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "Get-CimInstance Win32_Processor | "
                        "Select-Object -ExpandProperty Name",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                nombre = resultado.stdout.strip()

                if nombre:
                    return nombre

            if platform.system() == "Linux":
                with open(
                    "/proc/cpuinfo",
                    "r",
                    encoding="utf-8",
                ) as archivo:
                    for linea in archivo:
                        if linea.startswith("model name"):
                            return linea.split(":", 1)[1].strip()

            if platform.system() == "Darwin":
                resultado = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                nombre = resultado.stdout.strip()

                if nombre:
                    return nombre

        except Exception:
            pass

        return platform.processor()

    info = {
        "hostname": platform.node(),
        "sistema": platform.system(),
        "version_sistema": platform.version(),
        "arquitectura": platform.machine(),
        "procesador": obtener_nombre_cpu(),
        "python_version": sys.version.split()[0],
        "cpu_count": os.cpu_count(),
    }

    try:
        import psutil

        info["ram_total_gb"] = round(
            psutil.virtual_memory().total / (1024 ** 3),
            2,
        )

        frecuencia = psutil.cpu_freq()

        info["cpu_freq_mhz"] = (
            frecuencia.current
            if frecuencia
            else None
        )

        info["cpu_freq_max_mhz"] = (
            frecuencia.max
            if frecuencia
            else None
        )

    except ImportError:
        info["ram_total_gb"] = None
        info["cpu_freq_mhz"] = None
        info["cpu_freq_max_mhz"] = None

    return info


def cargar_resultados(
    archivo=None
):
    """Carga el CSV con los resultados de N-Reinas."""

    ruta = (
        Path(archivo)
        if archivo is not None
        else CARPETA_DATOS / "resultados.csv"
    )

    return pd.read_csv(ruta)


def calcular_promedios(datos):
    """Calcula promedios de tiempo, memoria y nodos por N y algoritmo."""

    return (
        datos
        .groupby(
            ["n", "algoritmo"],
            as_index=False,
        )
        .agg(
            repeticiones=("simulacion", "count"),
            tiempo_promedio=("tiempo", "mean"),
            memoria_promedio=("memoria_kb", "mean"),
            nodos_promedio=("nodos", "mean"),
        )
    )


def guardar_figura(
    ruta
):
    """Guarda la figura actual y libera sus recursos."""

    ruta = Path(ruta)

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.tight_layout()

    plt.savefig(
        ruta,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def grafica_comparativa(
    promedios,
    metrica,
    titulo,
    ylabel,
    ruta,
):
    """
    Genera barras agrupadas BFS vs DFS por N.

    Se utiliza escala logarítmica porque las diferencias entre ambos
    algoritmos abarcan varios órdenes de magnitud para N grandes.
    """

    bfs = (
        promedios[
            promedios["algoritmo"] == "BFS"
        ]
        .set_index("n")
        .sort_index()
    )

    dfs = (
        promedios[
            promedios["algoritmo"] == "DFS"
        ]
        .set_index("n")
        .sort_index()
    )

    valores_n = sorted(
        promedios["n"].unique()
    )

    posiciones = np.arange(
        len(valores_n)
    )

    ancho = 0.36

    plt.figure(
        figsize=(11, 6)
    )

    plt.bar(
        posiciones - ancho / 2,
        [bfs.loc[n, metrica] for n in valores_n],
        ancho,
        label="BFS",
    )

    plt.bar(
        posiciones + ancho / 2,
        [dfs.loc[n, metrica] for n in valores_n],
        ancho,
        label="DFS",
    )

    plt.yscale(
        "log"
    )

    plt.xticks(
        posiciones,
        [str(n) for n in valores_n],
    )

    plt.xlabel(
        "Tamaño del tablero (N)"
    )

    plt.ylabel(
        ylabel
    )

    plt.title(
        titulo
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
        which="both",
        axis="y",
    )

    guardar_figura(
        ruta
    )


def grafica_tiempo_por_n(
    promedios,
    ruta
):
    """Genera la comparación de tiempo promedio por N."""

    grafica_comparativa(
        promedios,
        "tiempo_promedio",
        "N-Reinas - Tiempo promedio BFS vs DFS",
        "Tiempo promedio (segundos)",
        ruta,
    )


def grafica_memoria_por_n(
    promedios,
    ruta
):
    """Genera la comparación de memoria pico promedio por N."""

    grafica_comparativa(
        promedios,
        "memoria_promedio",
        "N-Reinas - Memoria promedio BFS vs DFS",
        "Memoria pico promedio (KB)",
        ruta,
    )


def grafica_nodos_por_n(
    promedios,
    ruta
):
    """Genera la comparación de nodos explorados promedio por N."""

    grafica_comparativa(
        promedios,
        "nodos_promedio",
        "N-Reinas - Nodos explorados BFS vs DFS",
        "Nodos explorados promedio",
        ruta,
    )


def grafica_ratio_bfs_dfs(
    promedios,
    ruta
):
    """
    Muestra cuántas veces el promedio de BFS supera al de DFS.

    Los ratios se presentan para tiempo, memoria y nodos. La línea 1x
    representa igualdad entre ambos algoritmos.
    """

    bfs = (
        promedios[
            promedios["algoritmo"] == "BFS"
        ]
        .set_index("n")
        .sort_index()
    )

    dfs = (
        promedios[
            promedios["algoritmo"] == "DFS"
        ]
        .set_index("n")
        .sort_index()
    )

    valores_n = sorted(
        promedios["n"].unique()
    )

    ratio_tiempo = [
        bfs.loc[n, "tiempo_promedio"]
        / dfs.loc[n, "tiempo_promedio"]
        for n in valores_n
    ]

    ratio_memoria = [
        bfs.loc[n, "memoria_promedio"]
        / dfs.loc[n, "memoria_promedio"]
        for n in valores_n
    ]

    ratio_nodos = [
        bfs.loc[n, "nodos_promedio"]
        / dfs.loc[n, "nodos_promedio"]
        for n in valores_n
    ]

    plt.figure(
        figsize=(11, 6)
    )

    plt.plot(
        valores_n,
        ratio_tiempo,
        marker="o",
        label="Tiempo BFS/DFS",
    )

    plt.plot(
        valores_n,
        ratio_memoria,
        marker="o",
        label="Memoria BFS/DFS",
    )

    plt.plot(
        valores_n,
        ratio_nodos,
        marker="o",
        label="Nodos BFS/DFS",
    )

    plt.axhline(
        y=1,
        linestyle="--",
        label="Igualdad (1x)",
    )

    plt.yscale(
        "log"
    )

    plt.xlabel(
        "Tamaño del tablero (N)"
    )

    plt.ylabel(
        "Ratio BFS / DFS"
    )

    plt.title(
        "N-Reinas - Comparación relativa BFS/DFS"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
        which="both",
    )

    guardar_figura(
        ruta
    )


def mostrar_resumen(
    promedios
):
    """Muestra los promedios y el número real de repeticiones por N."""

    print()
    print("PROMEDIOS DE N-REINAS")
    print()

    for _, fila in promedios.iterrows():

        print(
            f"N={int(fila['n'])} - {fila['algoritmo']} "
            f"({int(fila['repeticiones'])} repeticiones)"
        )

        print(
            f"  Tiempo promedio:  {fila['tiempo_promedio']:.6f} s"
        )

        print(
            f"  Memoria promedio: {fila['memoria_promedio']:.2f} KB"
        )

        print(
            f"  Nodos promedio:   {fila['nodos_promedio']:.0f}"
        )

        print()


def generar_todas_graficas(
    promedios,
    datos=None,
    carpeta_salida=None,
):
    """
    Genera las cuatro gráficas principales del análisis de N-Reinas.

    El parámetro datos se conserva para mantener compatibilidad con main.py,
    aunque estas cuatro gráficas utilizan los promedios agregados.
    """

    carpeta = CARPETA_GRAFICAS

    if carpeta_salida:
        carpeta = carpeta / carpeta_salida

    carpeta.mkdir(
        parents=True,
        exist_ok=True,
    )

    grafica_tiempo_por_n(
        promedios,
        carpeta / "01_tiempo_por_n.png",
    )

    grafica_memoria_por_n(
        promedios,
        carpeta / "02_memoria_por_n.png",
    )

    grafica_nodos_por_n(
        promedios,
        carpeta / "03_nodos_por_n.png",
    )

    grafica_ratio_bfs_dfs(
        promedios,
        carpeta / "04_ratio_bfs_dfs.png",
    )

    print(
        f"Se generaron 4 gráficas principales en: {carpeta}"
    )


if __name__ == "__main__":

    datos = cargar_resultados()

    promedios = calcular_promedios(
        datos
    )

    mostrar_resumen(
        promedios
    )

    generar_todas_graficas(
        promedios,
        datos,
    )
