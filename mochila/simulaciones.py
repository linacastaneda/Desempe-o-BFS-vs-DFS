import random
import csv
import os

from bfs_dfs_mochila import bfs_mochila, dfs_mochila
from medicion import medir_algoritmo


def generar_mochila(cantidad_objetos):
    """
    Genera una instancia aleatoria del problema
    de la mochila 0/1.

    Cada objeto tiene:
        - Un peso entre 1 y 15.
        - Un valor entre 1 y 30.

    La capacidad de la mochila corresponde
    aproximadamente al 40 % del peso total
    de todos los objetos.

    Parámetros:
        cantidad_objetos: cantidad de objetos
        que tendrá la mochila.

    Retorna:
        pesos: lista de pesos generados.
        valores: lista de valores generados.
        capacidad: capacidad máxima de la mochila.
    """

    pesos = []
    valores = []

    for _ in range(cantidad_objetos):

        peso = random.randint(1, 15)
        valor = random.randint(1, 30)

        pesos.append(peso)
        valores.append(valor)

    peso_total = sum(pesos)

    capacidad = max(
        1,
        int(peso_total * 0.40)
    )

    return pesos, valores, capacidad


def ejecutar_simulaciones():
    """
    Ejecuta 100 simulaciones del problema
    de la mochila 0/1.

    Se utilizan cinco tamaños diferentes:

        5 objetos
        8 objetos
        10 objetos
        12 objetos
        15 objetos

    Para cada tamaño se generan 20 mochilas
    aleatorias.

    Cada mochila es resuelta tanto por BFS
    como por DFS utilizando exactamente
    los mismos pesos, valores y capacidad.

    Esto permite comparar de manera justa
    el tiempo de ejecución y el consumo
    de memoria de ambos algoritmos.
    """

    tamanos = [5, 8, 10, 12, 15]

    simulaciones_por_tamano = 20

    resultados = []

    numero_simulacion = 1

    for cantidad_objetos in tamanos:

        print()

        print(
            "Ejecutando simulaciones con",
            cantidad_objetos,
            "objetos..."
        )

        for _ in range(simulaciones_por_tamano):

            pesos, valores, capacidad = generar_mochila(
                cantidad_objetos
            )

            resultado_bfs = medir_algoritmo(
                bfs_mochila,
                pesos,
                valores,
                capacidad
            )

            resultado_dfs = medir_algoritmo(
                dfs_mochila,
                pesos,
                valores,
                capacidad
            )

            if resultado_bfs["valor"] != resultado_dfs["valor"]:

                print(
                    "Advertencia: BFS y DFS encontraron "
                    "resultados diferentes en la simulación",
                    numero_simulacion
                )

            resultados.append(
                {
                    "simulacion": numero_simulacion,
                    "objetos": cantidad_objetos,
                    "algoritmo": "BFS",
                    "pesos": pesos,
                    "valores": valores,
                    "capacidad": capacidad,
                    "tiempo": resultado_bfs["tiempo"],
                    "memoria_kb": resultado_bfs["memoria_kb"],
                    "nodos": resultado_bfs["nodos"],
                    "valor_optimo": resultado_bfs["valor"]
                }
            )

            resultados.append(
                {
                    "simulacion": numero_simulacion,
                    "objetos": cantidad_objetos,
                    "algoritmo": "DFS",
                    "pesos": pesos,
                    "valores": valores,
                    "capacidad": capacidad,
                    "tiempo": resultado_dfs["tiempo"],
                    "memoria_kb": resultado_dfs["memoria_kb"],
                    "nodos": resultado_dfs["nodos"],
                    "valor_optimo": resultado_dfs["valor"]
                }
            )

            print(
                f"Simulación {numero_simulacion}: "
                f"{cantidad_objetos} objetos"
            )

            numero_simulacion += 1

    return resultados


def guardar_resultados(resultados):
    """
    Guarda en un archivo CSV los resultados
    obtenidos durante las simulaciones.

    Además de las métricas de desempeño,
    se almacenan los pesos y valores utilizados
    en cada instancia.

    Esto permite identificar y reproducir
    exactamente cada problema de mochila.
    """

    carpeta_resultados = "resultados"

    os.makedirs(
        carpeta_resultados,
        exist_ok=True
    )

    ruta_archivo = os.path.join(
        carpeta_resultados,
        "resultados_mochila.csv"
    )

    columnas = [
        "simulacion",
        "objetos",
        "algoritmo",
        "pesos",
        "valores",
        "capacidad",
        "tiempo",
        "memoria_kb",
        "nodos",
        "valor_optimo"
    ]

    with open(
        ruta_archivo,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )

        escritor.writeheader()

        escritor.writerows(resultados)

    print()

    print(
        "Resultados guardados en:",
        ruta_archivo
    )


if __name__ == "__main__":

    # La semilla permite que las mismas mochilas
    # puedan volver a generarse en futuras ejecuciones.
    random.seed(42)

    resultados = ejecutar_simulaciones()

    guardar_resultados(resultados)

    print()

    print(
        "Simulaciones completadas correctamente."
    )