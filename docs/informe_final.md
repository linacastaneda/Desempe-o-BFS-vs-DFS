# Informe Final
## Análisis de Desempeño de BFS vs DFS 

---

## 1. Introducción

La búsqueda en anchura (**BFS**) y la búsqueda en profundidad (**DFS**). Aunque ambas permiten explorar soluciones en problemas combinatorios, su comportamiento puede cambiar de manera importante según la estructura del problema.

En este proyecto se compara experimentalmente el desempeño de BFS y DFS en tres problemas:

- Puzzle 3x3.
- N-Reinas.
- Mochila 0/1.

---

## 2. Metodología General

Las implementaciones fueron desarrolladas en Python. Para la medición experimental se utilizaron principalmente:

- `time.perf_counter()` para medir tiempo de ejecución.
- `tracemalloc` para registrar memoria pico durante la ejecución.
- Contadores explícitos de nodos explorados como métrica auxiliar.

Dentro de cada problema, BFS y DFS se ejecutan bajo las mismas condiciones de entrada, de modo que la comparación entre ambos sea directa.

La complejidad teórica se interpreta de acuerdo con la estructura de cada espacio de búsqueda.

---

## 3. Análisis del Problema de N-Reinas

### 3.1 Descripción del problema

El problema de N-Reinas consiste en ubicar N reinas sobre un tablero de tamaño N × N de manera que ninguna pueda atacar a otra. Esto implica evitar coincidencias en filas, columnas y diagonales.

En la implementación utilizada, el tablero se representa como una lista en la que el índice corresponde a la columna y el valor almacenado corresponde a la fila en la que se ubica la reina.

El objetivo de BFS y DFS es encontrar la primera solución completa válida.

### 4.2 Configuración experimental

Se evaluaron tamaños entre N=4 y N=13. La cantidad de repeticiones disminuye en los valores más grandes debido al aumento significativo del costo de BFS.

| N | Repeticiones por algoritmo |
|---:|---:|
| 4 a 10 | 100 |
| 11 | 50 |
| 12 | 20 |
| 13 | 10 |

Las métricas principales fueron tiempo de ejecución y memoria pico, mientras que los nodos explorados se utilizaron como apoyo para interpretar las diferencias observadas.

### 4.3 Complejidad

El espacio de búsqueda de N-Reinas tiene un comportamiento combinatorio asociado a las diferentes posiciones posibles de las reinas. En el peor caso, el crecimiento se aproxima a una estructura factorial.

| Aspecto | BFS | DFS |
|---------|-----|-----|
| **Tiempo peor caso** | O(N!) | O(N!) |
| **Espacio de frontera** | O(N!) | O(N) |
| **Orden de recorrido** | Nivel por nivel | Rama por rama |
| **Criterio de terminación** | Primera solución completa | Primera solución completa |

DFS resulta espacialmente favorable porque profundiza una rama y mantiene principalmente el camino actual y las alternativas pendientes. BFS, en cambio, puede conservar simultáneamente una gran cantidad de estados pertenecientes al mismo nivel.

### 4.4 Árbol de búsqueda

Para visualizar el comportamiento de ambos algoritmos se utiliza N=4.

![Árbol de búsqueda N-Reinas](../resultados/nreinas/graficas/arboles/arbol_n4.png)

El árbol permite observar que BFS recorre los estados por niveles, mientras DFS avanza en profundidad hasta encontrar una solución o necesitar retroceder.

Esta diferencia de orden es relevante porque en N-Reinas no se requiere encontrar una solución con profundidad mínima: todas las soluciones completas tienen N reinas. Por tanto, recorrer niveles completos antes de profundizar no aporta una ventaja práctica para este criterio de terminación.

### 4.5 Tiempo de ejecución

![Tiempo de ejecución N-Reinas](../resultados/nreinas/graficas/desktop-pcts8tb/01_tiempo_barras.png)

Los resultados muestran una diferencia creciente entre BFS y DFS a medida que aumenta N. Para tamaños pequeños ambos algoritmos pueden completar la búsqueda rápidamente, pero BFS incrementa su costo de forma mucho más marcada en las instancias grandes.

Para N=13, los resultados guardados muestran un tiempo promedio aproximado de **112 segundos para BFS**, mientras DFS se mantiene alrededor de **0,0012 segundos**.

