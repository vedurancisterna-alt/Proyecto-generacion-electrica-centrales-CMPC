# Changelog

Registro de las mejoras técnicas incorporadas durante la evolución del proyecto F1–F4.
Cada cambio se vincula con un commit verificable del repositorio y documenta su
justificación e impacto técnico.

| Fecha | Descripción del cambio | Commit | Justificación técnica | Impacto |
|---|---|---|---|---|
| 2026-09-16 | Modularización del pipeline de datos de F1 y F2 mediante módulos separados para carga, transformación y validación. | `550cfc6` | Separar responsabilidades evita concentrar la lógica de procesamiento en los notebooks y facilita reutilización, validación y mantenimiento. | Mayor modularidad, claridad y mantenibilidad. |
| 2026-09-22 | Unificación de las identidades Git de los integrantes mediante `.mailmap`. | `5e60e7f` | Consolidar las distintas identidades utilizadas en Git permite atribuir correctamente las contribuciones individuales y mantener un historial consistente. | Mejora de trazabilidad y documentación colaborativa. |
| 2026-09-23 | Corrección complementaria de `.mailmap` para consolidar completamente la identidad Git de Verónica Durán. | `ce134a7` | Corregir una identidad aún no consolidada evita fragmentación en el historial de autoría. | Mayor precisión de la trazabilidad individual. |
| 2026-09-23 | Refactorización de `validacion.py` en reglas atómicas parametrizadas. | `a4e655d` | La separación de las validaciones en reglas independientes y parametrizables mejora su reutilización y permite aplicar controles específicos desde distintas fases del proyecto. | Mayor modularidad, reutilización y claridad del proceso de validación. |
| 2026-09-25 | Corrección de F1 y F2 para asegurar ejecución reproducible de los notebooks. | `fd08c0f` | Se ajustaron los notebooks para que su ejecución pueda repetirse de manera consistente dentro del entorno configurado. | Mejora de reproducibilidad técnica. |
| 2026-09-25 | Incorporación de benchmark completo y mejoras derivadas de la retroalimentación en F3. | `1d67d9b` | Las mediciones permiten respaldar las decisiones algorítmicas con evidencia reproducible de desempeño. | Mejora del análisis de eficiencia y de la fundamentación técnica. |
| 2026-09-26 | Refactorización del pipeline POO e incorporación explícita del filtrado temporal. | `2a7372f` | Se reutilizó lógica existente de transformación y se incorporó `FiltradorPeriodo`, reduciendo duplicación y delimitando mejor las responsabilidades del pipeline. | Mayor cohesión, reutilización y mantenibilidad de la arquitectura POO. |
| 2026-09-27 | Documentación de las contribuciones individuales realizadas durante F3. | `4840598` | Registrar las contribuciones permite relacionar el trabajo técnico con los integrantes responsables y con los commits existentes. | Mejora de trazabilidad y documentación del trabajo colaborativo. |
| 2026-09-28 | Inicio de F4 mediante notebook de consolidación y análisis temporal. | `3da2753` | La Fase 4 requiere integrar los resultados obtenidos durante las fases anteriores y preparar su análisis y comunicación final. | Inicio de la integración F1–F4 y comunicación analítica. |