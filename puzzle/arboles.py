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
    Construye un árbol parcial común
    del espacio de estados.
    """

    grafo = nx.DiGraph()

    raiz = inicio

    cola = deque(
        [
            (
                inicio,
                0
            )
        ]
    )

    visitados = {
        inicio
    }

    grafo.add_node(
        inicio,
        profundidad=0
    )

    while cola:

        estado, profundidad = (
            cola.popleft()
        )

        if (
            profundidad
            >= profundidad_max
        ):
            continue

        for nuevo_estado in movimientos(
            estado
        ):

            if (
                nuevo_estado
                not in visitados
            ):

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
    Recorrido BFS.
    """

    orden = []

    cola = deque(
        [raiz]
    )

    while cola:

        nodo = cola.popleft()

        orden.append(
            nodo
        )

        for hijo in grafo.successors(
            nodo
        ):

            cola.append(
                hijo
            )

    return orden


def obtener_orden_dfs(
    grafo,
    raiz
):
    """
    Recorrido DFS.

    Los hijos se agregan a la pila
    en el orden en que fueron generados,
    reproduciendo la lógica del solver DFS.
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

        for hijo in hijos:

            if (
                hijo
                not in visitados
            ):

                pila.append(
                    hijo
                )

    return orden


def calcular_posiciones(
    grafo,
    raiz
):
    """
    Calcula posiciones jerárquicas.
    """

    niveles = {}

    for nodo in grafo.nodes:

        nivel = (
            nx.shortest_path_length(
                grafo,
                raiz,
                nodo
            )
        )

        if nivel not in niveles:

            niveles[
                nivel
            ] = []

        niveles[
            nivel
        ].append(
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

            x = (
                indice
                - (cantidad - 1) / 2
            )

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
    Representa un estado como tablero 3x3.
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

    return (
        f"{''.join(valores[0:3])}\n"
        f"{''.join(valores[3:6])}\n"
        f"{''.join(valores[6:9])}"
    )


def crear_etiquetas(
    grafo,
    orden
):
    """
    Crea etiquetas con número de visita
    y estado del tablero.
    """

    posiciones = {
        nodo: numero
        for numero, nodo
        in enumerate(
            orden,
            start=1
        )
    }

    etiquetas = {}

    for nodo in grafo.nodes:

        etiqueta = (
            f"#{posiciones[nodo]}\n"
            f"{estado_a_texto(nodo)}"
        )

        if nodo == META_PUZZLE:

            etiqueta += (
                "\nMETA"
            )

        etiquetas[
            nodo
        ] = etiqueta

    return etiquetas


def mostrar_arbol_comparado(
    inicio=INICIO_PUZZLE,
    profundidad_max=3
):
    """
    Guarda una única imagen con BFS
    y DFS lado a lado.
    """

    grafo, raiz = construir_arbol(
        inicio,
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

    posiciones = calcular_posiciones(
        grafo,
        raiz
    )

    carpeta = Path(
        "resultados/puzzle/graficas/arboles"
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    figura, (
        ax_bfs,
        ax_dfs
    ) = plt.subplots(
        1,
        2,
        figsize=(24, 10)
    )

    configuraciones = [
        (
            ax_bfs,
            orden_bfs,
            "BFS - Nivel por nivel"
        ),
        (
            ax_dfs,
            orden_dfs,
            "DFS - Profundidad"
        )
    ]

    for (
        eje,
        orden,
        titulo
    ) in configuraciones:

        etiquetas = crear_etiquetas(
            grafo,
            orden
        )

        nx.draw_networkx_edges(
            grafo,
            posiciones,
            ax=eje,
            arrows=True,
            arrowsize=12
        )

        nx.draw_networkx_nodes(
            grafo,
            posiciones,
            ax=eje,
            node_size=1900
        )

        nx.draw_networkx_labels(
            grafo,
            posiciones,
            ax=eje,
            labels=etiquetas,
            font_size=6
        )

        if (
            META_PUZZLE
            in grafo.nodes
        ):

            nx.draw_networkx_nodes(
                grafo,
                posiciones,
                ax=eje,
                nodelist=[
                    META_PUZZLE
                ],
                node_size=2400
            )

        eje.set_title(
            titulo,
            fontsize=13,
            fontweight="bold"
        )

        eje.axis(
            "off"
        )

    figura.suptitle(
        "Puzzle 3x3 - Árbol parcial BFS vs DFS\n"
        f"Profundidad visual: {profundidad_max} | "
        f"Estados mostrados: {grafo.number_of_nodes()}",
        fontsize=15,
        fontweight="bold"
    )

    plt.tight_layout()

    ruta = (
        carpeta
        / "arbol_puzzle.png"
    )

    plt.savefig(
        ruta,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

    print()

    print(
        "Árbol guardado en:",
        ruta
    )


if __name__ == "__main__":

    mostrar_arbol_comparado(
        INICIO_PUZZLE,
        profundidad_max=3
    )