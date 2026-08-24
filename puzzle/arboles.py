"""
Visualización del espacio de estados del Puzzle 3x3.

Este archivo construye un árbol parcial del espacio de búsqueda
a partir de un estado inicial y permite comparar visualmente
el orden de recorrido de:

- BFS
- DFS

El árbol utilizado es el mismo para ambos algoritmos.
Lo que cambia es el orden en que los estados son visitados.

La profundidad se limita para mantener la visualización legible.
"""

from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

from bfs_dfs_puzzle import (
    INICIO_PUZZLE,
    META_PUZZLE,
    movimientos,
)


def construir_arbol(
    inicio,
    profundidad_max=3
):
    """
    Construye un árbol parcial del espacio de estados
    del Puzzle 3x3.

    Parámetros:
        inicio:
            Estado inicial del Puzzle.

        profundidad_max:
            Profundidad máxima que se mostrará
            en el árbol.

    Retorna:
        grafo:
            Grafo dirigido con los estados.

        raiz:
            Estado inicial utilizado como raíz.
    """

    grafo = nx.DiGraph()

    raiz = inicio

    cola = deque()

    cola.append(
        (
            inicio,
            0
        )
    )

    visitados = {
        inicio
    }

    grafo.add_node(
        inicio,
        profundidad=0
    )

    while cola:

        estado, profundidad = cola.popleft()

        if profundidad >= profundidad_max:
            continue

        for nuevo_estado in movimientos(
            estado
        ):

            if nuevo_estado not in visitados:

                visitados.add(
                    nuevo_estado
                )

                grafo.add_node(
                    nuevo_estado,
                    profundidad=profundidad + 1
                )

                grafo.add_edge(
                    estado,
                    nuevo_estado
                )

                cola.append(
                    (
                        nuevo_estado,
                        profundidad + 1
                    )
                )

    return grafo, raiz


def obtener_orden_bfs(
    grafo,
    raiz
):
    """
    Obtiene el orden en que BFS visita los nodos.

    BFS utiliza una cola FIFO y explora
    los estados nivel por nivel.
    """

    orden = []

    cola = deque(
        [raiz]
    )

    visitados = {
        raiz
    }

    while cola:

        nodo = cola.popleft()

        orden.append(
            nodo
        )

        for hijo in grafo.successors(
            nodo
        ):

            if hijo not in visitados:

                visitados.add(
                    hijo
                )

                cola.append(
                    hijo
                )

    return orden


def obtener_orden_dfs(
    grafo,
    raiz
):
    """
    Obtiene el orden en que DFS visita los nodos.

    DFS utiliza una pila LIFO y profundiza
    una rama antes de regresar.
    """

    orden = []

    pila = [
        raiz
    ]

    visitados = set()

    while pila:

        nodo = pila.pop()

        if nodo in visitados:
            continue

        visitados.add(
            nodo
        )

        orden.append(
            nodo
        )

        hijos = list(
            grafo.successors(
                nodo
            )
        )

        # Se invierte el orden de los hijos
        # para que el primer hijo generado
        # sea también el primero en ser visitado
        # por DFS.
        hijos.reverse()

        for hijo in hijos:

            if hijo not in visitados:

                pila.append(
                    hijo
                )

    return orden


def calcular_posiciones(
    grafo,
    raiz
):
    """
    Calcula posiciones jerárquicas para dibujar
    el árbol de arriba hacia abajo.
    """

    niveles = {}

    for nodo in grafo.nodes:

        nivel = nx.shortest_path_length(
            grafo,
            raiz,
            nodo
        )

        if nivel not in niveles:

            niveles[nivel] = []

        niveles[nivel].append(
            nodo
        )

    posiciones = {}

    for nivel, nodos in niveles.items():

        cantidad = len(
            nodos
        )

        for indice, nodo in enumerate(
            nodos
        ):

            x = indice - (
                cantidad - 1
            ) / 2

            y = -nivel

            posiciones[
                nodo
            ] = (
                x,
                y
            )

    return posiciones


def estado_a_texto(
    estado
):
    """
    Convierte un estado del Puzzle
    en una representación de tres filas.

    El cero se representa como un espacio
    para que se parezca al tablero real.

    Ejemplo:

        123
        5 6
        478
    """

    valores = []

    for numero in estado:

        if numero == 0:

            valores.append(
                " "
            )

        else:

            valores.append(
                str(numero)
            )

    fila_1 = "".join(
        valores[0:3]
    )

    fila_2 = "".join(
        valores[3:6]
    )

    fila_3 = "".join(
        valores[6:9]
    )

    return (
        f"{fila_1}\n"
        f"{fila_2}\n"
        f"{fila_3}"
    )


