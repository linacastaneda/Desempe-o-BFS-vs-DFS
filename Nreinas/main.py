#!/usr/bin/env python3
"""
N-Reinas: experimento automatizado BFS vs DFS.

Ejecuta:
1. Simulaciones.
2. Procesamiento de resultados.
3. Gráficas principales.
4. Análisis estadístico.
"""

from graficas import (
    calcular_promedios,
    cargar_resultados,
    generar_todas_graficas,
    obtener_info_maquina,
)

from simulaciones import (
    ejecutar_simulaciones,
    guardar_resultados,
)

from analisis_resultados import (
    cargar_datos,
    comparar_algoritmos,
    exportar_resumenes,
    generar_resumen,
    mostrar_comparacion,
    mostrar_complejidad_teorica,
    mostrar_resumen as mostrar_resumen_detallado,
)


def main():
    """Ejecuta el flujo completo del experimento de N-Reinas."""

    print("=" * 60)
    print("N-REINAS: BFS VS DFS - EXPERIMENTO AUTOMATIZADO")
    print("=" * 60)

    info_maquina = obtener_info_maquina()

    print(f"\nEquipo: {info_maquina['hostname']}")
    print(f"CPU: {info_maquina['procesador']}")
    print(f"RAM: {info_maquina['ram_total_gb']} GB")
    print(f"Python: {info_maquina['python_version']}")

    print("\n[1/4] Ejecutando simulaciones...")

    resultados, info_maquina = ejecutar_simulaciones()

    guardar_resultados(
        resultados,
        info_maquina,
    )

    print("\n[2/4] Procesando resultados...")

    datos = cargar_resultados()

    promedios = calcular_promedios(
        datos
    )

    print("\n[3/4] Generando gráficas principales...")

    nombre_carpeta = (
        info_maquina["hostname"]
        .lower()
        .replace(" ", "_")
    )

    generar_todas_graficas(
        promedios,
        datos,
        carpeta_salida=nombre_carpeta,
    )

    print("\n[4/4] Generando análisis estadístico...")

    datos_analisis = cargar_datos()

    resumen = generar_resumen(
        datos_analisis
    )

    comparacion = comparar_algoritmos(
        resumen
    )

    mostrar_resumen_detallado(
        resumen
    )

    mostrar_comparacion(
        comparacion
    )

    mostrar_complejidad_teorica()

    exportar_resumenes(
        resumen,
        comparacion,
    )

    print("\n" + "=" * 60)
    print("EXPERIMENTO COMPLETADO")
    print("=" * 60)
    print("Resultados: resultados/nreinas/datos/resultados.csv")
    print("Resumen: resultados/nreinas/datos/resumen.csv")
    print("Comparación: resultados/nreinas/datos/comparacion.csv")
    print(
        "Gráficas: "
        f"resultados/nreinas/graficas/{nombre_carpeta}/"
    )
    print("Info máquina: resultados/nreinas/datos/info_maquina.json")


if __name__ == "__main__":
    main()
