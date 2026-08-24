"""
Implementación de BFS y DFS para el Puzzle 3x3.

El objetivo es comparar el desempeño de ambos algoritmos
principalmente en:

- Tiempo de ejecución.
- Consumo de memoria.

Cada estado del Puzzle se representa mediante una tupla
de nueve posiciones.

El valor 0 representa el espacio vacío.

Ejemplo:

    1 2 3
    5 0 6
    4 7 8

Se representa como:

    (1, 2, 3, 5, 0, 6, 4, 7, 8)
"""

from collections import deque


# Estado inicial utilizado para pruebas individuales.
INICIO_PUZZLE = (
    1, 2, 3,
    5, 0, 6,
    4, 7, 8
)


# Estado objetivo del Puzzle 3x3.
META_PUZZLE = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)


def movimientos(estado):
    """
    Genera todos los estados que pueden obtenerse
    realizando un movimiento válido desde el estado actual.

    El espacio vacío está representado por el número 0.

    Parámetros:
        estado:
            Tupla de nueve elementos que representa
            la configuración actual del puzzle.

    Retorna:
        Lista de estados vecinos válidos.
    """

    resultado = []

    # Se busca la posición del espacio vacío.
    posicion = estado.index(0)

    # Se convierte la posición lineal en fila y columna.
    fila = posicion // 3
    columna = posicion % 3

    # Movimientos posibles del espacio vacío:
    #
    # arriba
    # abajo
    # izquierda
    # derecha
    direcciones = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    for cambio_fila, cambio_columna in direcciones:

        nueva_fila = fila + cambio_fila
        nueva_columna = columna + cambio_columna

        # Se comprueba que el movimiento permanezca
        # dentro del tablero 3x3.
        if (
            0 <= nueva_fila < 3
            and 0 <= nueva_columna < 3
        ):

            nueva_posicion = (
                nueva_fila * 3
                + nueva_columna
            )

            # Se crea una copia temporal del estado
            # para intercambiar el espacio vacío.
            nuevo_estado = list(estado)

            nuevo_estado[
                posicion
            ], nuevo_estado[
                nueva_posicion
            ] = (
                nuevo_estado[nueva_posicion],
                nuevo_estado[posicion],
            )

            resultado.append(
                tuple(nuevo_estado)
            )

    return resultado


def reconstruir_camino(
    padres,
    inicio,
    meta
):
    """
    Reconstruye el camino desde el estado inicial
    hasta el estado objetivo.

    En lugar de guardar una copia completa del camino
    dentro de cada nodo, los algoritmos almacenan
    únicamente el padre de cada estado.

    Esto reduce considerablemente el consumo de memoria.

    Parámetros:
        padres:
            Diccionario que relaciona cada estado
            con el estado desde el cual fue generado.

        inicio:
            Estado inicial.

        meta:
            Estado objetivo.

    Retorna:
        Lista de estados desde el primer movimiento
        hasta la meta.

        El estado inicial no se incluye para mantener
        el mismo formato utilizado anteriormente.
    """

    camino = []

    estado_actual = meta

    while estado_actual != inicio:

        camino.append(
            estado_actual
        )

        estado_actual = padres[
            estado_actual
        ]

    # El camino se construyó desde la meta
    # hacia el inicio, por lo que debe invertirse.
    camino.reverse()

    return camino


def bfs(
    inicio=INICIO_PUZZLE,
    meta=META_PUZZLE,
    max_nodos=50000
):
    """
    Resuelve el Puzzle 3x3 mediante búsqueda
    en anchura BFS.

    BFS utiliza una cola FIFO:

        First In, First Out.

    Esto hace que los estados sean explorados
    por niveles de profundidad.

    Parámetros:
        inicio:
            Estado inicial del puzzle.

        meta:
            Estado objetivo.

        max_nodos:
            Número máximo de nodos que pueden
            ser explorados antes de detener
            la búsqueda.

    Retorna:
        solucion:
            Camino desde el estado inicial
            hasta la meta.

            Retorna None si no se encuentra
            solución antes del límite.

        nodos:
            Cantidad de estados explorados.
    """

    # Caso especial:
    # el estado inicial ya es la meta.
    if inicio == meta:
        return [], 1

    # BFS utiliza una cola.
    cola = deque()

    cola.append(
        inicio
    )

    # Permite evitar estados repetidos.
    visitados = {
        inicio
    }

    # Guarda únicamente la relación entre
    # cada estado y su padre.
    padres = {
        inicio: None
    }

    nodos = 0

    while cola:

        # BFS obtiene el estado más antiguo
        # almacenado en la cola.
        estado = cola.popleft()

        nodos += 1

        # Si se alcanzó la meta,
        # se reconstruye el camino.
        if estado == meta:

            camino = reconstruir_camino(
                padres,
                inicio,
                meta
            )

            return camino, nodos

        # Se detiene la búsqueda si se alcanza
        # el límite experimental.
        if nodos >= max_nodos:

            return None, nodos

        # Se generan los estados vecinos.
        for nuevo_estado in movimientos(
            estado
        ):

            # Solo se procesan estados
            # que no hayan sido visitados.
            if nuevo_estado not in visitados:

                visitados.add(
                    nuevo_estado
                )

                # Se registra desde qué estado
                # fue generado.
                padres[
                    nuevo_estado
                ] = estado

                # El nuevo estado queda pendiente
                # en la cola.
                cola.append(
                    nuevo_estado
                )

    return None, nodos


