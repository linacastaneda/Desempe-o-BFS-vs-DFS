from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


def construir_arbol_mochila(pesos, valores, capacidad):
    """
    Construye el árbol de decisiones del problema
    de la mochila 0/1.

    Cada nodo representa un estado con:

        indice:
            objeto que se evaluará a continuación.

        peso:
            peso acumulado de los objetos seleccionados.

        valor:
            valor acumulado de los objetos seleccionados.

        seleccionados:
            índices de los objetos incluidos en la mochila.

    Cada objeto genera como máximo dos decisiones:

        - No tomar el objeto.
        - Tomar el objeto.

    La opción de tomar solo se crea si no supera
    la capacidad máxima de la mochila.

    Retorna:
        grafo:
            árbol de estados representado con NetworkX.

        raiz:
            identificador del nodo inicial.
    """

    grafo = nx.DiGraph()

    contador_nodos = 0

    raiz = contador_nodos

    grafo.add_node(
        raiz,
        indice=0,
        peso=0,
        valor=0,
        seleccionados=[]
    )

    contador_nodos += 1

    cola = deque()

    cola.append(raiz)

    while cola:

        nodo_actual = cola.popleft()

        datos = grafo.nodes[nodo_actual]

        indice = datos["indice"]
        peso_actual = datos["peso"]
        valor_actual = datos["valor"]
        seleccionados = datos["seleccionados"]

        # Si ya se evaluaron todos los objetos,
        # el nodo es una hoja del árbol.
        if indice == len(pesos):
            continue

        # Se crea primero la opción de no tomar
        # el objeto actual.
        nodo_no_tomar = contador_nodos

        contador_nodos += 1

        grafo.add_node(
            nodo_no_tomar,
            indice=indice + 1,
            peso=peso_actual,
            valor=valor_actual,
            seleccionados=seleccionados.copy()
        )

        grafo.add_edge(
            nodo_actual,
            nodo_no_tomar,
            decision=f"No tomar {indice + 1}"
        )

        cola.append(nodo_no_tomar)

        # Se calcula el peso que tendría la mochila
        # si se seleccionara el objeto actual.
        nuevo_peso = peso_actual + pesos[indice]

        # Solo se crea la rama "Tomar" si la capacidad
        # máxima no es superada.
        if nuevo_peso <= capacidad:

            nodo_tomar = contador_nodos

            contador_nodos += 1

            nuevo_valor = (
                valor_actual
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
                nodo_actual,
                nodo_tomar,
                decision=f"Tomar {indice + 1}"
            )

            cola.append(nodo_tomar)

    return grafo, raiz


def obtener_orden_bfs(grafo, raiz):
    """
    Obtiene el orden en el cual BFS visita
    los nodos del árbol.

    BFS utiliza una cola FIFO:

        First In - First Out.

    Esto hace que el árbol sea recorrido
    nivel por nivel.
    """

    orden = []

    cola = deque()

    cola.append(raiz)

    while cola:

        nodo = cola.popleft()

        orden.append(nodo)

        for hijo in grafo.successors(nodo):

            cola.append(hijo)

    return orden


def obtener_orden_dfs(grafo, raiz):
    """
    Obtiene el orden en el cual DFS visita
    los nodos del árbol.

    DFS utiliza una pila LIFO:

        Last In - First Out.

    Esta función reproduce el mismo orden
    utilizado en dfs_mochila().

    En el algoritmo original se agrega:

        1. No tomar.
        2. Tomar.

    Como la pila es LIFO, la opción
    "Tomar" se procesa primero.
    """

    orden = []

    pila = [raiz]

    while pila:

        nodo = pila.pop()

        orden.append(nodo)

        hijos = list(
            grafo.successors(nodo)
        )

        # Los hijos fueron creados en el orden:
        #
        # 1. No tomar.
        # 2. Tomar.
        #
        # Se introducen en la pila en ese mismo
        # orden para que "Tomar", al ser el último,
        # salga primero.

        for hijo in hijos:

            pila.append(hijo)

    return orden


