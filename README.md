# Desempeño BFS vs DFS

Proyecto académico para comparar experimentalmente los algoritmos **Breadth-First Search (BFS)** y **Depth-First Search (DFS)** en tres problemas con espacios de estados diferentes:

1. Puzzle 3x3.
2. N-Reinas.
3. Mochila 0/1.

El análisis se concentra principalmente en **tiempo de ejecución** y **memoria pico utilizada**. La cantidad de nodos explorados y, cuando aplica, la profundidad o longitud de la solución se utilizan como métricas auxiliares para explicar el comportamiento observado.

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
│
├── puzzle/
│   ├── bfs_dfs_puzzle.py
│   ├── medicion.py
│   ├── simulaciones.py
│   ├── analisis_resultados.py
│   ├── graficas.py
│   └── arboles.py
│
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
│   ├── main.py
│   └── README.md
│
├── resultados/
│   ├── mochila/
│   │   ├── datos/
│   │   │   ├── resultados.csv
│   │   │   ├── resumen.csv
│   │   │   └── comparacion.csv
│   │   └── graficas/
│   │       ├── arboles/
│   │       └── comparacion/
│   │
│   ├── puzzle/
│   │   ├── datos/
│   │   │   ├── resultados.csv
│   │   │   ├── resumen.csv
│   │   │   ├── resumen_exitosas.csv
│   │   │   └── limites.csv
│   │   └── graficas/
│   │       ├── arboles/
│   │       └── comparacion/
│   │
│   └── nreinas/
│       ├── datos/
│       └── graficas/
│
├── docs/
├── requirements.txt
└── .gitignore
```

## Metodología común

Las implementaciones se desarrollaron en Python. Para las mediciones se utilizaron:

- `time.perf_counter()` para medir tiempo de ejecución.
- `tracemalloc` para registrar memoria pico asignada durante la ejecución.
- Un contador explícito de nodos procesados como métrica auxiliar.

Dentro de cada problema, BFS y DFS reciben las mismas condiciones de entrada para que la comparación sea equivalente.

Las mediciones deben interpretarse de manera experimental: los tiempos pueden cambiar entre equipos y entre ejecuciones, mientras que las tendencias relativas permiten estudiar el comportamiento de cada estrategia de búsqueda.

## Mochila 0/1

Cada estado representa la decisión de **tomar o no tomar un objeto**. BFS y DFS recorren el mismo árbol factible de decisiones, por lo que ambos encuentran el mismo valor óptimo y exploran la misma cantidad de nodos en cada instancia. La diferencia principal se encuentra en el orden de exploración y en la cantidad de estados que permanecen pendientes en memoria.

Se realizaron **100 instancias aleatorias**, distribuidas en cinco tamaños:

- 20 instancias con 5 objetos.
- 20 instancias con 8 objetos.
- 20 instancias con 10 objetos.
- 20 instancias con 12 objetos.
- 20 instancias con 15 objetos.

Los pesos se generan entre 1 y 15, los valores entre 1 y 30 y la capacidad corresponde aproximadamente al 40 % del peso total. Se utiliza `random.seed(42)` para reproducibilidad.

### Resultado general

Al aumentar el número de objetos, BFS presenta un crecimiento de memoria mucho mayor que DFS debido al tamaño de la frontera almacenada en la cola. DFS mantiene una pila mucho más pequeña mientras profundiza por una rama del árbol.

Para la visualización se construye un árbol de decisiones común y se muestra el orden de visita de BFS y DFS sobre ese mismo árbol, permitiendo comparar directamente ambas estrategias.

## Puzzle 3x3

Los estados iniciales se generan a partir del estado objetivo mediante **6 movimientos válidos aleatorios**, evitando la reversión inmediata del último movimiento. Este procedimiento garantiza que las instancias generadas sean solucionables.

Los 6 movimientos corresponden al proceso de mezcla utilizado para generar cada instancia; no implican necesariamente que la distancia óptima a la solución sea exactamente 6 movimientos.

Se realizaron **100 simulaciones** con semilla `42`. En cada simulación BFS y DFS reciben exactamente el mismo estado inicial.

Se estableció un límite experimental de **50.000 nodos por ejecución**. Las ejecuciones que alcanzan ese límite se identifican explícitamente y se analizan por separado de las búsquedas que terminan normalmente.

### Resultados del conjunto actual

- BFS completó 100 de 100 ejecuciones.
- DFS completó 51 de 100 ejecuciones.
- DFS alcanzó el límite de 50.000 nodos en 49 ejecuciones.

En estas instancias cercanas a la meta, BFS presentó menor tiempo y menor memoria que DFS. El análisis distingue entre:

- resultados globales, que consideran todas las ejecuciones;
- resultados de ejecuciones que terminaron normalmente.

En el resumen global se comparan principalmente tiempo, memoria y nodos explorados. Los movimientos y la profundidad se reportan únicamente para las ejecuciones que terminaron normalmente.

### Árbol de búsqueda del Puzzle

El árbol mostrado para el Puzzle es una **representación parcial común del espacio de estados**, construida hasta una profundidad visual limitada. Se utiliza con fines comparativos para mostrar el orden de visita de BFS y DFS sobre un mismo conjunto de estados.

Por tanto, esta visualización no representa la totalidad del espacio de búsqueda real ni todos los estados que cada algoritmo podría explorar durante una simulación completa.

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

### Resultado general

DFS encuentra una primera solución con muchos menos nodos, tiempo y memoria que BFS. Para N=13, los resultados guardados muestran un promedio aproximado de 112 s y 234.770 KB para BFS, frente a aproximadamente 0,0012 s y 1,72 KB para DFS.

## Interpretación conjunta

Los resultados muestran que no existe un algoritmo universalmente superior en todos los espacios de estados.

- En **Mochila 0/1**, DFS conserva una ventaja muy marcada en memoria porque profundiza una rama y mantiene una frontera pequeña, mientras BFS conserva numerosos estados del mismo nivel.
- En **Puzzle 3x3**, BFS fue superior en las instancias estudiadas porque las soluciones se encontraban a poca profundidad relativa y DFS podía internarse en rutas muy largas antes de alcanzar la meta.
- En **N-Reinas**, DFS fue considerablemente más eficiente para encontrar la primera solución, mientras BFS acumuló una frontera muy grande antes de llegar al nivel completo.

Por tanto, la conveniencia de BFS o DFS depende de la estructura del espacio de estados, de la profundidad esperada de la solución, del criterio de terminación y de la forma en que cada implementación administra los estados pendientes y visitados.

## Instalación

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Todos los comandos siguientes se pueden ejecutar desde la raíz del repositorio.

### Mochila

Ejecutar simulaciones:

```bash
python mochila/simulaciones.py
```

Generar análisis estadístico:

```bash
python mochila/analisis_resultados.py
```

Generar gráficas de comparación:

```bash
python mochila/graficas.py
```

Generar el árbol comparativo BFS vs DFS:

```bash
python mochila/arboles.py
```

### Puzzle 3x3

Ejecutar simulaciones:

```bash
python puzzle/simulaciones.py
```

Generar análisis estadístico:

```bash
python puzzle/analisis_resultados.py
```

Generar gráficas de comparación:

```bash
python puzzle/graficas.py
```

Generar el árbol parcial comparativo BFS vs DFS:

```bash
python puzzle/arboles.py
```

### N-Reinas

Flujo completo:

```bash
python Nreinas/main.py
```

Análisis a partir de los datos existentes:

```bash
python Nreinas/analisis_resultados.py
```

Gráficas a partir de los datos existentes:

```bash
python Nreinas/graficas.py
```

Árbol de búsqueda para N=4:

```bash
python Nreinas/arboles.py 4
```

## Resultados

Los resultados se organizan por problema para separar claramente los datos experimentales de las visualizaciones.

### Mochila

- `resultados/mochila/datos/resultados.csv`: resultados de las 100 instancias.
- `resultados/mochila/datos/resumen.csv`: estadísticas descriptivas por cantidad de objetos y algoritmo.
- `resultados/mochila/datos/comparacion.csv`: comparación directa entre BFS y DFS.
- `resultados/mochila/graficas/arboles/`: árbol comparativo BFS vs DFS.
- `resultados/mochila/graficas/comparacion/`: gráficas de tiempo y memoria.

### Puzzle

- `resultados/puzzle/datos/resultados.csv`: resultados de las 100 simulaciones.
- `resultados/puzzle/datos/resumen.csv`: resumen global de tiempo, memoria y nodos.
- `resultados/puzzle/datos/resumen_exitosas.csv`: estadísticas de las ejecuciones que terminaron normalmente.
- `resultados/puzzle/datos/limites.csv`: cantidad de ejecuciones que alcanzaron el límite experimental.
- `resultados/puzzle/graficas/arboles/`: árbol parcial comparativo BFS vs DFS.
- `resultados/puzzle/graficas/comparacion/`: gráficas de tiempo, memoria, nodos y ejecuciones limitadas.

### N-Reinas

- `resultados/nreinas/datos/`: resultados y resúmenes experimentales.
- `resultados/nreinas/graficas/`: visualizaciones generadas para el problema.

## Nota sobre reproducibilidad

Los tiempos de ejecución pueden variar entre equipos y entre ejecuciones. Por esta razón se reportan promedios y medianas, y N-Reinas registra además información del equipo utilizado.

Los resultados deben interpretarse como evidencia experimental de las implementaciones incluidas en este repositorio y no como tiempos absolutos universales de BFS y DFS.