Este comportamiento se explica por la forma en que BFS debe expandir y conservar grandes niveles del espacio de búsqueda antes de llegar a estados completos, mientras DFS puede alcanzar rápidamente una solución profundizando por una secuencia válida de decisiones.

### 4.6 Consumo de memoria

![Memoria N-Reinas](../resultados/nreinas/graficas/desktop-pcts8tb/02_memoria_barras.png)

La diferencia de memoria es todavía más marcada. BFS conserva una frontera amplia y el número de estados almacenados crece rápidamente con N.

Para N=13, BFS alcanza aproximadamente **234.770 KB**, mientras DFS utiliza alrededor de **1,7 KB** en los resultados registrados.

Esto confirma que la principal desventaja práctica de BFS en N-Reinas es el tamaño de la frontera que debe mantener simultáneamente.

### 4.7 Nodos explorados

![Nodos explorados N-Reinas](../resultados/nreinas/graficas/desktop-pcts8tb/03_nodos_barras.png)

La cantidad de nodos explorados muestra que BFS debe procesar una fracción mucho mayor del espacio de búsqueda antes de alcanzar una solución completa.

DFS, al profundizar en una rama válida, puede encontrar la primera solución con una cantidad considerablemente menor de estados procesados.

Por tanto, en este problema la diferencia de tiempo y memoria no se debe únicamente a las estructuras de datos utilizadas, sino también a que el criterio de terminación favorece el orden de recorrido de DFS.

### 4.8 Distribución del tiempo

![Distribución del tiempo N-Reinas](../resultados/nreinas/graficas/desktop-pcts8tb/08_boxplot_tiempo.png)

La distribución temporal permite observar la variabilidad de las mediciones. En los valores mayores de N, BFS presenta ejecuciones mucho más costosas y una dispersión mayor que DFS.

DFS se mantiene relativamente estable debido a que, bajo el orden de generación utilizado, suele alcanzar una primera solución completa después de explorar una cantidad reducida de estados.

### 4.9 Conclusión particular de N-Reinas

Los resultados experimentales muestran que **DFS es considerablemente más eficiente que BFS para encontrar la primera solución del problema de N-Reinas** en esta implementación.

La ventaja de DFS se manifiesta en las tres métricas analizadas: explora menos nodos, requiere menos tiempo y utiliza mucha menos memoria. BFS no obtiene un beneficio práctico por recorrer el espacio nivel por nivel, ya que el problema no exige encontrar una solución de menor profundidad.

---

## 5. Análisis del Problema de Mochila 0/1

### 5.1 Descripción del problema

El problema de Mochila 0/1 consiste en seleccionar un subconjunto de objetos con el propósito de maximizar su valor total sin superar una capacidad máxima de peso.

Cada objeto tiene dos posibilidades:

- No tomarlo.
- Tomarlo, siempre que el peso acumulado no supere la capacidad.

El estado utilizado en la implementación es:

```text
(indice, peso_actual, valor_actual, seleccionados)
```

Cada nivel del árbol representa la decisión asociada a un objeto.

### 5.2 Configuración experimental

Se realizaron 100 instancias aleatorias distribuidas en cinco tamaños:

| Cantidad de objetos | Simulaciones |
|---:|---:|
| 5 | 20 |
| 8 | 20 |
| 10 | 20 |
| 12 | 20 |
| 15 | 20 |

Para cada instancia:

- Los pesos se generan entre 1 y 15.
- Los valores se generan entre 1 y 30.
- La capacidad corresponde aproximadamente al 40 % del peso total.
- Se utiliza `random.seed(42)` para reproducibilidad.
- La misma instancia se ejecuta con BFS y DFS.

En total se realizan 200 ejecuciones: 100 con BFS y 100 con DFS.

### 5.3 Complejidad

En Mochila 0/1, cada objeto puede generar hasta dos decisiones, por lo que el árbol puede crecer exponencialmente.

| Aspecto | BFS | DFS |
|---------|-----|-----|
| **Tiempo peor caso** | O(2^N) | O(2^N) |
| **Espacio de frontera** | O(2^N) | O(N) |
| **Profundidad máxima** | O(N) | O(N) |
| **Orden de recorrido** | Nivel por nivel | Rama por rama |

