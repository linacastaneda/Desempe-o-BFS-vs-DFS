"""
Visualización del árbol de búsqueda para N-Reinas (N pequeño).
Muestra cómo BFS y DFS exploran el espacio de estados.
"""

from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
from n_reinas import es_valida, es_solucion_completa


def construir_arbol_nreinas(n):
    """
    Construye el árbol de decisiones del problema de N-Reinas.
    
    Cada nodo representa un estado parcial del tablero.
    Nivel = columna que se está evaluando.
    """
    grafo = nx.DiGraph()
    contador_nodos = 0
    raiz = contador_nodos
    
    grafo.add_node(raiz, tablero=[], columna=0, profundidad=0)
    contador_nodos += 1
    
    cola = deque()
    cola.append(raiz)
    
    while cola:
        nodo_actual = cola.popleft()
        datos = grafo.nodes[nodo_actual]
        tablero = datos["tablero"]
        columna = datos["columna"]
        profundidad = datos["profundidad"]
        
        # Si ya es solución completa o no hay más columnas, es hoja
        if es_solucion_completa(tablero, n) or columna >= n:
            continue
        
        # Generar hijos: probar cada fila en esta columna
        for fila in range(n):
            if es_valida(tablero, fila, columna):
                nuevo_tablero = tablero + [fila]
                hijo = contador_nodos
                contador_nodos += 1
                
                es_sol = es_solucion_completa(nuevo_tablero, n)
                
                grafo.add_node(
                    hijo,
                    tablero=nuevo_tablero,
                    columna=columna + 1,
                    profundidad=profundidad + 1,
                    es_solucion=es_sol
                )
                
                grafo.add_edge(nodo_actual, hijo, decision=f"Q en ({fila},{columna})")
                cola.append(hijo)
    
    return grafo, raiz


def obtener_orden_bfs(grafo, raiz):
    """Orden de visita BFS (nivel por nivel)."""
    orden = []
    cola = deque([raiz])
    
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        for hijo in grafo.successors(nodo):
            cola.append(hijo)
    return orden


def obtener_orden_dfs(grafo, raiz):
    """Orden de visita DFS (profundidad)."""
    orden = []
    pila = [raiz]
    
    while pila:
        nodo = pila.pop()
        orden.append(nodo)
        hijos = list(grafo.successors(nodo))
        # Para que explore en orden natural, invertimos
        for hijo in reversed(hijos):
            pila.append(hijo)
    return orden


def calcular_posiciones(grafo, raiz):
    """Calcula posiciones jerárquicas para dibujar el árbol."""
    posiciones = {}
    niveles = {}
    
    cola = deque([(raiz, 0)])
    
    while cola:
        nodo, nivel = cola.popleft()
        
        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(nodo)
        
        for hijo in grafo.successors(nodo):
            cola.append((hijo, nivel + 1))
    
    # Asignar coordenadas
    for nivel, nodos in niveles.items():
        cantidad = len(nodos)
        for pos, nodo in enumerate(nodos):
            x = pos - (cantidad - 1) / 2
            y = -nivel
            posiciones[nodo] = (x, y)
    
    return posiciones


def obtener_soluciones(grafo):
    """Encuentra todos los nodos que son soluciones completas."""
    soluciones = []
    for nodo in grafo.nodes:
        if grafo.nodes[nodo].get("es_solucion", False):
            soluciones.append(nodo)
    return soluciones


def crear_etiquetas(grafo, orden, soluciones):
    """Crea etiquetas para los nodos."""
    posiciones_orden = {nodo: i+1 for i, nodo in enumerate(orden)}
    etiquetas = {}
    
    for nodo in grafo.nodes:
        datos = grafo.nodes[nodo]
        visita = posiciones_orden.get(nodo, 0)
        tablero_str = str(datos["tablero"])
        
        etiqueta = f"#{visita}\n{tablero_str}"
        if nodo in soluciones:
            etiqueta += "\n[SOLUCION]"
        etiquetas[nodo] = etiqueta
    
    return etiquetas