def calcular_posiciones(grafo, raiz):
    """
    Calcula las posiciones de los nodos
    para dibujar el árbol jerárquicamente.

    Los nodos del mismo nivel aparecen
    aproximadamente a la misma altura.
    """

    posiciones = {}

    niveles = {}

    cola = deque()

    cola.append(
        (
            raiz,
            0
        )
    )

    while cola:

        nodo, nivel = cola.popleft()

        if nivel not in niveles:

            niveles[nivel] = []

        niveles[nivel].append(
            nodo
        )

        for hijo in grafo.successors(nodo):

            cola.append(
                (
                    hijo,
                    nivel + 1
                )
            )

    # Se asignan coordenadas a los nodos
    # según el nivel al que pertenecen.
    for nivel, nodos in niveles.items():

        cantidad = len(nodos)

        for posicion, nodo in enumerate(nodos):

            x = posicion - (
                cantidad - 1
            ) / 2

            y = -nivel

            posiciones[nodo] = (
                x,
                y
            )

    return posiciones


def obtener_mejor_valor(grafo):
    """
    Busca el mayor valor acumulado presente
    dentro de todos los nodos del árbol.

    Ese valor corresponde al valor óptimo
    encontrado para la instancia.
    """

    mejor_valor = 0

    for nodo in grafo.nodes:

        valor = grafo.nodes[nodo]["valor"]

        if valor > mejor_valor:

            mejor_valor = valor

    return mejor_valor


def obtener_nodos_optimos(
    grafo,
    mejor_valor
):
    """
    Obtiene todos los nodos cuyo valor
    acumulado corresponde al valor óptimo.

    Puede existir más de una combinación
    diferente de objetos con el mismo
    valor óptimo.
    """

    nodos_optimos = []

    for nodo in grafo.nodes:

        datos = grafo.nodes[nodo]

        if datos["valor"] == mejor_valor:

            nodos_optimos.append(nodo)

    return nodos_optimos


def crear_etiquetas(
    grafo,
    orden,
    nodos_optimos
):
    """
    Crea las etiquetas mostradas dentro
    de cada nodo.

    Cada etiqueta incluye:

        # número de visita
        P = peso acumulado
        V = valor acumulado

    Los nodos con solución óptima incluyen
    además el texto:

        ÓPTIMO
    """

    posiciones_orden = {}

    for numero_visita, nodo in enumerate(
        orden,
        start=1
    ):

        posiciones_orden[nodo] = numero_visita

    etiquetas = {}

    for nodo in grafo.nodes:

        datos = grafo.nodes[nodo]

        visita = posiciones_orden[nodo]

        etiqueta = (
            f"#{visita}\n"
            f"P={datos['peso']}\n"
            f"V={datos['valor']}"
        )

        if nodo in nodos_optimos:

            etiqueta += "\nÓPTIMO"

        etiquetas[nodo] = etiqueta

    return etiquetas


def mostrar_arbol(
    grafo,
    raiz,
    orden,
    titulo
):
    """
    Dibuja gráficamente el árbol
    de decisiones de la mochila.

    El número mostrado dentro de cada nodo
    representa el orden en que el algoritmo
    visitó ese estado.
    """

    posiciones = calcular_posiciones(
        grafo,
        raiz
    )

    mejor_valor = obtener_mejor_valor(
        grafo
    )

    nodos_optimos = obtener_nodos_optimos(
        grafo,
        mejor_valor
    )

    etiquetas = crear_etiquetas(
        grafo,
        orden,
        nodos_optimos
    )

    etiquetas_aristas = (
        nx.get_edge_attributes(
            grafo,
            "decision"
        )
    )

    plt.figure(
        figsize=(18, 10)
    )

    # Se dibujan primero todos los nodos.
    nx.draw(
        grafo,
        posiciones,
        labels=etiquetas,
        with_labels=True,
        node_size=2200,
        font_size=8,
        arrows=True
    )

    # Se muestran las decisiones:
    #
    # Tomar objeto
    # No tomar objeto
    nx.draw_networkx_edge_labels(
        grafo,
        posiciones,
        edge_labels=etiquetas_aristas,
        font_size=7
    )

    # Se dibujan nuevamente los nodos óptimos
    # con un tamaño mayor para destacarlos.
    nx.draw_networkx_nodes(
        grafo,
        posiciones,
        nodelist=nodos_optimos,
        node_size=2800
    )

    # Se vuelven a dibujar las etiquetas
    # de los nodos óptimos.
    etiquetas_optimas = {
        nodo: etiquetas[nodo]
        for nodo in nodos_optimos
    }

    nx.draw_networkx_labels(
        grafo,
        posiciones,
        labels=etiquetas_optimas,
        font_size=8
    )

    plt.title(
        titulo
    )

    plt.axis("off")

    plt.tight_layout()

    plt.show()


