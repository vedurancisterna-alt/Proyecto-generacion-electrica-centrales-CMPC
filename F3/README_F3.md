# Fase 3 — Núcleo algorítmico, eficiencia y POO

## Objetivo
Continuar el proyecto de generación eléctrica desarrollado en F1 y F2, incorporando diseño modular, programación estructurada y recursiva, mediciones de complejidad y Programación Orientada a Objetos.

## Notebook principal
`F3/F3_nucleo_algoritmico.ipynb`

## Módulos utilizados
- `src/carga.py`: carga del dataset CEN.
- `src/transformacion.py`: transformación ancho → largo.
- `src/validacion.py`: reglas de validación.
- `src/nucleo_poo.py`: pipeline POO y transformadores.
- `src/agregacion_temporal.py`: patrón Strategy para agregación temporal.
- `src/secuencias.py`: algoritmos iterativo/recursivo y mediciones de eficiencia.

## Ejecución
Desde la raíz del repositorio, abrir el notebook `F3/F3_nucleo_algoritmico.ipynb` en VS Code/Jupyter y seleccionar el kernel del entorno virtual `.venv`. Ejecutar las celdas en orden mediante **Run All**.

En Windows, para verificar el entorno virtual:

```powershell
.\.venv\Scripts\python.exe --version
```

Para comprobar pandas:

```powershell
.\.venv\Scripts\python.exe -c "import pandas; print(pandas.__version__)"
```

Para ejecutar las pruebas independientes del algoritmo de secuencias:

```powershell
.\.venv\Scripts\python.exe src\secuencias.py
```

## Dependencias principales
Las versiones exactas deben conservarse en `requirements.txt`. El proyecto utiliza Python, pandas y Jupyter, además de módulos de la biblioteca estándar como `timeit` y `tracemalloc`.

## Evidencias F3
- Equivalencia del pipeline POO con el dataset procesado de F2.
- Comparación `pandas.melt` vs. `iterrows`.
- Pruebas normal, límite y excepción.
- Algoritmos iterativo y recursivo equivalentes para secuencias de 0 MWh.
- Medición de tiempo con `timeit` y memoria con `tracemalloc`.
- Herencia, polimorfismo y encapsulamiento.
- Patrón Strategy con agregación horaria, diaria, mensual y por día de semana.
- Aplicación sobre las tres centrales del estudio.

## Contribuciones individuales

| Integrante              | Contribución verificable |
|-------------------------|--------------------------|
| Raúl Moya Arriagada     | Implementación inicial de la arquitectura POO de F3 mediante la jerarquía `Transformador`/`Pipeline`; incorporación del patrón Strategy para agregación temporal; benchmark de eficiencia `melt` vs. `iterrows`; verificación de equivalencia con F2; y refactorización de `validacion.py` en reglas atómicas parametrizadas. |
| Verónica Durán Cisterna | Mejoras de F2 según retroalimentación docente; incorporación de `exportacion.py` y ampliación de `transformacion.py` y `validacion.py`; implementación del análisis iterativo y recursivo de secuencias; desarrollo del núcleo algorítmico y análisis de complejidad de F3; documentación técnica de F3; y mejoras de reproducibilidad y benchmark del notebook. |
| Daniela Rojas           | Actualización de los textos Markdown de los notebooks F1, F2 y F3; actualización de configuración del repositorio mediante `.gitignore`; e incorporación y gestión del archivo de datos raw utilizado por F3. |
| Manuel Sánchez          | Refactorización del pipeline POO de F3 para reutilizar funciones existentes de `transformacion.py`, reducir duplicación de lógica e incorporar explícitamente el filtrado temporal mediante `FiltradorPeriodo`; actualización asociada del notebook F3 y de su documentación del pipeline. |

## Reproducibilidad
Los datos crudos pueden permanecer fuera de Git si están excluidos mediante `.gitignore`. El dataset procesado utilizado para verificar la equivalencia con F2 debe conservarse en la ruta documentada por el proyecto. Los resultados de rendimiento pueden variar entre equipos, por lo que las comparaciones deben ejecutarse bajo las mismas condiciones.

