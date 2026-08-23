from collections import deque


def bfs_mochila(pesos, valores, capacidad):
    """
    Resuelve el problema de la mochila 0/1 utilizando
    búsqueda en anchura (BFS).

    Parámetros:
        pesos: lista con el peso de cada objeto.
        valores: lista con el valor de cada objeto.
        capacidad: capacidad máxima de la mochila.

    Retorna:
        mejor_valor: valor máximo encontrado.
        mejor_seleccion: índices de los objetos seleccionados.
        nodos_explorados: cantidad de estados procesados.
    """

    cantidad_objetos = len(pesos)

    # La cola almacena los estados pendientes por explorar.
    # Cada estado tiene:
    # (indice, peso_actual, valor_actual, objetos_seleccionados)
    cola = deque()

    # Estado inicial:
    # todavía no se ha evaluado ningún objeto,
    # el peso y el valor acumulados son cero.
    cola.append((0, 0, 0, []))

    mejor_valor = 0
    mejor_seleccion = []

    nodos_explorados = 0

    while cola:

        # BFS extrae siempre el primer elemento de la cola.
        indice, peso_actual, valor_actual, seleccionados = cola.popleft()

        nodos_explorados += 1

        # Si el valor de este estado supera al mejor encontrado,
        # se actualiza la mejor solución.
        if valor_actual > mejor_valor:
            mejor_valor = valor_actual
            mejor_seleccion = seleccionados.copy()

        # Si ya se evaluaron todos los objetos,
        # no se generan nuevos estados.
        if indice == cantidad_objetos:
            continue

        # Primera posibilidad:
        # no seleccionar el objeto actual.
        cola.append(
            (
                indice + 1,
                peso_actual,
                valor_actual,
                seleccionados.copy()
            )
        )

        # Segunda posibilidad:
        # seleccionar el objeto actual.
        nuevo_peso = peso_actual + pesos[indice]

        # Solo se genera este estado si la capacidad
        # máxima de la mochila no es superada.
        if nuevo_peso <= capacidad:

            nuevo_valor = valor_actual + valores[indice]

            nueva_seleccion = seleccionados + [indice]

            cola.append(
                (
                    indice + 1,
                    nuevo_peso,
                    nuevo_valor,
                    nueva_seleccion
                )
            )

    return mejor_valor, mejor_seleccion, nodos_explorados


def dfs_mochila(pesos, valores, capacidad):
    """
    Resuelve el problema de la mochila 0/1 utilizando
    búsqueda en profundidad (DFS).

    Parámetros:
        pesos: lista con el peso de cada objeto.
        valores: lista con el valor de cada objeto.
        capacidad: capacidad máxima de la mochila.

    Retorna:
        mejor_valor: valor máximo encontrado.
        mejor_seleccion: índices de los objetos seleccionados.
        nodos_explorados: cantidad de estados procesados.
    """

    cantidad_objetos = len(pesos)

    # DFS utiliza una pila.
    # El último estado agregado será el primero en procesarse.
    pila = []

    # Estado inicial.
    pila.append((0, 0, 0, []))

    mejor_valor = 0
    mejor_seleccion = []

    nodos_explorados = 0

    while pila:

        # pop() extrae el último elemento agregado.
        indice, peso_actual, valor_actual, seleccionados = pila.pop()

        nodos_explorados += 1

        if valor_actual > mejor_valor:
            mejor_valor = valor_actual
            mejor_seleccion = seleccionados.copy()

        if indice == cantidad_objetos:
            continue

        # Se agrega primero la alternativa de no tomar el objeto.
        # Debido al funcionamiento LIFO de la pila,
        # la alternativa de tomar el objeto será explorada primero.
        pila.append(
            (
                indice + 1,
                peso_actual,
                valor_actual,
                seleccionados.copy()
            )
        )

        nuevo_peso = peso_actual + pesos[indice]

        if nuevo_peso <= capacidad:

            nuevo_valor = valor_actual + valores[indice]

            nueva_seleccion = seleccionados + [indice]

            pila.append(
                (
                    indice + 1,
                    nuevo_peso,
                    nuevo_valor,
                    nueva_seleccion
                )
            )

    return mejor_valor, mejor_seleccion, nodos_explorados


def mostrar_resultado(
    nombre_algoritmo,
    mejor_valor,
    seleccionados,
    pesos,
    valores,
    nodos_explorados
):
    """
    Muestra de forma legible la solución obtenida
    por BFS o DFS.
    """

    peso_total = sum(pesos[i] for i in seleccionados)

    print()
    print(nombre_algoritmo)
    print("Valor óptimo:", mejor_valor)
    print("Peso utilizado:", peso_total)
    print("Nodos explorados:", nodos_explorados)

    print("Objetos seleccionados:")

    for indice in seleccionados:
        print(
            f"Objeto {indice + 1}: "
            f"peso = {pesos[indice]}, "
            f"valor = {valores[indice]}"
        )


if __name__ == "__main__":

    # Caso de prueba inicial.
    # Se utilizan pocos objetos para comprobar
    # que BFS y DFS están funcionando correctamente.

    pesos = [2, 3, 4, 5]
    valores = [3, 4, 5, 8]

    capacidad = 8

    resultado_bfs = bfs_mochila(
        pesos,
        valores,
        capacidad
    )

    resultado_dfs = dfs_mochila(
        pesos,
        valores,
        capacidad
    )

    valor_bfs, seleccion_bfs, nodos_bfs = resultado_bfs

    valor_dfs, seleccion_dfs, nodos_dfs = resultado_dfs

    mostrar_resultado(
        "BFS",
        valor_bfs,
        seleccion_bfs,
        pesos,
        valores,
        nodos_bfs
    )

    mostrar_resultado(
        "DFS",
        valor_dfs,
        seleccion_dfs,
        pesos,
        valores,
        nodos_dfs
    )

    print()

    if valor_bfs == valor_dfs:
        print(
            "Validación correcta: BFS y DFS encontraron "
            "el mismo valor óptimo."
        )
    else:
        print(
            "Advertencia: BFS y DFS obtuvieron "
            "resultados diferentes."
        )