# Desempeño BFS vs DFS

Proyecto académico para comparar experimentalmente los algoritmos **Breadth-First Search (BFS)** y **Depth-First Search (DFS)** en tres problemas con espacios de estados diferentes:

1. Puzzle 3x3.
2. N-Reinas.
3. Mochila 0/1.

El análisis se concentra principalmente en **tiempo de ejecución** y **memoria pico utilizada**. La cantidad de nodos explorados y, cuando aplica, la profundidad o longitud de la solución se usan como métricas auxiliares para explicar el comportamiento observado.

## Estructura del repositorio

```text
.
├── mochila/
│   ├── bfs_dfs_mochila.py
│   ├── medicion.py
│   ├── simulaciones.py
│   ├── analisis_resultados.py
│   ├── graficas.py
│   └── arboles.py
├── puzzle/
│   ├── bfs_dfs_puzzle.py
│   ├── medicion.py
│   ├── simulaciones.py
│   ├── analisis_resultados.py
│   ├── graficas.py
│   └── arboles.py
├── Nreinas/
│   ├── n_reinas.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── medicion.py
│   ├── simulaciones.py
│   ├── analisis_resultados.py
│   ├── graficas.py
│   ├── arboles.py
│   ├── visualizacion.py
│   ├── comparar_maquinas.py
│   └── main.py
├── resultados/
├── docs/
├── requirements.txt
└── .gitignore
```

## Metodología común

Las implementaciones se desarrollaron en Python. Para las mediciones se utilizaron:

- `time.perf_counter()` para medir tiempo de ejecución.
- `tracemalloc` para registrar memoria pico asignada durante la ejecución.
- Un contador explícito de nodos procesados como métrica auxiliar.

En cada comparación BFS y DFS reciben las mismas condiciones de entrada dentro de cada problema.

## Mochila 0/1

Cada estado representa la decisión de tomar o no tomar un objeto. BFS y DFS recorren el mismo árbol factible de decisiones, por lo que ambos encuentran el mismo valor óptimo y exploran la misma cantidad de nodos en cada instancia; la principal diferencia está en el orden de exploración y en la cantidad de estados que permanecen pendientes en memoria.

Se realizaron **100 instancias aleatorias**, distribuidas en cinco tamaños:

- 20 instancias con 5 objetos.
- 20 instancias con 8 objetos.
- 20 instancias con 10 objetos.
- 20 instancias con 12 objetos.
- 20 instancias con 15 objetos.

Los pesos se generan entre 1 y 15, los valores entre 1 y 30 y la capacidad corresponde aproximadamente al 40 % del peso total. Se utiliza `random.seed(42)` para reproducibilidad.

Resultado general: al aumentar el número de objetos, BFS presenta un crecimiento de memoria mucho mayor que DFS debido al tamaño de la frontera almacenada en la cola.

## Puzzle 3x3

Los estados iniciales se generan a partir del estado objetivo mediante **6 movimientos válidos aleatorios**, evitando la reversión inmediata del último movimiento. De esta manera todas las instancias generadas son solucionables.

Se realizaron **100 simulaciones** con semilla `42`. En cada simulación BFS y DFS reciben exactamente el mismo estado inicial.

Se estableció un límite experimental de **50.000 nodos por ejecución**. Las ejecuciones que alcanzan ese límite se identifican explícitamente y se analizan por separado de las búsquedas que terminan normalmente.

Resultados del conjunto actual:

- BFS completó 100 de 100 ejecuciones.
- DFS completó 51 de 100 ejecuciones.
- DFS alcanzó el límite de 50.000 nodos en 49 ejecuciones.

En estas instancias cercanas a la meta, BFS presentó menor tiempo y memoria. El análisis incluye resultados globales y resultados considerando únicamente ejecuciones completadas.

## N-Reinas

El tablero se representa mediante una lista donde el índice corresponde a la columna y el valor almacenado corresponde a la fila de la reina. Los sucesores se generan colocando una reina válida en la siguiente columna.

BFS y DFS buscan la **primera solución completa**. Para cada valor de N se repite el mismo problema, por lo que las repeticiones permiten observar principalmente la estabilidad de las mediciones de tiempo y memoria.

Se evaluaron los siguientes tamaños:

| N | Repeticiones por algoritmo |
|---:|---:|
| 4 a 10 | 100 |
| 11 | 50 |
| 12 | 20 |
| 13 | 10 |

El número de repeticiones se reduce en los tamaños mayores debido al fuerte crecimiento del costo de BFS.

Resultado general: DFS encuentra una primera solución con muchos menos nodos, tiempo y memoria que BFS. Para N=13, los resultados guardados muestran un promedio aproximado de 112 s y 234.770 KB para BFS, frente a aproximadamente 0,0012 s y 1,72 KB para DFS.

## Interpretación conjunta

Los resultados muestran que no existe un algoritmo universalmente superior en todos los espacios de estados.

- En **Mochila 0/1**, DFS conserva una ventaja muy marcada en memoria porque profundiza una rama y mantiene una frontera pequeña, mientras BFS conserva numerosos estados del mismo nivel.
- En **Puzzle 3x3**, BFS fue superior en las instancias estudiadas porque las soluciones estaban a poca profundidad y DFS podía internarse en rutas muy largas antes de alcanzar la meta.
- En **N-Reinas**, DFS fue considerablemente más eficiente para encontrar la primera solución, mientras BFS acumuló una frontera muy grande antes de llegar al nivel completo.

Por tanto, la conveniencia de BFS o DFS depende de la estructura del espacio de estados, de la profundidad esperada de la solución y del criterio de terminación utilizado.

## Instalación

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

### Mochila

```bash
python mochila/simulaciones.py
python mochila/analisis_resultados.py
python mochila/graficas.py
python mochila/arboles.py
```

### Puzzle 3x3

```bash
python puzzle/simulaciones.py
python puzzle/analisis_resultados.py
python puzzle/graficas.py
python puzzle/arboles.py
```

### N-Reinas

El módulo de N-Reinas tiene un flujo automatizado propio. Para conservar las rutas actuales de sus archivos de salida, se ejecuta desde su carpeta:

```bash
cd Nreinas
python main.py
```

Para visualizar el árbol de N=4:

```bash
python arboles.py 4
```

## Resultados

Los archivos CSV, resúmenes y gráficas generadas se encuentran en `resultados/`.

Las gráficas de Puzzle se redujeron a un conjunto principal que evita redundancias y utiliza escala logarítmica cuando las diferencias entre BFS y DFS son de varios órdenes de magnitud.

## Nota sobre reproducibilidad

Los tiempos de ejecución pueden variar entre equipos y entre ejecuciones. Por esta razón se reportan promedios y medianas, y N-Reinas registra además información del equipo utilizado. Los resultados deben interpretarse como evidencia experimental de las implementaciones incluidas en este repositorio, no como tiempos absolutos universales de BFS y DFS.
