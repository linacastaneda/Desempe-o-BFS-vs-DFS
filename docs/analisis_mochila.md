# Análisis de Desempeño: BFS vs DFS en Mochila 0/1

---

## 1. Resumen Ejecutivo

Este documento presenta el análisis experimental comparativo entre **Búsqueda en Anchura (BFS)** y **Búsqueda en Profundidad (DFS)** aplicados al problema de la **Mochila 0/1**.

En esta implementación, ambos algoritmos recorren el mismo árbol factible de decisiones y evalúan las mismas alternativas de tomar o no tomar cada objeto. Por esta razón, BFS y DFS encuentran el mismo valor óptimo y exploran la misma cantidad de nodos para una misma instancia. La diferencia principal se encuentra en el **orden de exploración** y en la cantidad de estados que cada algoritmo mantiene pendientes en memoria.

**Conclusión principal:** DFS presenta una ventaja clara en consumo de memoria y, a medida que aumenta el número de objetos, también muestra un mejor comportamiento temporal. La diferencia de memoria se vuelve especialmente marcada en las instancias de mayor tamaño, debido a que BFS conserva una frontera amplia de nodos del mismo nivel mientras DFS profundiza una rama antes de continuar con las alternativas pendientes.

---

## 2. Configuración Experimental

| Parámetro | Valor |
|-----------|-------|
| **Problema** | Mochila 0/1 |
| **Representación del estado** | `(indice, peso_actual, valor_actual, seleccionados)` |
| **Algoritmos** | BFS (cola FIFO) vs DFS (pila LIFO) |
| **Métricas principales** | Tiempo de ejecución (s), memoria pico (KB) |
| **Métrica auxiliar** | Nodos explorados |
| **Tamaños evaluados** | 5, 8, 10, 12 y 15 objetos |
| **Simulaciones por tamaño** | 20 |
| **Total de instancias** | 100 |
| **Ejecuciones totales** | 200 (100 BFS + 100 DFS) |
| **Pesos aleatorios** | 1 a 15 |
| **Valores aleatorios** | 1 a 30 |
| **Capacidad** | 40 % del peso total de cada instancia |
| **Semilla** | `random.seed(42)` |
| **Herramientas de medición** | `time.perf_counter()`, `tracemalloc` |

Cada instancia se ejecuta con exactamente los mismos pesos, valores y capacidad para BFS y DFS, lo que permite realizar una comparación directa entre los dos algoritmos.

---

## 3. Resultados Cuantitativos

### 3.1 Tabla Resumen de Promedios

| Objetos | **BFS Tiempo** | **DFS Tiempo** | **BFS Memoria** | **DFS Memoria** | **Nodos BFS** | **Nodos DFS** |
|--------:|---------------:|---------------:|----------------:|----------------:|--------------:|--------------:|
| 5 | 0.00002971 s | 0.00002710 s | 1.3758 KB | 0.1141 KB | 33.30 | 33.30 |
| 8 | 0.00017801 s | 0.00016852 s | 4.0250 KB | 0.2367 KB | 214.25 | 214.25 |
| 10 | 0.00110635 s | 0.00089131 s | 24.3918 KB | 0.3352 KB | 827.70 | 827.70 |
| 12 | 0.00490357 s | 0.00406395 s | 108.3906 KB | 0.4445 KB | 3071.30 | 3071.30 |
| 15 | 0.04147082 s | 0.02388505 s | 1289.9215 KB | 0.6406 KB | 22012.05 | 22012.05 |

### 3.2 Comparación Porcentual

| Objetos | **BFS vs DFS en tiempo** | **BFS vs DFS en memoria** |
|--------:|-------------------------:|--------------------------:|
| 5 | 9.59 % más | 1106.16 % más |
| 8 | 5.63 % más | 1600.33 % más |
| 10 | 24.13 % más | 7177.74 % más |
| 12 | 20.66 % más | 24283.13 % más |
| 15 | 73.63 % más | 201253.60 % más |

En términos más intuitivos, para 15 objetos BFS utilizó aproximadamente **2014 veces** la memoria promedio utilizada por DFS.

### 3.3 Observaciones Clave

