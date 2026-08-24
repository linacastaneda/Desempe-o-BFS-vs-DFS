# N-Reinas: Comparación BFS vs DFS

Implementación del problema de las N-Reinas utilizando búsqueda en profundidad (DFS) y búsqueda en anchura (BFS), con análisis experimental de desempeño.

## Estructura

```
Nreinas/
├── main.py                 # Punto de entrada con menú interactivo
├── n_reinas.py             # Funciones comunes (validación, representación)
├── bfs.py                  # Implementación BFS
├── dfs.py                  # Implementación DFS
├── visualizacion.py        # Visualización del tablero con matplotlib
├── medicion.py             # Medición de tiempo y memoria
├── simulaciones.py         # 100 simulaciones por cada N
├── graficas.py             # Generación de gráficas comparativas
├── analisis_resultados.py  # Análisis estadístico y Big-O
│
├── resultados/
│   └── datos/
│       ├── resultados_nreinas.csv
│       ├── resumen_nreinas.csv
│       └── comparacion_nreinas.csv
│
└── README.md
```

## Representación del Estado

El tablero se representa como una lista donde el índice es la columna y el valor es la fila:

```python
tablero = [1, 3, 0, 2]  # 4 reinas
```

Significa:
- Columna 0: reina en fila 1
- Columna 1: reina en fila 3
- Columna 2: reina en fila 0
- Columna 3: reina en fila 2

Visualmente:
```
. Q . .
. . . Q
Q . . .
. . Q .
```

## Algoritmos

### DFS (Depth-First Search)
- Utiliza una **pila** (LIFO)
- Explora en profundidad hasta encontrar solución o callejón sin salida
- Complejidad espacial: **O(N)** (solo almacena el camino actual)
- Encuentra la primera solución rápidamente

### BFS (Breadth-First Search)
- Utiliza una **cola** (FIFO)
- Explora nivel por nivel (todas las posiciones de una columna antes de pasar a la siguiente)
- Complejidad espacial: **O(N!)** en peor caso (almacena nivel completo)
- Garantiza encontrar la solución con menor profundidad

## Métricas Medidas

1. **Tiempo de ejecución** - `time.perf_counter()`
2. **Memoria pico** - `tracemalloc` (en KB)
3. **Nodos explorados** - Contador de estados visitados
4. **Solución encontrada** - Booleano

## Experimento

- **N valores**: 4, 5, 6, 7, 8, 9, 10
- **Simulaciones por N**: 100
- **Total**: 1,400 ejecuciones (700 BFS + 700 DFS)
- **Mismo problema**: BFS y DFS resuelven exactamente la misma instancia

## Uso

### Menú interactivo
```bash
python main.py
```

### Experimento automático completo
```bash
python main.py --experimentos
```

### Opciones del menú
1. Ejecutar DFS una vez
2. Ejecutar BFS una vez
3. Comparar ambos (con visualización)
4. Ejecutar 100 simulaciones
5. Generar gráficas desde CSV guardado
6. Experimento completo (simulaciones + gráficas + análisis)
7. Análisis estadístico detallado

## Resultados Generados

### `resultados_nreinas.csv`
Datos brutos de cada simulación:
```
simulacion, n, algoritmo, tiempo, memoria_kb, nodos, solucion_encontrada
```

### `resumen_nreinas.csv`
Promedios por N y algoritmo:
```
n, algoritmo, tiempo_promedio, memoria_promedio, nodos_promedio
```

### `comparacion_nreinas.csv`
Diferencias porcentuales BFS vs DFS:
```
n, diferencia_tiempo_porcentaje, diferencia_memoria_porcentaje, diferencia_nodos_porcentaje
```

## Gráficas Generadas

1. **Tiempo vs N** (escala logarítmica)
2. **Memoria vs N** (escala logarítmica)
3. **Nodos explorados vs N** (escala logarítmica)
4. **Boxplot tiempo** - Distribución por N y algoritmo
5. **Boxplot memoria** - Distribución por N y algoritmo
6. **Boxplot nodos** - Distribución por N y algoritmo

## Análisis de Complejidad (Big-O)

| Aspecto | DFS | BFS |
|---------|-----|-----|
| Tiempo peor caso | O(N!) | O(N!) |
| Espacio peor caso | O(N) | O(N!) |
| Espacio típico | O(N) | Exponencial |
| Primera solución | Rápida | Lenta (explora nivel completo) |
| Optimalidad (profundidad) | No garantizada | Garantizada (mínima profundidad) |

## Requisitos

```bash
pip install matplotlib pandas numpy networkx
```

## Ejemplo de Salida

```
===================================
       N-REINAS: BFS vs DFS
===================================

1. Ejecutar DFS
2. Ejecutar BFS
3. Mostrar tablero
4. Ejecutar 100 simulaciones
5. Generar gráficas
6. Ejecutar experimento completo
7. Salir

Seleccione una opción: 3
Ingrese N: 8

DFS: [4, 6, 1, 5, 2, 0, 3, 7] (0.000123s, 145 nodos)
BFS: [0, 4, 7, 5, 2, 6, 1, 3] (0.000456s, 2891 nodos)
```

Se abren dos ventanas con los tableros visuales y una comparación lado a lado.

