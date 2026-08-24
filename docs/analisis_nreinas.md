# Análisis de desempeño: BFS vs DFS en N-Reinas

## 1. Objetivo

Comparar experimentalmente BFS y DFS en el problema de las N-Reinas utilizando como métricas principales:

- Tiempo de ejecución.
- Memoria pico utilizada.

Como métrica auxiliar se registra la cantidad de nodos explorados.

## 2. Representación del problema

El tablero se representa como una lista donde el índice corresponde a la columna y el valor corresponde a la fila ocupada por la reina:

```python
tablero = [1, 3, 0, 2]
```

Los estados se construyen columna por columna. Antes de generar un sucesor se verifica que la nueva reina no comparta fila ni diagonal con las ya colocadas.

BFS y DFS se detienen al encontrar la primera solución completa.

## 3. Configuración experimental

| Parámetro | Valor |
|---|---|
| Problema | N-Reinas |
| Algoritmos | BFS y DFS |
| Rango de N | 4 a 13 |
| Tiempo | `time.perf_counter()` |
| Memoria | `tracemalloc` |
| Métrica auxiliar | Nodos explorados |

El número de repeticiones no es igual para todos los tamaños debido al costo creciente de BFS:

| N | Repeticiones por algoritmo |
|---:|---:|
| 4 a 10 | 100 |
| 11 | 50 |
| 12 | 20 |
| 13 | 10 |

Para cada N se repite el mismo problema determinista. Por tanto, las repeticiones permiten estudiar principalmente la variabilidad de las mediciones de tiempo y memoria.

## 4. Resultados guardados

Los promedios actuales del archivo `resultados/nreinas/datos/resumen.csv` son:

| N | BFS tiempo | BFS memoria | BFS nodos | DFS tiempo | DFS memoria | DFS nodos |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.000056 s | 1.32 KB | 16 | 0.000036 s | 0.15 KB | 9 |
| 5 | 0.000180 s | 1.70 KB | 45 | 0.000032 s | 0.20 KB | 6 |
| 6 | 0.000696 s | 2.99 KB | 150 | 0.000158 s | 0.35 KB | 32 |
| 7 | 0.00319 s | 13.58 KB | 513 | 0.000079 s | 0.43 KB | 10 |
| 8 | 0.0149 s | 58.86 KB | 1,966 | 0.000743 s | 0.57 KB | 114 |
| 9 | 0.0763 s | 270.73 KB | 8,043 | 0.000349 s | 0.70 KB | 42 |
| 10 | 0.457 s | 1,606.47 KB | 34,816 | 0.000913 s | 0.93 KB | 103 |
| 11 | 2.70 s | 8,172.26 KB | 164,247 | 0.000574 s | 1.20 KB | 53 |
| 12 | 19.76 s | 43,483.20 KB | 841,990 | 0.00333 s | 1.52 KB | 262 |
| 13 | 111.99 s | 234,769.94 KB | 4,601,179 | 0.00123 s | 1.72 KB | 112 |

## 5. Interpretación

El patrón experimental es claro: a medida que aumenta N, BFS debe mantener una frontera cada vez más grande y procesar todos los estados de niveles anteriores antes de alcanzar una solución completa en profundidad N.

DFS, en cambio, profundiza una rama válida antes de regresar a otras alternativas. Con el orden de generación utilizado en esta implementación, encuentra una primera solución completa después de explorar muchos menos estados.

Para N=13, BFS explora aproximadamente 4,6 millones de nodos frente a 112 de DFS. Esta diferencia explica el fuerte contraste observado tanto en tiempo como en memoria.

No se debe concluir que DFS sea universalmente superior a BFS. El resultado corresponde a este problema, a este criterio de terminación y al orden de generación de sucesores implementado.

## 6. Decisiones de visualización

Las gráficas principales usan escala logarítmica porque las diferencias entre BFS y DFS abarcan varios órdenes de magnitud. Mantener una escala lineal haría que los valores de DFS quedaran visualmente comprimidos cerca de cero.

Se generan cuatro gráficas principales:

1. Tiempo promedio por N.
2. Memoria pico promedio por N.
3. Nodos explorados promedio por N.
4. Ratio BFS/DFS para tiempo, memoria y nodos.

La gráfica de ratios permite leer directamente cuántas veces el promedio de BFS supera al promedio de DFS en cada métrica.

## 7. Árbol de búsqueda

Para visualizar el comportamiento de ambos algoritmos se utiliza N=4, porque el árbol completo sigue siendo legible. Se construye el mismo árbol de estados factibles y se diferencia el orden de visita de BFS y DFS mediante la numeración de los nodos.

Esta visualización tiene un propósito explicativo y no sustituye las mediciones de las ejecuciones experimentales.

## 8. Archivos de salida

Los datos se guardan en:

```text
resultados/nreinas/datos/
├── resultados.csv
├── resumen.csv
├── comparacion.csv
└── info_maquina.json
```

Las gráficas se guardan en:

```text
resultados/nreinas/graficas/
```

## 9. Conclusión del problema N-Reinas

Para encontrar la primera solución del problema N-Reinas con las implementaciones evaluadas, DFS presenta un desempeño significativamente mejor que BFS. La diferencia se hace especialmente grande al aumentar N porque BFS conserva una frontera extensa y procesa una cantidad mucho mayor de estados antes de llegar al nivel donde aparecen las soluciones completas.
