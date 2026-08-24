# N-Reinas: comparación BFS vs DFS

Implementación y análisis experimental de **Breadth-First Search (BFS)** y **Depth-First Search (DFS)** aplicados al problema de las N-Reinas.

## Objetivo

Comparar principalmente:

- Tiempo de ejecución.
- Memoria pico utilizada.

También se registra la cantidad de nodos explorados como métrica auxiliar.

## Representación del estado

El tablero se representa mediante una lista donde el índice corresponde a la columna y el valor almacenado corresponde a la fila en la que se ubica la reina.

Ejemplo para N=4:

```python
tablero = [1, 3, 0, 2]
```

Esto representa una reina por columna y una solución válida del problema.

## Archivos

```text
Nreinas/
├── n_reinas.py
├── bfs.py
├── dfs.py
├── medicion.py
├── simulaciones.py
├── analisis_resultados.py
├── graficas.py
├── arboles.py
├── visualizacion.py
├── comparar_maquinas.py
├── main.py
└── README.md
```

## BFS

`bfs.py` utiliza una cola FIFO (`deque`). Los estados parciales se exploran por niveles. El algoritmo se detiene cuando encuentra la primera solución completa.

## DFS

`dfs.py` utiliza una pila LIFO. El algoritmo profundiza una rama válida antes de regresar a otras alternativas y se detiene cuando encuentra la primera solución completa.

## Medición

`medicion.py` utiliza:

- `time.perf_counter()` para medir tiempo.
- `tracemalloc` para registrar memoria pico.
- Un contador explícito para los nodos procesados.

## Diseño experimental

Se evaluaron valores de N entre 4 y 13.

| N | Repeticiones por algoritmo |
|---:|---:|
| 4 a 10 | 100 |
| 11 | 50 |
| 12 | 20 |
| 13 | 10 |

La reducción de repeticiones para N grandes se debe al fuerte crecimiento del costo de BFS.

Para un mismo valor de N, las repeticiones ejecutan el mismo problema determinista. Por tanto, sirven principalmente para observar la variabilidad de las mediciones de tiempo y memoria y no representan instancias aleatorias diferentes.

## Resultados actuales

Los resultados agregados se encuentran en:

```text
resultados/nreinas/datos/
├── resultados.csv
├── resumen.csv
├── comparacion.csv
└── info_maquina.json
```

Los datos guardados muestran un crecimiento muy marcado de BFS a medida que aumenta N. En N=13, el promedio almacenado es aproximadamente:

- BFS: 112 s, 234.770 KB y 4.601.179 nodos.
- DFS: 0,0012 s, 1,72 KB y 112 nodos.

Estos valores corresponden a las implementaciones y al equipo registrados en los archivos de resultados; no deben interpretarse como tiempos universales de BFS y DFS.

## Gráficas principales

`graficas.py` genera cuatro visualizaciones principales:

1. Tiempo promedio BFS vs DFS por N.
2. Memoria pico promedio BFS vs DFS por N.
3. Nodos explorados promedio BFS vs DFS por N.
4. Ratio BFS/DFS para tiempo, memoria y nodos.

Se utiliza escala logarítmica porque, para N grandes, las diferencias abarcan varios órdenes de magnitud.

## Árbol de búsqueda

`arboles.py` permite visualizar un tamaño pequeño, recomendado N=4, para observar el orden de recorrido de BFS y DFS sobre el mismo árbol de estados factibles.

## Ejecución

Desde la raíz del repositorio:

```bash
python Nreinas/main.py
```

Para generar únicamente el análisis a partir del CSV existente:

```bash
python Nreinas/analisis_resultados.py
```

Para regenerar las gráficas desde los resultados existentes:

```bash
python Nreinas/graficas.py
```

Para visualizar el árbol de N=4:

```bash
python Nreinas/arboles.py 4
```

## Interpretación

En este problema el objetivo es encontrar una primera configuración válida completa. BFS debe avanzar nivel por nivel y conserva una frontera amplia, mientras DFS puede alcanzar rápidamente una solución profundizando una rama válida. Esto explica el comportamiento experimental observado, donde DFS utiliza muchos menos nodos, tiempo y memoria para los tamaños evaluados.