def dfs(
    inicio=INICIO_PUZZLE,
    meta=META_PUZZLE,
    max_nodos=50000
):
    """
    Resuelve el Puzzle 3x3 mediante búsqueda
    en profundidad DFS.

    DFS utiliza una pila LIFO:

        Last In, First Out.

    Esto provoca que el algoritmo profundice
    una rama antes de regresar a explorar
    otras alternativas.

    Parámetros:
        inicio:
            Estado inicial del puzzle.

        meta:
            Estado objetivo.

        max_nodos:
            Número máximo de nodos que pueden
            ser explorados antes de detener
            la búsqueda.

    Retorna:
        solucion:
            Camino encontrado desde el estado
            inicial hasta la meta.

            Retorna None si no se encuentra
            solución antes del límite.

        nodos:
            Cantidad de estados explorados.
    """

    if inicio == meta:
        return [], 1

    # DFS utiliza una pila.
    pila = []

    pila.append(
        inicio
    )

    visitados = {
        inicio
    }

    padres = {
        inicio: None
    }

    nodos = 0

    while pila:

        # DFS obtiene el último estado
        # agregado a la pila.
        estado = pila.pop()

        nodos += 1

        if estado == meta:

            camino = reconstruir_camino(
                padres,
                inicio,
                meta
            )

            return camino, nodos

        if nodos >= max_nodos:

            return None, nodos

        # Se generan los estados vecinos.
        for nuevo_estado in movimientos(
            estado
        ):

            if nuevo_estado not in visitados:

                visitados.add(
                    nuevo_estado
                )

                padres[
                    nuevo_estado
                ] = estado

                pila.append(
                    nuevo_estado
                )

    return None, nodos


def resolver(
    algoritmo,
    inicio=INICIO_PUZZLE,
    meta=META_PUZZLE,
    max_nodos=50000
):
    """
    Ejecuta BFS o DFS dependiendo del nombre
    recibido como parámetro.

    Esta función permite utilizar una única
    interfaz desde medicion.py y simulaciones.py.

    Parámetros:
        algoritmo:
            "BFS" o "DFS".

        inicio:
            Estado inicial.

        meta:
            Estado objetivo.

        max_nodos:
            Límite de nodos explorados.

    Retorna:
        Resultado producido por BFS o DFS.
    """

    algoritmo = algoritmo.upper()

    if algoritmo == "BFS":

        return bfs(
            inicio,
            meta,
            max_nodos
        )

    if algoritmo == "DFS":

        return dfs(
            inicio,
            meta,
            max_nodos
        )

    raise ValueError(
        "El algoritmo debe ser BFS o DFS."
    )


def mostrar_tablero(estado):
    """
    Muestra un estado del Puzzle en forma
    de tablero 3x3.
    """

    for fila in range(3):

        inicio_fila = fila * 3

        elementos = estado[
            inicio_fila:
            inicio_fila + 3
        ]

        print(
            elementos
        )


if __name__ == "__main__":

    print()
    print("ESTADO INICIAL")

    mostrar_tablero(
        INICIO_PUZZLE
    )

    print()
    print("ESTADO OBJETIVO")

    mostrar_tablero(
        META_PUZZLE
    )

    for algoritmo in (
        "BFS",
        "DFS"
    ):

        solucion, nodos = resolver(
            algoritmo,
            INICIO_PUZZLE,
            META_PUZZLE
        )

        print()
        print(algoritmo)

        print(
            "Nodos explorados:",
            nodos
        )

        if solucion is not None:

            print(
                "Solución encontrada: Sí"
            )

            print(
                "Número de movimientos:",
                len(solucion)
            )

        else:

            print(
                "Solución encontrada: No"
            )

            print(
                "Se alcanzó el límite de nodos."
            )