#!/usr/bin/env python3
"""
N-Reinas: BFS vs DFS - Experimento Automatizado
Ejecuta experimento completo y genera análisis.
Uso: python main.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bfs import resolver_bfs
from dfs import resolver_dfs
from visualizacion import mostrar_tablero, mostrar_comparacion
from medicion import medir_algoritmo
from simulaciones import ejecutar_simulaciones, guardar_resultados
from graficas import (
    cargar_resultados,
    calcular_promedios,
    generar_todas_graficas,
    obtener_info_maquina
)
from analisis_resultados import (
    cargar_datos,
    generar_resumen,
    comparar_algoritmos,
    mostrar_resumen as mostrar_resumen_detallado,
    mostrar_comparacion,
    analisis_big_o,
    exportar_resumenes
)


def main():
    print("=" * 60)
    print("N-REINAS: BFS vs DFS - EXPERIMENTO AUTOMATIZADO")
    print("=" * 60)
    
    info_maquina = obtener_info_maquina()
    print(f"\nEquipo: {info_maquina['hostname']}")
    print(f"CPU: {info_maquina['procesador']}")
    print(f"RAM: {info_maquina['ram_total_gb']} GB")
    print(f"Python: {info_maquina['python_version']}")
    print()
    
    # 1. Ejecutar simulaciones
    print("[1/4] Ejecutando simulaciones...")
    resultados, info_maquina = ejecutar_simulaciones()
    guardar_resultados(resultados, info_maquina)
    
    # 2. Cargar y procesar resultados
    print("\n[2/4] Procesando resultados...")
    datos = cargar_resultados()
    promedios = calcular_promedios(datos)
    
    # 3. Generar gráficas
    print("\n[3/4] Generando gráficas...")
    nombre_carpeta = info_maquina["hostname"].lower().replace(" ", "_")
    generar_todas_graficas(promedios, datos, carpeta_salida=nombre_carpeta)
    
    # 4. Análisis estadístico
    print("\n[4/4] Análisis estadístico y Big-O...")
    datos_analisis = cargar_datos()
    resumen = generar_resumen(datos_analisis)
    comparacion = comparar_algoritmos(resumen)
    mostrar_resumen_detallado(resumen)
    mostrar_comparacion(comparacion)
    analisis_big_o()
    exportar_resumenes(resumen, comparacion)
    
    print("\n" + "=" * 60)
    print("EXPERIMENTO COMPLETADO")
    print("=" * 60)
    print(f"Resultados CSV: resultados/nreinas/datos/resultados.csv")
    print(f"Resumen:        resultados/nreinas/datos/resumen.csv")
    print(f"Comparación:    resultados/nreinas/datos/comparacion.csv")
    print(f"Gráficas:       resultados/nreinas/graficas/{nombre_carpeta}/")
    print(f"Info máquina:   resultados/nreinas/datos/info_maquina.json")


if __name__ == "__main__":
    main()