Ambos algoritmos realizan una búsqueda exhaustiva sobre el mismo árbol factible y, por tanto, presentan la misma complejidad  en el peor caso.

En la implementación concreta, cada estado almacena además la lista de objetos seleccionados, por lo que el consumo real de memoria incluye el costo adicional de almacenar y copiar dicha lista.

### 5.4 Árbol de búsqueda

Para la visualización se utiliza una instancia pequeña con:

- Pesos: `[2, 3, 4, 5]`.
- Valores: `[3, 4, 5, 8]`.
- Capacidad: `8`.

La solución óptima tiene valor **12** y ambos algoritmos exploran **24 nodos**.

![Árbol de búsqueda Mochila 0/1](../resultados/mochila/graficas/arboles/arbol_mochila.png)

La figura presenta el mismo árbol de decisiones para BFS y DFS, pero con diferente orden de visita. Esto es importante porque permite comprobar que la diferencia de desempeño no proviene de que un algoritmo explore menos estados en esta implementación.

### 5.5 Resultados cuantitativos

| Objetos | BFS Tiempo | DFS Tiempo | BFS Memoria | DFS Memoria | Nodos BFS | Nodos DFS |
|--------:|-----------:|-----------:|------------:|------------:|----------:|----------:|
| 5 | 0.00002971 s | 0.00002710 s | 1.3758 KB | 0.1141 KB | 33.30 | 33.30 |
| 8 | 0.00017801 s | 0.00016852 s | 4.0250 KB | 0.2367 KB | 214.25 | 214.25 |
| 10 | 0.00110635 s | 0.00089131 s | 24.3918 KB | 0.3352 KB | 827.70 | 827.70 |
| 12 | 0.00490357 s | 0.00406395 s | 108.3906 KB | 0.4445 KB | 3071.30 | 3071.30 |
| 15 | 0.04147082 s | 0.02388505 s | 1289.9215 KB | 0.6406 KB | 22012.05 | 22012.05 |

Los datos muestran que BFS y DFS exploran exactamente la misma cantidad promedio de nodos para cada tamaño.

Por tanto, las diferencias de tiempo y memoria observadas se relacionan principalmente con la forma en que cada estrategia administra la frontera de búsqueda.

### 5.6 Tiempo de ejecución

![Tiempo promedio Mochila](../resultados/mochila/graficas/comparacion/03_tiempo_por_objetos.png)

En los tamaños pequeños la diferencia temporal entre BFS y DFS es reducida. Esto es esperable porque las ejecuciones duran fracciones muy pequeñas de segundo y el costo fijo de las operaciones puede influir en las mediciones.

A medida que aumenta la cantidad de objetos, la separación se vuelve más clara. Con 15 objetos, BFS tarda aproximadamente **0,04147 s**, mientras DFS tarda aproximadamente **0,02389 s**, lo que representa cerca de **73,63 % más tiempo para BFS**.

Como ambos algoritmos procesan los mismos estados, la diferencia se asocia principalmente al manejo de sus estructuras de frontera.

### 5.7 Consumo de memoria

![Memoria promedio Mochila](../resultados/mochila/graficas/comparacion/04_memoria_por_objetos.png)

La memoria constituye la diferencia más importante en Mochila 0/1.

BFS utiliza una cola FIFO y conserva numerosos estados de un mismo nivel antes de avanzar. Esto provoca que el tamaño de la frontera aumente rápidamente con el número de objetos.

DFS utiliza una pila LIFO y profundiza una rama antes de continuar con las demás alternativas. Por esta razón mantiene simultáneamente una cantidad mucho menor de estados pendientes.

Con 15 objetos, BFS utiliza aproximadamente **1289,92 KB**, mientras DFS utiliza aproximadamente **0,64 KB**. En términos relativos, BFS consume alrededor de **2014 veces** la memoria promedio de DFS.

### 5.8 Comportamiento a lo largo de las simulaciones

![Tiempo por simulación Mochila](../resultados/mochila/graficas/comparacion/01_tiempo_simulaciones.png)

La evolución de los tiempos por simulación evidencia el incremento del costo computacional conforme se pasa a instancias con mayor cantidad de objetos.

![Memoria por simulación Mochila](../resultados/mochila/graficas/comparacion/02_memoria_simulaciones.png)

