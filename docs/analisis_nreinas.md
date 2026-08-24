# Análisis de Desempeño: BFS vs DFS en N-Reinas

---

## 1. Resumen Ejecutivo

Este documento presenta el análisis experimental comparativo entre **Búsqueda en Anchura (BFS)** y **Búsqueda en Profundidad (DFS)** aplicados al problema de las **N-Reinas**, ejecutado en un **AMD Ryzen 7 7445HS w/ Radeon 740M Graphics** (12 núcleos, 15.26 GB RAM, Python 3.14.7).

**Conclusión principal:** DFS es **dramáticamente superior** a BFS para este problema. A partir de N=11, BFS se vuelve impráctico (tiempos > 35s, memoria > 8MB) mientras DFS resuelve N=13 en ~1ms con < 2KB.

---

## 2. Configuración Experimental

| Parámetro | Valor |
|-----------|-------|
| **Problema** | N-Reinas (colocar N reinas en tablero N×N sin ataques) |
| **Representación** | `tablero = [fila_col_0, fila_col_1, ...]` (una reina por columna) |
| **Algoritmos** | BFS (cola FIFO) vs DFS (pila LIFO) |
| **Métricas** | Tiempo (s), Memoria pico (KB), Nodos explorados |
| **Rango N** | 4 a 13 |
| **Simulaciones por N** | 100 (N≤10), 50 (N=11), 20 (N=12), 10 (N=13) |
| **Total ejecuciones** | 1,560 (780 BFS + 780 DFS) |
| **Herramientas** | `time.perf_counter()`, `tracemalloc`, 100% Python estándar |

---

## 3. Resultados Cuantitativos

### 3.1 Tabla Resumen (Promedios)

| N | Simul. | **BFS Tiempo** | **BFS Memoria** | **DFS Tiempo** | **DFS Memoria** | **Ratio Tiempo (BFS/DFS)** |
|---|--------|----------------|-----------------|----------------|-----------------|----------------------------|
| 4 | 100 | 0.000056 s | 1.3 KB | 0.000036 s | 0.15 KB | **1.5x** |
| 5 | 100 | 0.000180 s | 1.7 KB | 0.000032 s | 0.20 KB | **5.6x** |
| 6 | 100 | 0.000696 s | 3.0 KB | 0.000158 s | 0.35 KB | **4.4x** |
| 7 | 100 | 0.0032 s | 13.6 KB | 0.000079 s | 0.43 KB | **40x** |
| 8 | 100 | 0.0149 s | 58.9 KB | 0.00074 s | 0.57 KB | **20x** |
| 9 | 100 | 0.076 s | 271 KB | 0.00035 s | 0.70 KB | **218x** |
| 10 | 100 | 0.46 s | 1,569 KB | 0.00091 s | 0.93 KB | **501x** |
| 11 | 50 | **2.7 s** | **8,172 KB** | 0.00057 s | 1.2 KB | **4,707x** |
| 12 | 20 | **19.8 s** | **43,483 KB** | 0.0033 s | 1.5 KB | **5,928x** |
| 13 | 10 | **112 s** | **234,770 KB** | 0.0012 s | 1.7 KB | **91,393x** |

### 3.2 Observaciones Clave

1. **Tiempo**: BFS crece exponencialmente; en N=13 es **9.1 millones % más lento** que DFS
2. **Memoria**: BFS explota (230 MB en N=13); DFS se mantiene constante ~O(N) (< 2 KB)
3. **Nodos explorados**: BFS explora nivel completo; DFS hace backtracking eficiente
4. **Variabilidad**: BFS tiene alta desviación estándar en N≥11 (algunas ejecuciones mucho peores)

---

## 4. Análisis de Complejidad (Big-O)

| Aspecto | DFS (Backtracking) | BFS |
|---------|-------------------|-----|
| **Tiempo peor caso** | O(N!) | O(N!) |
| **Espacio peor caso** | **O(N)** | **O(N!)** |
| **Espacio típico** | O(N) | Exponencial |
| **Primera solución** | Rápida (profundo primero) | Lenta (explora nivel completo) |
| **Optimalidad profundidad** | No garantizada | Garantizada (mínima) |

### ¿Por qué DFS gana en N-Reinas?

1. **Naturaleza del problema**: Solo necesitamos **una** solución válida, no la "más corta"
2. **Backtracking natural**: DFS descarta ramas inválidas inmediatamente
3. **Memoria constante**: Solo guarda el camino actual (stack depth = N)
4. **BFS guarda nivel completo**: En N=13, el nivel 6 tiene ~4.6M nodos → 230 MB

---

## 5. Visualización del Árbol de Búsqueda (N=4)

Para N=4, el árbol completo tiene **17 nodos** y **2 soluciones**:

```
                    [] (raíz)
                 /  |  |  \
               [0] [1] [2] [3]  ← Nivel 1: columna 0
               /    |    |    \
            [0,2]  [1,3] ...     ← Nivel 2: columna 1
             |     |
            ...   ...
```

**BFS** visita nivel por nivel: `[], [0], [1], [2], [3], [0,2], [1,3], ...`
**DFS** va profundo: `[], [0], [0,2], [0,2,?], backtrack, [1], [1,3], [1,3,0], [1,3,0,2] ✓`

DFS encuentra la primera solución `[1, 3, 0, 2]` en el **nodo 9** (orden DFS), BFS en el **nodo 15** (orden BFS).

![Árbol N=4](../resultados/nreinas/graficas/arboles/arbol_n4.png)

---

## 6. Gráficas Generadas

Ubicación: `resultados/nreinas/graficas/<hostname>/`

| Archivo | Descripción |
|---------|-------------|
| `01_tiempo_barras.png` | Barras agrupadas tiempo BFS vs DFS |
| `02_memoria_barras.png` | Barras agrupadas memoria BFS vs DFS |
| `03_nodos_barras.png` | Barras agrupadas nodos BFS vs DFS |
| `04_tiempo_subplots.png` | Escalas separadas BFS/DFS |
| `05_memoria_subplots.png` | Escalas separadas BFS/DFS |
| `06_nodos_subplots.png` | Escalas separadas BFS/DFS |
| `07_ratio_bfs_dfs.png` | **Ratio BFS/DFS (clave)** - barras logarítmicas |
| `08_boxplot_tiempo.png` | Distribución tiempo por N |
| `09_boxplot_memoria.png` | Distribución memoria por N |
| `10_boxplot_nodos.png` | Distribución nodos por N |
| `arboles/arbol_n4.png` | Árbol completo BFS vs DFS lado a lado |

---

## 7. Archivos de Datos

Ubicación: `resultados/nreinas/datos/`

| Archivo | Contenido |
|---------|-----------|
| `resultados.csv` | 1,560 filas: cada simulación con hostname, CPU, RAM, Python |
| `info_maquina.json` | Hardware completo del equipo |
| `resumen.csv` | Promedios por N y algoritmo (con estadísticas) |
| `comparacion.csv` | Diferencias % BFS vs DFS por N |

---

## 8. Código Fuente

Ubicación: `Nreinas/`

```
Nreinas/
├── main.py              # Ejecución automática (sin menú)
├── n_reinas.py          # Validación y representación
├── bfs.py               # BFS con deque
├── dfs.py               # DFS con pila
├── visualizacion.py     # Tablero gráfico con matplotlib
├── medicion.py          # time.perf_counter + tracemalloc
├── simulaciones.py      # Experimento completo N=4..13
├── graficas.py          # 10 tipos de gráficas
├── analisis_resultados.py # Stats + Big-O
├── comparar_maquinas.py # Comparación multi-equipo
├── arboles.py           # Visualización árbol N pequeño
└── README.md
```

### Ejecución
```bash
cd Nreinas
python3 main.py                    # Experimento completo automático
python3 arboles.py 4               # Ver árbol N=4
python3 main.py --comparar-maquinas # Comparar múltiples PCs
```

---

## 9. Conclusiones y Recomendaciones

### Para N-Reinas (problema de satisfacción):
- **Usar DFS/Backtracking**: Memoria O(N), encuentra solución rápido
- **Evitar BFS**: Memoria O(N!), impráctico para N ≥ 11

### Para otros problemas:
- **BFS** es mejor cuando: se necesita solución óptima en profundidad, espacio de estados pequeño, o grafo no muy ramificado
- **DFS** es mejor cuando: espacio de estados grande/ramificado, solo se necesita una solución, memoria limitada

### Para el informe del profesor:
1. Mostrar tabla de resultados (Sección 3.1)
2. Explicar Big-O teórico vs experimental (Sección 4)
3. Mostrar gráfica de ratio (07_ratio_bfs_dfs.png)
4. Mostrar árbol N=4 (arboles/arbol_n4.png)
5. Concluir: DFS gana por backtracking natural y memoria constante

---

## 10. Próximos Pasos (Para completar entrega grupal)

- [ ] Agregar resultados de **Puzzle 3x3** (carpeta hermana `puzzle_3x3/`)
- [ ] Agregar resultados de **Mochila** (ya existe en `mochila/`)
- [ ] Unificar comparativas en `docs/comparacion_general.md`
- [ ] Preparar presentación: 3 problemas, 2 algoritmos, 1 conclusión

---

*Generado automáticamente por el experimento N-Reinas BFS vs DFS*  
*Equipo: AMD Ryzen 7 7445HS | 15.26 GB RAM | Python 3.14.7*  
*Fecha: 24/08/2026*