def mostrar_datos_problema(
    pesos,
    valores,
    capacidad
):
    """
    Muestra en consola los datos utilizados
    para construir el árbol.
    """

    print()
    print("PROBLEMA DE LA MOCHILA")

    print(
        "Capacidad:",
        capacidad
    )

    print()

    print("Objetos:")

    for i in range(len(pesos)):

        print(
            f"Objeto {i + 1}: "
            f"peso = {pesos[i]}, "
            f"valor = {valores[i]}"
        )


def mostrar_resultado_arbol(
    grafo,
    mejor_valor
):
    """
    Muestra en consola las combinaciones
    correspondientes al valor óptimo.
    """

    print()
    print(
        "Valor óptimo:",
        mejor_valor
    )

    print(
        "Soluciones óptimas encontradas:"
    )

    for nodo in grafo.nodes:

        datos = grafo.nodes[nodo]

        if datos["valor"] == mejor_valor:

            seleccionados = datos[
                "seleccionados"
            ]

            # Solo interesa mostrar estados
            # que contengan realmente objetos.
            if seleccionados:

                objetos = [
                    indice + 1
                    for indice
                    in seleccionados
                ]

                print(
                    "Objetos:",
                    objetos,
                    "| Peso:",
                    datos["peso"],
                    "| Valor:",
                    datos["valor"]
                )


if __name__ == "__main__":

    # Instancia pequeña utilizada únicamente
    # para visualizar claramente el árbol.
    #
    # No se utilizan las mochilas grandes
    # de las 100 simulaciones porque sus árboles
    # contienen miles de nodos y serían ilegibles.

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

    mostrar_datos_problema(
        pesos,
        valores,
        capacidad
    )

    # Se construye un único árbol.
    #
    # BFS y DFS utilizan exactamente el mismo
    # espacio de estados.
    grafo, raiz = construir_arbol_mochila(
        pesos,
        valores,
        capacidad
    )

    # Se calcula el orden de recorrido BFS.
    orden_bfs = obtener_orden_bfs(
        grafo,
        raiz
    )

    # Se calcula el orden de recorrido DFS.
    orden_dfs = obtener_orden_dfs(
        grafo,
        raiz
    )

    mejor_valor = obtener_mejor_valor(
        grafo
    )

    mostrar_resultado_arbol(
        grafo,
        mejor_valor
    )

    print()

    print(
        "Cantidad total de nodos:",
        grafo.number_of_nodes()
    )

    print()

    print(
        "Orden de recorrido BFS:"
    )

    print(
        orden_bfs
    )

    print()

    print(
        "Orden de recorrido DFS:"
    )

    print(
        orden_dfs
    )

    # Árbol con numeración según BFS.
    mostrar_arbol(
        grafo,
        raiz,
        orden_bfs,
        "Árbol del problema de la mochila - Recorrido BFS"
    )

    # Árbol con numeración según DFS.
    mostrar_arbol(
        grafo,
        raiz,
        orden_dfs,
        "Árbol del problema de la mochila - Recorrido DFS"
    )