La gráfica de memoria confirma que el crecimiento de BFS es mucho más pronunciado que el de DFS. La diferencia se hace especialmente visible en las instancias correspondientes a 12 y 15 objetos.

### 5.9 Conclusión particular de Mochila 0/1

En Mochila 0/1, BFS y DFS encuentran el mismo valor óptimo y exploran la misma cantidad de nodos porque ambos realizan una búsqueda exhaustiva sobre el mismo árbol.

Sin embargo, DFS presenta una ventaja clara en consumo de memoria y también un mejor desempeño temporal en las instancias más grandes.

La principal causa no es una reducción del espacio explorado, sino la forma en que cada algoritmo conserva los estados pendientes. BFS mantiene una frontera amplia, mientras DFS mantiene una frontera mucho más pequeña.

---

## 6. Comparación Parcial entre N-Reinas y Mochila 0/1

Los resultados obtenidos permiten observar que DFS resulta más conveniente en ambos problemas, pero por razones diferentes.

En N-Reinas, DFS no solo utiliza menos memoria: también explora considerablemente menos nodos antes de encontrar la primera solución. El criterio de terminación favorece la exploración en profundidad, ya que no es necesario recorrer todos los estados de niveles anteriores para obtener una solución completa.

En Mochila 0/1, en cambio, BFS y DFS recorren el mismo número de estados. La ventaja de DFS proviene principalmente del manejo de la frontera, ya que no necesita conservar simultáneamente un nivel completo del árbol.

| Característica | N-Reinas | Mochila 0/1 |
|----------------|-----------|-------------|
| Crecimiento teórico principal | Factorial O(N!) | Exponencial O(2^N) |
| BFS explora más nodos que DFS | Sí, en los resultados observados | No |
| DFS tiene ventaja en memoria | Sí | Sí |
| DFS tiene ventaja en tiempo | Sí, muy marcada | Sí, principalmente en tamaños grandes |
| Razón principal de la ventaja | Encuentra una solución profunda rápidamente | Mantiene una frontera mucho menor |

Esta comparación muestra que una misma diferencia experimental puede tener causas distintas dependiendo de la estructura del problema.

---

## 7. Conclusiones Generales

Los resultados obtenidos en N-Reinas y Mochila 0/1 permiten concluir que el desempeño de BFS y DFS no puede evaluarse únicamente a partir de su definición teórica como recorridos en anchura o profundidad. La estructura del espacio de estados, el criterio de terminación y la representación de los nodos tienen un efecto directo sobre el tiempo y la memoria utilizados.

En **N-Reinas**, DFS presenta una ventaja muy marcada porque profundiza rápidamente hasta alcanzar una solución completa. BFS, al recorrer nivel por nivel, procesa y mantiene una gran cantidad de estados antes de llegar a la profundidad necesaria. Como consecuencia, DFS explora menos nodos y obtiene resultados considerablemente mejores tanto en tiempo como en memoria.

En **Mochila 0/1**, ambos algoritmos recorren el mismo árbol factible y exploran la misma cantidad de nodos. Esto permite observar con claridad el efecto exclusivo del orden de recorrido y del manejo de la frontera. BFS necesita conservar simultáneamente muchos estados de un mismo nivel, mientras DFS profundiza una rama y mantiene menos alternativas pendientes. Por esta razón, la diferencia más significativa aparece en el consumo de memoria.

Los resultados también muestran que las diferencias entre BFS y DFS se hacen más importantes a medida que aumenta el tamaño de las instancias. En problemas pequeños, ambas estrategias pueden presentar tiempos similares; sin embargo, cuando el espacio de búsqueda crece, la administración de la frontera y el orden de exploración se vuelven determinantes.

Desde el punto de vista teórico, los dos problemas presentan crecimientos distintos. N-Reinas se relaciona con un espacio de búsqueda de naturaleza factorial, mientras Mochila 0/1 presenta una estructura binaria con crecimiento exponencial. Esta diferencia confirma que la complejidad no depende únicamente del algoritmo BFS o DFS, sino también del problema sobre el cual se aplica.

