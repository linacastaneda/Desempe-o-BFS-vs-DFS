from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_DATOS = RAIZ_PROYECTO / "resultados" / "nreinas" / "datos"
CARPETA_GRAFICAS = RAIZ_PROYECTO / "resultados" / "nreinas" / "graficas" / "comparacion_maquinas"


def cargar_todos_resultados(
    carpeta_base=CARPETA_DATOS
):
    """
    Carga archivos de resultados de una o varias máquinas.

    Se acepta el archivo estándar `resultados.csv` y también copias con
    nombres como `resultados_pc1.csv` o `resultados_portatil.csv`.
    """

    carpeta_base = Path(carpeta_base)

    archivos = sorted(
        carpeta_base.glob("resultados*.csv")
    )

    datos_lista = []

    for archivo in archivos:

        try:
            datos = pd.read_csv(archivo)
        except Exception as error:
            print(f"No se pudo cargar {archivo.name}: {error}")
            continue

        if "hostname" in datos.columns:
            fuente = str(datos["hostname"].iloc[0])
        else:
            fuente = archivo.stem.replace("resultados_", "")

        datos = datos.copy()
        datos["fuente"] = fuente

        datos_lista.append(
            datos
        )

        print(
            f"Cargado: {archivo.name} ({len(datos)} filas)"
        )

    if not datos_lista:
        print(
            f"No se encontraron archivos resultados*.csv en {carpeta_base}."
        )
        return None

    return pd.concat(
        datos_lista,
        ignore_index=True,
    )


def calcular_promedios_por_maquina(datos):
    """Calcula promedios por máquina, N y algoritmo."""

    return (
        datos
        .groupby(
            ["fuente", "n", "algoritmo"],
            as_index=False,
        )
        .agg(
            tiempo_promedio=("tiempo", "mean"),
            memoria_promedio=("memoria_kb", "mean"),
            nodos_promedio=("nodos", "mean"),
        )
    )


def grafica_por_maquina(
    promedios,
    metrica,
    ylabel,
    titulo,
    nombre_archivo,
):
    """Genera una gráfica de comparación entre máquinas."""

    CARPETA_GRAFICAS.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(
        figsize=(11, 6)
    )

    for (fuente, algoritmo), grupo in promedios.groupby(
        ["fuente", "algoritmo"]
    ):

        grupo = grupo.sort_values(
            "n"
        )

        plt.plot(
            grupo["n"],
            grupo[metrica],
            marker="o",
            label=f"{fuente} - {algoritmo}",
        )

    plt.yscale(
        "log"
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
    )

    plt.tight_layout()

    plt.savefig(
        CARPETA_GRAFICAS / nombre_archivo,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def main():
    """Ejecuta la comparación opcional entre resultados de varias máquinas."""

    datos = cargar_todos_resultados()

    if datos is None:
        return

    fuentes = sorted(
        datos["fuente"].unique()
    )

    print(
        "Máquinas/fuentes encontradas:",
        fuentes,
    )

    if len(fuentes) < 2:
        print(
            "Solo hay resultados de una máquina. "
            "La comparación multi-equipo no es necesaria."
        )
        return

    promedios = calcular_promedios_por_maquina(
        datos
    )

    grafica_por_maquina(
        promedios,
        "tiempo_promedio",
        "Tiempo promedio (segundos)",
        "N-Reinas - Tiempo por máquina",
        "tiempo_por_maquina.png",
    )

    grafica_por_maquina(
        promedios,
        "memoria_promedio",
        "Memoria pico promedio (KB)",
        "N-Reinas - Memoria por máquina",
        "memoria_por_maquina.png",
    )

    print(
        f"Gráficas guardadas en: {CARPETA_GRAFICAS}"
    )


if __name__ == "__main__":
    main()