def crear_etiquetas(
    grafo,
    orden
):
    """
    Crea las etiquetas de los nodos.

    Cada nodo muestra:

        - Número de visita.
        - Configuración del Puzzle.

    Si el estado corresponde a la meta,
    se agrega la palabra META.
    """

    posiciones_orden = {}

    for numero_visita, nodo in enumerate(
        orden,
        start=1
    ):

        posiciones_orden[
            nodo
        ] = numero_visita

    etiquetas = {}

    for nodo in grafo.nodes:

        numero = posiciones_orden[
            nodo
        ]

        tablero = estado_a_texto(
            nodo
        )

        etiqueta = (
            f"#{numero}\n"
            f"{tablero}"
        )

        if nodo == META_PUZZLE:

            etiqueta += "\nMETA"

        etiquetas[
            nodo
        ] = etiqueta

    return etiquetas


def mostrar_arbol(
    grafo,
    raiz,
    orden,
    algoritmo,
    profundidad_max,
    carpeta
):
    """
    Dibuja el árbol parcial del Puzzle.

    Los números dentro de los nodos indican
    el orden de visita del algoritmo.
    """

    posiciones = calcular_posiciones(
        grafo,
        raiz
    )

    etiquetas = crear_etiquetas(
        grafo,
        orden
    )

    plt.figure(
        figsize=(18, 10)
    )

    nx.draw_networkx_edges(
        grafo,
        posiciones,
        arrows=True,
        width=1.2
    )

    nx.draw_networkx_nodes(
        grafo,
        posiciones,
        node_size=2200
    )

    nx.draw_networkx_labels(
        grafo,
        posiciones,
        labels=etiquetas,
        font_size=7
    )

    if META_PUZZLE in grafo.nodes:

        nx.draw_networkx_nodes(
            grafo,
            posiciones,
            nodelist=[
                META_PUZZLE
            ],
            node_size=2900
        )

        nx.draw_networkx_labels(
            grafo,
            posiciones,
            labels={
                META_PUZZLE:
                    etiquetas[META_PUZZLE]
            },
            font_size=7
        )

    plt.title(
        f"Puzzle 3x3 - Recorrido {algoritmo}\n"
        f"Profundidad visual: {profundidad_max}"
    )

    plt.axis(
        "off"
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    nombre_archivo = (
        f"arbol_{algoritmo.lower()}_puzzle.png"
    )

    plt.savefig(
        carpeta / nombre_archivo,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()


def mostrar_secuencia(
    orden,
    algoritmo
):
    """
    Muestra en consola el orden de visita
    de los estados.
    """

    print()

    print(
        f"ORDEN DE RECORRIDO {algoritmo}"
    )

    print()

    for numero, nodo in enumerate(
        orden,
        start=1
    ):

        print(
            f"#{numero}: {nodo}"
        )


def mostrar_datos_arbol(
    grafo,
    profundidad_max
):
    """
    Muestra información general
    del árbol parcial generado.
    """

    print()

    print(
        "ÁRBOL PARCIAL DEL PUZZLE 3x3"
    )

    print()

    print(
        "Profundidad máxima visual:",
        profundidad_max
    )

    print(
        "Cantidad de estados mostrados:",
        grafo.number_of_nodes()
    )

    print(
        "Cantidad de conexiones:",
        grafo.number_of_edges()
    )

    print()

    print(
        "Estado inicial:",
        INICIO_PUZZLE
    )

    print(
        "Estado meta:",
        META_PUZZLE
    )

    print()

    if META_PUZZLE in grafo.nodes:

        print(
            "La meta aparece dentro "
            "del árbol visual."
        )

    else:

        print(
            "La meta NO aparece dentro "
            "de la profundidad visual seleccionada."
        )


if __name__ == "__main__":

    # Se utiliza una profundidad pequeña
    # exclusivamente para la visualización.
    #
    # No se intenta representar todo el espacio
    # de estados del Puzzle porque la gráfica
    # sería demasiado grande e ilegible.

    profundidad_max = 3

    carpeta = Path(
        "resultados/arboles_puzzle"
    )

    grafo, raiz = construir_arbol(
        INICIO_PUZZLE,
        profundidad_max
    )

    orden_bfs = obtener_orden_bfs(
        grafo,
        raiz
    )

    orden_dfs = obtener_orden_dfs(
        grafo,
        raiz
    )

    mostrar_datos_arbol(
        grafo,
        profundidad_max
    )

    mostrar_secuencia(
        orden_bfs,
        "BFS"
    )

    mostrar_secuencia(
        orden_dfs,
        "DFS"
    )

    mostrar_arbol(
        grafo,
        raiz,
        orden_bfs,
        "BFS",
        profundidad_max,
        carpeta
    )

    mostrar_arbol(
        grafo,
        raiz,
        orden_dfs,
        "DFS",
        profundidad_max,
        carpeta
    )

    print()

    print(
        "Árboles guardados correctamente."
    )

    print(
        "Carpeta:",
        carpeta
    )