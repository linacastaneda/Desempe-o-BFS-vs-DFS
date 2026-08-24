"""
Árbol de búsqueda del Puzzle 3x3.

El notebook original mostraba un árbol conceptual.
Aquí se genera el árbol real a partir del estado inicial.
Para que la gráfica sea legible se puede limitar la profundidad.
"""

import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError as exc:
    raise ImportError(
        "Instala networkx con: pip install networkx"
    ) from exc

from bfs_dfs_puzzle import movimientos


def etiqueta(estado):
    """Representación compacta de un estado."""
    return "".join(str(x) for x in estado)


def construir_arbol(inicio, profundidad_max=3):
    """Construye un árbol parcial del espacio de búsqueda."""
    grafo = nx.DiGraph()
    frontera = [(inicio, 0)]
    visitados = {inicio}

    while frontera:
        estado, profundidad = frontera.pop(0)
        grafo.add_node(estado)

        if profundidad >= profundidad_max:
            continue

        for nuevo in movimientos(estado):
            if nuevo not in visitados:
                visitados.add(nuevo)
                grafo.add_edge(estado, nuevo)
                frontera.append((nuevo, profundidad + 1))

    return grafo


def dibujar_arbol(inicio, profundidad_max=3, titulo="Árbol de búsqueda"):
    """Dibuja el árbol parcial del Puzzle 3x3."""
    grafo = construir_arbol(inicio, profundidad_max)

    niveles = {}
    for nodo in grafo.nodes:
        nivel = nx.shortest_path_length(grafo, inicio, nodo)
        niveles.setdefault(nivel, []).append(nodo)

    pos = {}
    for nivel, nodos in niveles.items():
        cantidad = len(nodos)
        for i, nodo in enumerate(nodos):
            x = i - (cantidad - 1) / 2
            pos[nodo] = (x, -nivel)

    plt.figure(figsize=(16, 9))
    nx.draw(
        grafo,
        pos,
        labels={n: etiqueta(n) for n in grafo.nodes},
        with_labels=True,
        node_size=1200,
        font_size=7,
        arrows=True,
    )
    plt.title(f"{titulo} - profundidad {profundidad_max}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    from bfs_dfs_puzzle import INICIO_PUZZLE
    dibujar_arbol(INICIO_PUZZLE, profundidad_max=3)
