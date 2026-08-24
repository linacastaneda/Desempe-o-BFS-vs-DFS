from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def construir_arbol_mochila(
    pesos,
    valores,
    capacidad
):
    """
    Construye el árbol completo de decisiones
    de una instancia pequeña de Mochila 0/1.
    """

    grafo = nx.DiGraph()

    contador = 0

    raiz = contador

    grafo.add_node(
        raiz,
        indice=0,
        peso=0,
        valor=0,
        seleccionados=[]
    )

    contador += 1

    cola = deque(
        [raiz]
    )

    while cola:

        nodo = cola.popleft()

        datos = grafo.nodes[
            nodo
        ]

        indice = datos[
            "indice"
        ]

        peso = datos[
            "peso"
        ]

        valor = datos[
            "valor"
        ]

        seleccionados = datos[
            "seleccionados"
        ]

        if indice == len(pesos):
            continue

        nodo_no_tomar = contador

        contador += 1

        grafo.add_node(
            nodo_no_tomar,
            indice=indice + 1,
            peso=peso,
            valor=valor,
            seleccionados=seleccionados.copy()
        )

        grafo.add_edge(
            nodo,
            nodo_no_tomar,
            decision=f"No tomar {indice + 1}"
        )

        cola.append(
            nodo_no_tomar
        )

        nuevo_peso = (
            peso
            + pesos[indice]
        )

        if nuevo_peso <= capacidad:

            nodo_tomar = contador

            contador += 1

            nuevo_valor = (
                valor
                + valores[indice]
            )

            nueva_seleccion = (
                seleccionados
                + [indice]
            )

            grafo.add_node(
                nodo_tomar,
                indice=indice + 1,
                peso=nuevo_peso,
                valor=nuevo_valor,
                seleccionados=nueva_seleccion
            )

            grafo.add_edge(
                nodo,
                nodo_tomar,
                decision=f"Tomar {indice + 1}"
            )

            cola.append(
                nodo_tomar
            )

    return grafo, raiz


def obtener_orden_bfs(
    grafo,
    raiz
):
    """
    Obtiene el recorrido BFS.
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
    Obtiene el recorrido DFS reproduciendo
    el comportamiento del algoritmo de Mochila.

    El hijo generado al final se procesa
    primero debido al funcionamiento LIFO.
    """

    orden = []

    pila = [
        raiz
    ]

    while pila:

        nodo = pila.pop()

        orden.append(
            nodo
        )

        for hijo in grafo.successors(
            nodo
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

    posiciones = {}

    niveles = {}

    cola = deque(
        [
            (
                raiz,
                0
            )
        ]
    )

    while cola:

        nodo, nivel = cola.popleft()

        if nivel not in niveles:

            niveles[
                nivel
            ] = []

        niveles[
            nivel
        ].append(
            nodo
        )

        for hijo in grafo.successors(
            nodo
        ):

            cola.append(
                (
                    hijo,
                    nivel + 1
                )
            )

    for nivel, nodos in niveles.items():

        cantidad = len(
            nodos
        )

        for posicion, nodo in enumerate(
            nodos
        ):

            x = (
                posicion
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


def obtener_mejor_valor(
    grafo,
    cantidad_objetos
):
    """
    Obtiene el mayor valor entre estados
    terminales del árbol.
    """

    valores_finales = []

    for nodo in grafo.nodes:

        datos = grafo.nodes[
            nodo
        ]

        if (
            datos["indice"]
            == cantidad_objetos
        ):

            valores_finales.append(
                datos["valor"]
            )

    return max(
        valores_finales
    )


def obtener_soluciones(
    grafo,
    mejor_valor,
    cantidad_objetos
):
    """
    Obtiene las hojas que representan
    soluciones óptimas.
    """

    soluciones = []

    for nodo in grafo.nodes:

        datos = grafo.nodes[
            nodo
        ]

        if (
            datos["indice"] == cantidad_objetos
            and datos["valor"] == mejor_valor
        ):

            soluciones.append(
                nodo
            )

    return soluciones


def crear_etiquetas(
    grafo,
    orden,
    soluciones
):
    """
    Crea las etiquetas visuales.
    """

    posiciones_orden = {
        nodo: numero
        for numero, nodo
        in enumerate(
            orden,
            start=1
        )
    }

    etiquetas = {}

    for nodo in grafo.nodes:

        datos = grafo.nodes[
            nodo
        ]

        etiqueta = (
            f"#{posiciones_orden[nodo]}\n"
            f"P={datos['peso']}\n"
            f"V={datos['valor']}"
        )

        if nodo in soluciones:

            etiqueta += (
                "\nÓPTIMO"
            )

        etiquetas[
            nodo
        ] = etiqueta

    return etiquetas


def mostrar_arbol_comparado(
    pesos,
    valores,
    capacidad
):
    """
    Genera una sola imagen con:

        BFS a la izquierda.
        DFS a la derecha.
    """

    grafo, raiz = (
        construir_arbol_mochila(
            pesos,
            valores,
            capacidad
        )
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

    mejor_valor = obtener_mejor_valor(
        grafo,
        len(pesos)
    )

    soluciones = obtener_soluciones(
        grafo,
        mejor_valor,
        len(pesos)
    )

    etiquetas_aristas = (
        nx.get_edge_attributes(
            grafo,
            "decision"
        )
    )

    carpeta = Path(
        "resultados/mochila/graficas/arboles"
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
            orden,
            soluciones
        )

        nx.draw(
            grafo,
            posiciones,
            ax=eje,
            labels=etiquetas,
            with_labels=True,
            node_size=1900,
            font_size=6,
            arrows=True,
            arrowsize=12
        )

        nx.draw_networkx_edge_labels(
            grafo,
            posiciones,
            ax=eje,
            edge_labels=etiquetas_aristas,
            font_size=5
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
        "Mochila 0/1 - Árbol de búsqueda BFS vs DFS\n"
        f"Capacidad: {capacidad} | "
        f"Nodos: {grafo.number_of_nodes()} | "
        f"Valor óptimo: {mejor_valor}",
        fontsize=15,
        fontweight="bold"
    )

    plt.tight_layout()

    ruta = (
        carpeta
        / "arbol_mochila.png"
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

    pesos = [
        2,
        3,
        4,
        5
    ]

    valores = [
        3,
        4,
        5,
        8
    ]

    capacidad = 8

    mostrar_arbol_comparado(
        pesos,
        valores,
        capacidad
    )