Por tanto, no es correcto afirmar de manera general que BFS o DFS sea siempre superior. **La estrategia más conveniente depende de las características del problema y del objetivo de la búsqueda.** En los dos casos analizados hasta el momento, DFS resultó más favorable, aunque las razones fueron diferentes: en N-Reinas porque alcanza una primera solución recorriendo una fracción mucho menor del espacio, y en Mochila porque administra de forma mucho más eficiente la memoria aun cuando explora los mismos estados que BFS.

La incorporación posterior de Puzzle 3x3 permitirá completar la comparación global y verificar cómo cambia este comportamiento en un problema donde la profundidad de la solución y la garantía de camino mínimo de BFS tienen un papel más importante.

---

## 8. Trabajo Pendiente

La versión final del informe incorporará el análisis de **Puzzle 3x3**, incluyendo:

- configuración experimental,
- resultados globales,
- ejecuciones que alcanzaron el límite experimental,
- comparación de ejecuciones completadas,
- árbol parcial de búsqueda,
- gráficas de tiempo, memoria y nodos,
- conclusión particular del problema.

Después de incorporar Puzzle 3x3, se actualizará la sección de conclusiones generales para integrar los resultados de los tres problemas.

## 9. Análisis del Problema Puzzle 3x3

### 9.1 Descripción

El Puzzle 3x3 consiste en organizar las fichas del 1 al 8 y un espacio vacío (`0`) hasta alcanzar una configuración objetivo.

En este experimento se compararon los algoritmos BFS (Breadth-First Search) y DFS (Depth-First Search), utilizando las mismas configuraciones iniciales para ambos algoritmos.

Las principales métricas analizadas fueron:

- Tiempo de ejecución.
- Consumo de memoria.
- Nodos explorados.
- Cantidad de movimientos.
- Profundidad de la solución.
- Ejecuciones que alcanzaron el límite experimental.

El objetivo es determinar cuál de las dos estrategias presenta un mejor comportamiento para las instancias utilizadas del Puzzle 3x3.

---

### 9.2 Configuración experimental

Se realizaron un total de 100 simulaciones para cada algoritmo.

Las configuraciones utilizadas tenían soluciones de profundidad 6 movimientos. Para evitar que algunas ejecuciones de DFS se prolongaran excesivamente, se estableció un límite máximo de 50.000 nodos explorados.

Este límite permite controlar las ejecuciones que presentan un comportamiento desfavorable y, al mismo tiempo, identificar qué tan estable es cada algoritmo.

Los resultados fueron:

| Algoritmo | Total de ejecuciones |
|---|---:|
| BFS | 100 |
| DFS | 100 |

BFS completó las 100 ejecuciones sin alcanzar el límite, mientras que DFS alcanzó el límite en 49 de las 100 simulaciones.

---

### 9.3 Complejidad y comportamiento

BFS explora el espacio de búsqueda nivel por nivel, mientras que DFS explora una rama en profundidad antes de regresar para continuar con otras alternativas.

En el Puzzle 3x3 esta diferencia es importante porque las soluciones utilizadas en el experimento se encontraban a una profundidad de 6 movimientos.

BFS resulta favorable cuando la solución se encuentra a poca profundidad, ya que explora sistemáticamente los niveles hasta llegar a ella. Además, BFS garantiza encontrar una solución de menor profundidad cuando todos los movimientos tienen el mismo costo.

DFS, en cambio, puede dirigirse inicialmente hacia ramas que no conducen directamente a la solución. Por esta razón, su cantidad de nodos explorados puede aumentar considerablemente dependiendo del orden en que se generen los movimientos.

En este experimento, esta característica produjo una diferencia importante entre ambos algoritmos.

---

### 9.4 Resultados generales

Los resultados estadísticos obtenidos fueron:

| Algoritmo | Ejecuciones exitosas | Tiempo promedio (s) | Memoria promedio (KB) | Nodos promedio |
|---|---:|---:|---:|---:|
| BFS | 100 | 0.000690 | 16.82 | 80.25 |
| DFS | 51 | 0.063014 | 2492.67 | 6979.39 |

En el caso de DFS, las estadísticas mostradas corresponden a las ejecuciones que terminaron exitosamente. Las otras 49 ejecuciones alcanzaron el límite establecido de 50.000 nodos.

BFS presentó un tiempo promedio aproximado de **0.00069 segundos**, mientras que DFS presentó un tiempo promedio de aproximadamente **0.06301 segundos** en sus ejecuciones exitosas.

