# Análisis de Desempeño: BFS vs DFS en el Puzzle 3x3

---

## 1. Resumen Ejecutivo

Este documento presenta el análisis experimental comparativo entre **Búsqueda en Anchura (BFS)** y **Búsqueda en Profundidad (DFS)** aplicados al problema del **Puzzle 3x3 (8-Puzzle)**.

El objetivo principal es comparar el desempeño de ambos algoritmos en términos de:

- Tiempo de ejecución.
- Consumo de memoria.
- Nodos explorados.
- Cantidad de movimientos de la solución.
- Profundidad de la solución.
- Ejecuciones que alcanzan el límite de nodos.

El experimento utiliza **100 estados iniciales**, ejecutando BFS y DFS sobre los mismos escenarios, para un total de **200 ejecuciones**. Cada búsqueda tiene un límite experimental de **50.000 nodos**.

> **Nota:** Los valores numéricos definitivos se incorporarán cuando se disponga de `resultados.csv`.

---

## 2. Configuración Experimental

| Parámetro | Valor |
|---|---|
| **Problema** | Puzzle 3x3 / 8-Puzzle |
| **Representación** | Tupla de 9 posiciones |
| **Espacio vacío** | `0` |
| **Estado objetivo** | `(1,2,3,4,5,6,7,8,0)` |
| **Algoritmos** | BFS vs DFS |
| **Estructura BFS** | Cola FIFO (`deque`) |
| **Estructura DFS** | Pila LIFO |
| **Simulaciones** | 100 |
| **Total ejecuciones** | 200 |
| **Límite de nodos** | 50.000 |
| **Mezcla inicial** | 6 movimientos |
| **Semilla aleatoria** | 42 |
| **Métricas** | Tiempo, memoria, nodos, movimientos y profundidad |
| **Tiempo** | `time.perf_counter()` |
| **Memoria** | `tracemalloc` |
| **Análisis** | `pandas` |
| **Gráficas** | `matplotlib` |
| **Árbol de estados** | `networkx` |

---

## 3. Resultados Cuantitativos

### 3.1 Tabla Resumen

| Métrica | **BFS** | **DFS** |
|---|---:|---:|
| Tiempo promedio | Pendiente | Pendiente |
| Memoria promedio | Pendiente | Pendiente |
| Nodos promedio | Pendiente | Pendiente |
| Movimientos promedio | Pendiente | Pendiente |
| Profundidad promedio | Pendiente | Pendiente |
| Ejecuciones con límite | Pendiente | Pendiente |

Los valores se completarán a partir de `resultados.csv` y de los archivos de resumen generados por el proyecto.

### 3.2 Observaciones Clave

1. BFS explora los estados por niveles utilizando una cola FIFO.
2. DFS profundiza en una rama utilizando una pila LIFO.
3. BFS garantiza una solución de profundidad mínima cuando todos los movimientos tienen el mismo costo.
4. DFS no garantiza encontrar la solución con menor cantidad de movimientos.
5. El tiempo y la memoria deben compararse utilizando los resultados reales de las simulaciones.
6. Las ejecuciones que alcanzan los 50.000 nodos deben analizarse por separado de las ejecuciones que terminan normalmente.

---

## 4. Análisis de Complejidad

| Aspecto | BFS | DFS |
|---|---|---|
| **Estrategia** | Nivel por nivel | Profundidad |
| **Estructura** | Cola FIFO | Pila LIFO |
| **Solución mínima** | Sí, con costos uniformes | No garantizada |
| **Estados visitados** | Sí | Sí |
| **Reconstrucción** | Mediante padres | Mediante padres |
| **Límite experimental** | 50.000 nodos | 50.000 nodos |

### ¿Por qué pueden comportarse de manera diferente?