def mostrar_arbol(grafo, raiz, orden, titulo, n):
    """Dibuja el árbol de búsqueda."""
    posiciones = calcular_posiciones(grafo, raiz)
    soluciones = obtener_soluciones(grafo)
    etiquetas = crear_etiquetas(grafo, orden, soluciones)
    etiquetas_aristas = nx.get_edge_attributes(grafo, "decision")
    
    plt.figure(figsize=(16, 10))
    
    # Nodos normales
    nx.draw(
        grafo,
        posiciones,
        labels=etiquetas,
        with_labels=True,
        node_size=2500,
        font_size=7,
        node_color=['lightgreen' if n in soluciones else 'lightblue' for n in grafo.nodes],
        edge_color='gray',
        arrows=True,
        arrowsize=15
    )
    
    # Etiquetas de aristas
    nx.draw_networkx_edge_labels(
        grafo,
        posiciones,
        edge_labels=etiquetas_aristas,
        font_size=6
    )
    
    plt.title(f"{titulo}\nN-Reinas N={n} | Nodos: {grafo.number_of_nodes()} | Soluciones: {len(soluciones)}", 
              fontsize=14, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def imprimir_orden(orden, grafo, titulo):
    """Imprime el orden de visita en consola."""
    print(f"\n{titulo}:")
    for i, nodo in enumerate(orden, 1):
        tablero = grafo.nodes[nodo]["tablero"]
        es_sol = grafo.nodes[nodo].get("es_solucion", False)
        marca = " [SOL]" if es_sol else ""
        print(f"  {i:3d}. Nodo {nodo}: {tablero}{marca}")


def mostrar_arbol_comparado(n, guardar_como=None):
    """Muestra ambos árboles lado a lado."""
    print(f"\n{'='*50}")
    print(f"CONSTRUYENDO ÁRBOL DE BÚSQUEDA - N-REINAS N={n}")
    print(f"{'='*50}")
    
    grafo, raiz = construir_arbol_nreinas(n)
    
    orden_bfs = obtener_orden_bfs(grafo, raiz)
    orden_dfs = obtener_orden_dfs(grafo, raiz)
    
    soluciones = obtener_soluciones(grafo)
    
    print(f"\nNodos totales en el árbol: {grafo.number_of_nodes()}")
    print(f"Soluciones encontradas: {len(soluciones)}")
    
    imprimir_orden(orden_bfs[:20], grafo, "Primeros 20 nodos BFS")
    imprimir_orden(orden_dfs[:20], grafo, "Primeros 20 nodos DFS")
    
    if len(orden_bfs) > 20:
        print(f"  ... y {len(orden_bfs)-20} nodos más (BFS)")
    if len(orden_dfs) > 20:
        print(f"  ... y {len(orden_dfs)-20} nodos más (DFS)")
    
    # Mostrar soluciones
    print("\nSoluciones completas:")
    for nodo in soluciones:
        tablero = grafo.nodes[nodo]["tablero"]
        print(f"  {tablero}")
    
    # Dibujar árboles
    if guardar_como:
        import os
        carpeta = os.path.join("..", "resultados", "nreinas", "graficas", "arboles")
        os.makedirs(carpeta, exist_ok=True)
        
        # BFS
        posiciones = calcular_posiciones(grafo, raiz)
        soluciones = obtener_soluciones(grafo)
        etiquetas = crear_etiquetas(grafo, orden_bfs, soluciones)
        etiquetas_aristas = nx.get_edge_attributes(grafo, "decision")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 10))
        
        for ax, orden, titulo_ax in [(ax1, orden_bfs, "BFS - Nivel por nivel"), 
                                      (ax2, orden_dfs, "DFS - Profundidad")]:
            etiquetas_orden = crear_etiquetas(grafo, orden, soluciones)
            
            nx.draw(
                grafo, posiciones, ax=ax,
                labels=etiquetas_orden, with_labels=True,
                node_size=2000, font_size=6,
                node_color=['lightgreen' if n in soluciones else 'lightblue' for n in grafo.nodes],
                edge_color='gray', arrows=True, arrowsize=12
            )
            nx.draw_networkx_edge_labels(
                grafo, posiciones, ax=ax,
                edge_labels=etiquetas_aristas, font_size=5
            )
            ax.set_title(f"{titulo_ax} (N={n})", fontsize=12, fontweight='bold')
            ax.axis("off")
        
        plt.tight_layout()
        ruta = os.path.join(carpeta, f"arbol_n{n}.png")
        plt.savefig(ruta, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"\nÁrbol guardado en: {ruta}")
    else:
        print("\n--- Árbol BFS ---")
        mostrar_arbol(grafo, raiz, orden_bfs, f"BFS - N-Reinas N={n}", n)
        
        print("\n--- Árbol DFS ---")
        mostrar_arbol(grafo, raiz, orden_dfs, f"DFS - N-Reinas N={n}", n)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print(f"Visualizando árbol para N={n}...")
    mostrar_arbol_comparado(n)