También existe una diferencia importante en la cantidad de nodos explorados. BFS exploró en promedio **80.25 nodos**, mientras que DFS exploró aproximadamente **6979.39 nodos** en las ejecuciones exitosas.

Esto indica que BFS necesitó explorar una cantidad mucho menor de estados para encontrar las soluciones de las instancias utilizadas.

---

### 9.5 Tiempo de ejecución

La siguiente gráfica muestra la comparación del tiempo de ejecución entre BFS y DFS.

![Tiempo de ejecución Puzzle 3x3](../resultados/puzzle/graficas/01_tiempo.png)

BFS presenta un tiempo promedio considerablemente menor que DFS.

El tiempo promedio de BFS fue de aproximadamente:

**0.00069 segundos**

Mientras que DFS presentó:

**0.06301 segundos**

Por lo tanto, en las ejecuciones exitosas analizadas, DFS tardó considerablemente más tiempo que BFS.

Esta diferencia se relaciona principalmente con la cantidad de estados que DFS necesita explorar antes de encontrar una solución.

Debido a que las soluciones se encuentran a profundidad 6, BFS puede avanzar de manera ordenada por los niveles hasta alcanzar la solución, mientras que DFS puede recorrer ramas que no llevan directamente al objetivo.

---

### 9.6 Consumo de memoria

La siguiente gráfica muestra el consumo promedio de memoria de ambos algoritmos.

![Memoria Puzzle 3x3](../resultados/puzzle/graficas/02_memoria.png)

La diferencia de memoria también es considerable.

BFS presentó un consumo promedio de aproximadamente:

**16.82 KB**

Mientras que DFS presentó:

**2492.67 KB**

Esto muestra que, para las ejecuciones analizadas, DFS tuvo un consumo de memoria mucho mayor.

Aunque normalmente DFS se caracteriza por utilizar una frontera de búsqueda menor que BFS, en estas ejecuciones el comportamiento observado estuvo condicionado por la cantidad de nodos explorados y por los estados que debieron mantenerse durante las búsquedas que se prolongaron.

Por lo tanto, los resultados experimentales muestran que en este conjunto particular de instancias BFS presentó un mejor comportamiento tanto en tiempo como en memoria.

---

### 9.7 Nodos explorados

La siguiente gráfica presenta la cantidad promedio de nodos explorados.

![Nodos explorados Puzzle 3x3](../resultados/puzzle/graficas/03_nodos.png)

BFS exploró aproximadamente:

**80.25 nodos en promedio**

Mientras que DFS exploró:

**6979.39 nodos en promedio**

La diferencia es significativa.

BFS pudo encontrar las soluciones recorriendo principalmente los niveles necesarios para alcanzar la profundidad de 6 movimientos.

DFS, por otro lado, dependió mucho más del orden de exploración. Esto hizo que en varias ejecuciones recorriera ramas que no conducían directamente a la solución.

Como resultado, DFS necesitó explorar una cantidad mucho mayor de estados en las ejecuciones que terminaron exitosamente.

---

### 9.8 Ejecuciones exitosas y ejecuciones que alcanzaron el límite

Para analizar la estabilidad de los algoritmos también se contabilizaron las ejecuciones que alcanzaron el límite de 50.000 nodos.

| Algoritmo | Total | Exitosas | Límite alcanzado | Porcentaje |
|---|---:|---:|---:|---:|
| BFS | 100 | 100 | 0 | 0% |
| DFS | 100 | 51 | 49 | 49% |

![Ejecuciones exitosas y límite Puzzle 3x3](../resultados/puzzle/graficas/04_limites.png)

BFS completó las **100 ejecuciones** sin alcanzar el límite experimental.

DFS, en cambio, completó exitosamente **51 ejecuciones** y alcanzó el límite de 50.000 nodos en **49 ejecuciones**, equivalente al **49%** del total.

Este resultado muestra que DFS presentó una mayor variabilidad en su comportamiento.

En algunas configuraciones DFS encontró rápidamente la solución, pero en otras siguió explorando una gran cantidad de estados sin encontrarla antes de alcanzar el límite establecido.

Por el contrario, BFS presentó un comportamiento mucho más estable en las instancias utilizadas.

