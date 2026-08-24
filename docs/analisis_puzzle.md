# Análisis de Desempeño: BFS vs DFS en Puzzle

---

## 1. Resumen Ejecutivo

Este documento presenta el análisis experimental comparativo entre **Búsqueda en Anchura (BFS)** y **Búsqueda en Profundidad (DFS)** aplicado al problema del **Puzzle 8**.

Se realizaron **100 simulaciones para cada algoritmo**, midiendo tiempo de ejecución, memoria utilizada, nodos explorados, movimientos y profundidad.

**Conclusión principal:** BFS presentó un comportamiento mucho más estable y eficiente en este experimento. Las 100 ejecuciones de BFS terminaron correctamente, mientras que DFS alcanzó el límite establecido en **49 de 100 ejecuciones**.

---

## 2. Configuración Experimental

| Parámetro | Valor |
|---|---|
| **Problema** | Puzzle 8 |
| **Algoritmos** | BFS y DFS |
| **Simulaciones** | 100 por algoritmo |
| **Métricas** | Tiempo, memoria, nodos, movimientos y profundidad |
| **Límite de DFS** | 50.000 nodos |
| **Algoritmo BFS exitoso** | 100% |
| **Algoritmo DFS exitoso** | 51% |

---

## 3. Resultados Cuantitativos

### 3.1 Comparación general

| Algoritmo | Ejecuciones | Tiempo promedio | Memoria promedio | Nodos promedio |
|---|---:|---:|---:|---:|
| **BFS** | 100 | 0.000690 s | 16.82 KB | 80.25 |
| **DFS** | 100 | 0.251394 s* | 9777.18 KB* | 28,059.49* |

\* Incluye las ejecuciones que alcanzaron el límite de 50.000 nodos.

### 3.2 Ejecuciones exitosas

| Algoritmo | Exitosas | Tiempo promedio | Memoria promedio | Nodos promedio |
|---|---:|---:|---:|---:|
| **BFS** | 100 | 0.000690 s | 16.82 KB | 80.25 |
| **DFS** | 51 | 0.063014 s | 2492.67 KB | 6979.39 |

---

## 4. Análisis de los Resultados

### BFS

BFS obtuvo **100 ejecuciones exitosas de 100**, sin alcanzar el límite de nodos.

Su tiempo promedio fue de aproximadamente:

**0.00069 segundos**

y utilizó en promedio:

**16.82 KB de memoria.**

Además, exploró aproximadamente **80 nodos por ejecución**.

### DFS

DFS tuvo **51 ejecuciones exitosas de 100**.

Las otras **49 ejecuciones alcanzaron el límite de 50.000 nodos**, equivalente al **49% de las ejecuciones**.

En las ejecuciones exitosas, DFS presentó:

- Tiempo promedio: **0.063 segundos**
- Memoria promedio: **2492.67 KB**
- Nodos promedio: **6979.39**

Esto muestra que DFS puede necesitar explorar una cantidad mucho mayor de estados antes de encontrar una solución.

---

## 5. Comparación de Límites

| Algoritmo | Total | Exitosas | Límite alcanzado | % límite |
|---|---:|---:|---:|---:|
| **BFS** | 100 | 100 | 0 | 0% |
| **DFS** | 100 | 51 | 49 | 49% |

**Observación principal:** BFS completó todas las simulaciones, mientras que DFS no pudo completar el 49% debido al límite de **50.000 nodos**.

---

## 6. Conclusión

Los resultados experimentales muestran que, para las configuraciones de Puzzle evaluadas:

- **BFS fue más rápido** en promedio.
- **BFS utilizó considerablemente menos memoria.**
- BFS completó **100% de las simulaciones**.
- DFS solo completó **51% de las simulaciones**.
- DFS alcanzó el límite de **50.000 nodos en 49 casos**.
- Cuando DFS alcanza el límite, aumenta considerablemente el tiempo, la memoria y la cantidad de nodos explorados.

Por lo tanto, **BFS presentó el mejor desempeño general en este experimento de Puzzle**, especialmente en estabilidad y capacidad para completar las búsquedas.

---

*Análisis elaborado a partir de los resultados experimentales disponibles en `resultados.csv`, `resumen.csv`, `resumen_exitosas.csv` y `limites.csv`.*