1. **BFS** mantiene una exploración ordenada por niveles, por lo que puede almacenar una cantidad importante de estados.
2. **DFS** continúa profundizando antes de explorar otras ramas.
3. La diferencia en el orden de exploración puede afectar el tiempo y la cantidad de nodos necesarios para encontrar una solución.
4. BFS favorece soluciones mínimas en número de movimientos, mientras que DFS prioriza encontrar una solución siguiendo una rama.

> La comparación de memoria debe basarse en las mediciones reales de `tracemalloc`, ya que la implementación mantiene estructuras de estados visitados y padres en ambos algoritmos.

---

## 5. Visualización del Árbol de Búsqueda

El archivo `arboles.py` construye un árbol parcial del espacio de estados con una profundidad visual máxima de **3 niveles**.

Se generan dos recorridos sobre el mismo árbol:

- **BFS:** nivel por nivel.
- **DFS:** profundizando por una rama antes de continuar con las demás.

La visualización permite observar directamente cómo cambia el orden de visita de los estados dependiendo del algoritmo.

**Archivo generado:**

```text
resultados/puzzle/graficas/arboles/arbol_puzzle.png
```

---

## 6. Gráficas Generadas

El proyecto genera seis gráficas principales:

| Archivo | Descripción |
|---|---|
| `01_tiempo_global.png` | Comparación del tiempo de BFS y DFS |
| `02_memoria_global_log.png` | Comparación de memoria en escala logarítmica |
| `03_nodos.png` | Comparación de nodos explorados |
| `04_limites.png` | Ejecuciones normales frente a ejecuciones limitadas |
| `05_tiempo_exitosas_log.png` | Tiempo de las ejecuciones exitosas |
| `06_memoria_exitosas_log.png` | Memoria de las ejecuciones exitosas |
| `arbol_puzzle.png` | Árbol parcial BFS vs DFS |

---

## 7. Archivos de Datos

El proyecto genera los resultados dentro de la carpeta:

```text
resultados/puzzle/
```

### Datos

```text
resultados/puzzle/datos/
├── resultados.csv
├── resumen.csv
├── resumen_exitosas.csv
└── limites.csv
```

### Gráficas

```text
resultados/puzzle/graficas/
├── comparacion/
└── arboles/
```

### Descripción

| Archivo | Contenido |
|---|---|
| `resultados.csv` | Resultados individuales de las simulaciones |
| `resumen.csv` | Estadísticas generales por algoritmo |
| `resumen_exitosas.csv` | Estadísticas de ejecuciones sin límite |
| `limites.csv` | Conteo de ejecuciones que alcanzaron el límite |

---

## 8. Código Fuente

La estructura principal del proyecto es:

```text
Puzzle/
├── bfs_dfs_puzzle.py
│   # Implementación de BFS y DFS
│
├── medicion.py
│   # Medición de tiempo, memoria y métricas
│
├── simulaciones.py
│   # Generación de las 100 simulaciones
│
├── analisis_resultados.py
│   # Análisis estadístico
│
├── graficas.py
│   # Generación de gráficas
│
└── arboles.py
    # Visualización del árbol BFS vs DFS
```

### Ejecución

```bash
python simulaciones.py
python analisis_resultados.py
python graficas.py
python arboles.py
```

---

## 9. Conclusión

El experimento permite comparar BFS y DFS bajo las mismas condiciones utilizando el Puzzle 3x3.

BFS realiza una búsqueda por niveles y tiene la ventaja de encontrar soluciones mínimas en cantidad de movimientos cuando los costos son uniformes. DFS, por su parte, explora en profundidad y puede encontrar una solución sin recorrer necesariamente todos los niveles anteriores.

La conclusión definitiva sobre cuál algoritmo presenta mejor desempeño en **tiempo, memoria y cantidad de nodos explorados** debe establecerse a partir de los resultados reales de las 100 simulaciones.

Una vez incorporado `resultados.csv`, esta sección deberá incluir los valores concretos y las diferencias porcentuales entre BFS y DFS.

---

*Documento preparado a partir de los seis archivos Python del proyecto Puzzle 3x3.*