---

### 9.9 Resultados de las ejecuciones exitosas

Para analizar únicamente las ejecuciones que terminaron encontrando una solución, se obtuvieron los siguientes resultados:

| Algoritmo | Ejecuciones | Tiempo promedio (s) | Tiempo mediana (s) | Memoria promedio (KB) | Memoria mediana (KB) | Nodos promedio | Movimientos promedio | Profundidad promedio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BFS | 100 | 0.000690 | 0.000632 | 16.82 | 16.48 | 80.25 | 6.00 | 6.00 |
| DFS | 51 | 0.063014 | 0.020424 | 2492.67 | 598.16 | 6979.39 | 6715.14 | 6715.14 |

Las ejecuciones exitosas de BFS presentan una profundidad promedio de **6 movimientos**, coincidiendo con la profundidad de las soluciones utilizadas.

En DFS, la profundidad y los movimientos presentan valores mucho mayores debido al comportamiento de búsqueda en profundidad y a la cantidad de estados explorados antes de encontrar la solución.

Estos resultados permiten observar que no solamente existe una diferencia en el tiempo de ejecución, sino también en la cantidad de estados que cada estrategia necesita recorrer antes de completar la búsqueda.

---

### 9.10 Conclusión del Puzzle 3x3

Para las instancias utilizadas en este experimento, **BFS presentó el mejor desempeño general**.

BFS obtuvo:

- Menor tiempo promedio.
- Menor consumo de memoria.
- Menor cantidad de nodos explorados.
- 100% de ejecuciones exitosas.
- Ninguna ejecución alcanzó el límite experimental.

DFS presentó un comportamiento más variable:

- Mayor tiempo promedio.
- Mayor consumo de memoria en los resultados registrados.
- Mayor cantidad de nodos explorados.
- Solo 51 ejecuciones exitosas.
- 49 ejecuciones alcanzaron el límite de 50.000 nodos.

La principal razón de esta diferencia está relacionada con la profundidad de las soluciones. Como las soluciones utilizadas tenían una profundidad de 6 movimientos, BFS pudo encontrarlas explorando sistemáticamente los niveles hasta llegar a dicha profundidad.

DFS, en cambio, pudo desviarse hacia ramas que no conducían directamente a la solución.

Por lo tanto, para las instancias utilizadas en este experimento, **BFS resultó más eficiente y estable que DFS**.

---

## 10. Comparación de los Tres Problemas

Los experimentos realizados permiten comparar el comportamiento de BFS y DFS en tres problemas con estructuras de búsqueda diferentes:

- N-Reinas.
- Mochila 0/1.
- Puzzle 3x3.

Los resultados muestran que ningún algoritmo fue superior en todos los problemas.

| Característica | N-Reinas | Mochila 0/1 | Puzzle 3x3 |
|---|---|---|---|
| Estrategia más favorable | DFS | DFS | BFS |
| Ventaja principal | Menor tiempo, memoria y nodos | Menor memoria y tiempo | Menor tiempo, memoria y nodos |
| BFS | Mayor costo en las instancias grandes | Mayor consumo de memoria | Mejor desempeño |
| DFS | Muy favorable | Favorable | Mayor variabilidad |
| Influencia de la profundidad | Alta | Media | Alta |

---

### 10.1 N-Reinas

En N-Reinas, DFS presentó mejores resultados porque pudo profundizar rápidamente hasta encontrar una solución completa.

BFS, al recorrer el espacio de búsqueda nivel por nivel, tuvo que mantener una cantidad mucho mayor de estados antes de alcanzar una solución.

Por esta razón, DFS presentó ventajas en tiempo, memoria y cantidad de nodos explorados.

La estructura del problema favorece la búsqueda en profundidad cuando el objetivo es encontrar rápidamente una primera solución válida.

---

### 10.2 Mochila 0/1

En Mochila 0/1, BFS y DFS exploraron la misma cantidad de nodos porque ambos recorrieron el mismo árbol de decisiones.

La diferencia principal estuvo en la forma de administrar la frontera.

BFS mantiene numerosos estados de un mismo nivel, mientras DFS mantiene principalmente la rama que está explorando y las alternativas pendientes.

Por esta razón, DFS presentó un consumo de memoria considerablemente menor y también mejores tiempos en las instancias de mayor tamaño.

