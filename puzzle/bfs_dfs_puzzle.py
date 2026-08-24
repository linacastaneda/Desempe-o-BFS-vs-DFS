"""
Puzzle 3x3 - BFS y DFS
"""

from collections import deque


INICIO_PUZZLE = (1, 2, 3, 5, 0, 6, 4, 7, 8)

META_PUZZLE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def movimientos(estado):
    """Genera los movimientos válidos del espacio vacío."""

    resultado = []

    posicion = estado.index(0)

    fila = posicion // 3
    columna = posicion % 3

    direcciones = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    for df, dc in direcciones:

        nueva_fila = fila + df
        nueva_columna = columna + dc

        if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3:

            nueva_posicion = nueva_fila * 3 + nueva_columna

            nuevo_estado = list(estado)

            nuevo_estado[posicion], nuevo_estado[nueva_posicion] = (
                nuevo_estado[nueva_posicion],
                nuevo_estado[posicion],
            )

            resultado.append(tuple(nuevo_estado))

    return resultado


def bfs(
    inicio=INICIO_PUZZLE,
    meta=META_PUZZLE,
    max_nodos=50000,
):
    """
    Búsqueda en amplitud (BFS).

    max_nodos evita que una simulación se quede ejecutándose
    indefinidamente.
    """

    cola = deque()

    cola.append((inicio, []))

    visitados = {inicio}

    nodos = 0

    while cola:

        estado, camino = cola.popleft()

        nodos += 1

        if estado == meta:
            return camino, nodos

        if nodos >= max_nodos:
            return None, nodos

        for nuevo in movimientos(estado):

            if nuevo not in visitados:

                visitados.add(nuevo)

                cola.append(
                    (
                        nuevo,
                        camino + [nuevo],
                    )
                )

    return None, nodos


def dfs(
    inicio=INICIO_PUZZLE,
    meta=META_PUZZLE,
    max_nodos=50000,
):
    """
    Búsqueda en profundidad (DFS).

    max_nodos evita que una simulación se quede ejecutándose
    indefinidamente.
    """

    pila = []

    pila.append((inicio, []))

    visitados = {inicio}

    nodos = 0

    while pila:

        estado, camino = pila.pop()

        nodos += 1

        if estado == meta:
            return camino, nodos

        if nodos >= max_nodos:
            return None, nodos

        for nuevo in movimientos(estado):

            if nuevo not in visitados:

                visitados.add(nuevo)

                pila.append(
                    (
                        nuevo,
                        camino + [nuevo],
                    )
                )

    return None, nodos


def resolver(
    algoritmo,
    inicio=INICIO_PUZZLE,
    meta=META_PUZZLE,
    max_nodos=50000,
):
    """Ejecuta BFS o DFS."""

    algoritmo = algoritmo.upper()

    if algoritmo == "BFS":

        return bfs(
            inicio,
            meta,
            max_nodos,
        )

    if algoritmo == "DFS":

        return dfs(
            inicio,
            meta,
            max_nodos,
        )

    raise ValueError(
        "El algoritmo debe ser BFS o DFS."
    )


if __name__ == "__main__":

    for algoritmo in ("BFS", "DFS"):

        solucion, nodos = resolver(
            algoritmo
        )

        print()
        print(algoritmo)

        print(
            "Nodos:",
            nodos
        )

        print(
            "Movimientos:",
            len(solucion)
            if solucion is not None
            else "Sin solución"
        )
        print(f"\n{algoritmo}")
        print("Nodos:", nodos)
        print("Movimientos:", len(solucion) if solucion is not None else "Sin solución")