1. **Mismos nodos explorados:** BFS y DFS recorren el mismo árbol factible, por lo que el promedio de nodos explorados es idéntico para ambos algoritmos en cada tamaño.
2. **Diferencia de memoria creciente:** la memoria de BFS aumenta mucho más rápido que la de DFS conforme crece el número de objetos.
3. **Diferencia temporal moderada al inicio:** para 5 y 8 objetos, la diferencia de tiempo es pequeña y puede verse influida por el costo fijo de ejecución y la variabilidad natural de mediciones muy cortas.
4. **Mayor separación en instancias grandes:** con 15 objetos, BFS utiliza 73.63 % más tiempo promedio que DFS y presenta una diferencia de memoria de varios órdenes de magnitud.
5. **El resultado no depende de una mejor solución:** ambos algoritmos obtienen el mismo valor óptimo; la diferencia se debe principalmente a cómo administran la frontera de búsqueda.

---

## 4. Análisis del Comportamiento de BFS y DFS

### 4.1 Estructura del árbol de decisiones

Para cada objeto existen dos decisiones posibles:

- **No tomar el objeto.**
- **Tomar el objeto**, siempre que su peso no haga superar la capacidad de la mochila.

El estado contiene el índice del siguiente objeto a evaluar, el peso acumulado, el valor acumulado y los objetos seleccionados. La búsqueda continúa hasta haber tomado una decisión sobre todos los objetos.

Debido a que tanto BFS como DFS generan los mismos sucesores y no utilizan una poda adicional distinta entre algoritmos, ambos recorren el mismo conjunto de estados factibles.

### 4.2 Tiempo de ejecución

En los tamaños pequeños las diferencias temporales son reducidas. Con 5 objetos, BFS tarda aproximadamente 9.59 % más que DFS, mientras que con 8 objetos la diferencia es de 5.63 %.

A medida que el árbol crece, la diferencia se hace más visible. Para 10 y 12 objetos, BFS tarda aproximadamente 24.13 % y 20.66 % más, respectivamente. En las instancias de 15 objetos la diferencia aumenta hasta aproximadamente 73.63 %.

Dado que ambos algoritmos exploran la misma cantidad de nodos, esta diferencia no se explica por una reducción del espacio de búsqueda, sino principalmente por el costo asociado a la administración de la frontera y de las estructuras de datos utilizadas durante el recorrido.

### 4.3 Consumo de memoria

La diferencia más importante del experimento aparece en la memoria pico.

BFS utiliza una cola FIFO y procesa el árbol por niveles. Antes de avanzar hacia niveles más profundos puede mantener simultáneamente una gran cantidad de estados pendientes. Cuando el árbol de decisiones aumenta, el ancho de los niveles intermedios también crece y la cola puede acumular numerosos nodos.

DFS utiliza una pila LIFO y profundiza una rama antes de regresar a otras alternativas. Esto permite mantener una cantidad mucho menor de estados pendientes al mismo tiempo.

El efecto se observa claramente en los resultados: con 5 objetos BFS utiliza aproximadamente 1.38 KB frente a 0.11 KB de DFS, mientras que con 15 objetos BFS alcanza aproximadamente 1289.92 KB frente a solo 0.64 KB de DFS.

### 4.4 Nodos explorados

Los promedios observados fueron:

- 5 objetos: 33.30 nodos.
- 8 objetos: 214.25 nodos.
- 10 objetos: 827.70 nodos.
- 12 objetos: 3071.30 nodos.
- 15 objetos: 22012.05 nodos.

Para cada tamaño, BFS y DFS presentan exactamente el mismo promedio de nodos. Este resultado es importante porque permite aislar el efecto del **orden de recorrido**: la diferencia en desempeño no proviene de que uno de los algoritmos evite explorar estados que el otro sí visita, sino de la forma en que organiza y conserva los estados pendientes.

---

## 5. Análisis de Complejidad

Considerando el árbol de decisiones de la Mochila 0/1, cada objeto puede producir hasta dos ramas. En el peor caso, el número de combinaciones crece exponencialmente con el número de objetos.

| Aspecto | BFS | DFS |
|---------|-----|-----|
| **Tiempo peor caso** | O(2^N) | O(2^N) |
| **Estados potenciales** | Exponenciales | Exponenciales |
| **Frontera almacenada** | Puede crecer exponencialmente | Crece principalmente con la profundidad |
| **Orden de recorrido** | Nivel por nivel | Rama por rama |
| **Ventaja observada** | Ninguna en esta implementación | Menor memoria y menor tiempo en tamaños grandes |

En términos del número de estados pendientes, DFS tiene una ventaja espacial porque no necesita conservar simultáneamente un nivel completo del árbol. La implementación utilizada almacena información adicional dentro de cada estado, por lo que el consumo real también depende de la representación concreta de los nodos en Python.