En este problema, la ventaja de DFS no se debe a que explore menos nodos, sino principalmente a que utiliza una estructura de búsqueda más pequeña.

---

### 10.3 Puzzle 3x3

En Puzzle 3x3 el comportamiento fue diferente.

BFS presentó mejores resultados porque las soluciones utilizadas tenían una profundidad de 6 movimientos.

Al explorar el espacio por niveles, BFS pudo llegar sistemáticamente a la profundidad donde se encontraban las soluciones.

DFS dependió mucho más del orden de exploración y, como consecuencia, tuvo que recorrer una cantidad considerablemente mayor de estados.

Además, DFS alcanzó el límite de 50.000 nodos en 49 de las 100 simulaciones, mientras que BFS completó todas las ejecuciones sin alcanzar dicho límite.

Por lo tanto, en las instancias utilizadas, BFS fue claramente más favorable para el Puzzle 3x3.

---

### 10.4 Comparación general

Los tres problemas permiten observar que no existe un algoritmo que sea siempre superior.

Los resultados experimentales fueron:

- **N-Reinas → DFS**
- **Mochila 0/1 → DFS**
- **Puzzle 3x3 → BFS**

En N-Reinas, DFS fue favorecido por la posibilidad de alcanzar rápidamente una solución completa.

En Mochila 0/1, DFS presentó una ventaja principalmente en el consumo de memoria, ya que ambos algoritmos exploraron la misma cantidad de estados.

En Puzzle 3x3, BFS fue superior porque las soluciones se encontraban a una profundidad pequeña y el recorrido por niveles permitió encontrarlas de manera sistemática.

Esto demuestra que la elección entre BFS y DFS debe realizarse considerando las características específicas del problema.

---

## 11. Conclusiones Generales

Los resultados obtenidos en N-Reinas, Mochila 0/1 y Puzzle 3x3 muestran que el desempeño de BFS y DFS depende directamente de la estructura del espacio de búsqueda, la profundidad de las soluciones, el criterio de terminación y la forma en que se administran los estados.

En **N-Reinas**, DFS presentó una ventaja clara porque encontró rápidamente una solución completa sin necesidad de recorrer grandes cantidades de estados.

En **Mochila 0/1**, BFS y DFS exploraron el mismo número de nodos, pero DFS presentó una ventaja importante en memoria y mejores tiempos en las instancias más grandes debido a que mantiene una frontera de búsqueda mucho menor.

En **Puzzle 3x3**, BFS presentó los mejores resultados. El algoritmo logró completar las 100 ejecuciones sin alcanzar el límite experimental y necesitó en promedio aproximadamente 80 nodos para encontrar las soluciones. DFS, por el contrario, alcanzó el límite de 50.000 nodos en el 49% de las ejecuciones.

Los experimentos permiten resumir el comportamiento de la siguiente manera:

| Problema | Mejor algoritmo | Principal motivo |
|---|---|---|
| N-Reinas | **DFS** | Encuentra rápidamente una solución y explora menos estados |
| Mochila 0/1 | **DFS** | Utiliza considerablemente menos memoria |
| Puzzle 3x3 | **BFS** | Encuentra soluciones poco profundas de forma sistemática |

Por lo tanto, **BFS no es siempre mejor que DFS, ni DFS es siempre mejor que BFS**.

La estrategia más adecuada depende de factores como:

- Tamaño del espacio de búsqueda.
- Profundidad esperada de la solución.
- Cantidad de estados que deben mantenerse en memoria.
- Criterio utilizado para terminar la búsqueda.
- Necesidad de encontrar una solución de menor profundidad.
- Recursos computacionales disponibles.

En conclusión, los experimentos permiten comprobar que la elección de un algoritmo de búsqueda no debe basarse únicamente en su complejidad teórica. Es necesario considerar también el comportamiento práctico sobre el problema específico.

Los tres experimentos muestran precisamente esta diferencia: **DFS fue más favorable en N-Reinas y Mochila 0/1, mientras que BFS fue más favorable en Puzzle 3x3**.

De esta manera, el análisis experimental demuestra cómo una misma estrategia de búsqueda puede presentar resultados muy diferentes dependiendo de la estructura del problema y de las características de las soluciones que se buscan.