---

## 6. Visualización del Árbol de Búsqueda

Para facilitar la interpretación se utiliza una instancia pequeña:

- Pesos: `[2, 3, 4, 5]`
- Valores: `[3, 4, 5, 8]`
- Capacidad: `8`

La solución óptima alcanza un valor de **12**, seleccionando los objetos de peso 3 y 5, cuyos valores son 4 y 8 respectivamente.

En esta instancia ambos algoritmos exploran **24 nodos**, pero en diferente orden.

- **BFS** recorre los estados nivel por nivel.
- **DFS** profundiza primero la última alternativa insertada en la pila y después retrocede para explorar las demás ramas.

![Árbol Mochila BFS vs DFS](../resultados/mochila/graficas/arboles/arbol_mochila.png)

La imagen muestra el mismo árbol de decisiones en ambos casos, pero las etiquetas indican un orden de visita diferente. Esto permite visualizar por qué ambos algoritmos llegan al mismo óptimo y recorren los mismos nodos, aunque su comportamiento de memoria sea distinto.

---

## 7. Gráficas Generadas

Ubicación: `resultados/mochila/graficas/comparacion/`

| Archivo | Descripción |
|---------|-------------|
| `01_tiempo_simulaciones.png` | Tiempo de ejecución de BFS y DFS en las 100 simulaciones |
| `02_memoria_simulaciones.png` | Memoria pico de BFS y DFS en las 100 simulaciones |
| `03_tiempo_por_objetos.png` | Tiempo promedio según cantidad de objetos |
| `04_memoria_por_objetos.png` | Memoria promedio según cantidad de objetos |

Las gráficas permiten observar el crecimiento del costo computacional al aumentar el número de objetos. La interpretación detallada de estas visualizaciones y su comparación con Puzzle 3x3 y N-Reinas se desarrolla en el informe final del proyecto.

---

## 8. Archivos de Datos

Ubicación: `resultados/mochila/datos/`

| Archivo | Contenido |
|---------|-----------|
| `resultados.csv` | Resultados de las 100 instancias ejecutadas con BFS y DFS |
| `resumen.csv` | Promedios, medianas, mínimos, máximos y desviaciones por cantidad de objetos y algoritmo |
| `comparacion.csv` | Comparación directa y diferencias porcentuales entre BFS y DFS |

Los datos de cada instancia incluyen pesos, valores, capacidad, tiempo, memoria pico, nodos explorados y valor óptimo, lo que permite reproducir y verificar el análisis experimental.

---

## 9. Código Fuente

Ubicación: `mochila/`

```text
mochila/
├── bfs_dfs_mochila.py      # Implementación BFS y DFS
├── medicion.py              # Medición de tiempo y memoria
├── simulaciones.py          # Generación y ejecución de las 100 instancias
├── analisis_resultados.py   # Estadísticas y comparación BFS vs DFS
├── graficas.py              # Generación de gráficas comparativas
└── arboles.py               # Visualización del árbol BFS vs DFS
```

### Ejecución

Desde la raíz del repositorio:

```bash
python mochila/simulaciones.py
python mochila/analisis_resultados.py
python mochila/graficas.py
python mochila/arboles.py
```

---

## 10. Conclusiones

Los resultados experimentales muestran que BFS y DFS son capaces de resolver correctamente las mismas instancias de Mochila 0/1 y encontrar el mismo valor óptimo. Además, debido a la naturaleza exhaustiva de las implementaciones utilizadas, ambos exploran la misma cantidad de nodos.

La principal diferencia aparece en la forma de administrar la frontera de búsqueda. BFS conserva una gran cantidad de estados pertenecientes a los niveles actuales del árbol, lo que produce un crecimiento considerable de memoria a medida que aumenta el número de objetos. DFS profundiza una rama y mantiene una frontera mucho menor, por lo que su consumo de memoria permanece reducido en comparación.

En tiempo de ejecución, las diferencias son pequeñas para las instancias de menor tamaño, pero aumentan cuando crece el árbol de decisiones. Para 15 objetos, BFS presentó aproximadamente 73.63 % más tiempo promedio que DFS.

Por tanto, para la implementación experimental utilizada en este proyecto, **DFS resulta más conveniente que BFS para resolver exhaustivamente la Mochila 0/1**, especialmente cuando se considera el consumo de memoria. Sin embargo, esta conclusión corresponde al diseño concreto del experimento y no implica que DFS sea universalmente superior en todos los problemas de búsqueda.
