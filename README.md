# Proyecto de Ciencia de Datos – Generación eléctrica en centrales CMPC

## Análisis reproducible de generación eléctrica horaria a partir de datos públicos del CEN

Este repositorio contiene el desarrollo integrado de las **Fases 1, 2, 3 y 4** del proyecto de **Programación para la Ciencia de Datos**.

El proyecto utiliza datos públicos de **Generación Real** publicados por el **Coordinador Eléctrico Nacional (CEN)** y analiza tres centrales asociadas en la fuente a **BIOENERGÍAS FORESTALES SPA**:

- `TER CMPC LAJA`
- `TER CMPC PACIFICO`
- `TER CMPC SANTA FE`

El período de estudio comprende desde el **1 de enero hasta el 31 de agosto de 2026**.

El flujo completo abarca la definición del problema, preparación y validación de datos, construcción de un núcleo algorítmico modular y orientado a objetos, evaluación de eficiencia, análisis temporal, caracterización de registros `0 MWh`, visualización e interpretación de resultados.

> El alcance analítico final se mantiene exclusivamente sobre las tres centrales anteriores, conforme a la delimitación definida en las fases iniciales del proyecto.

---

## Pregunta de investigación

**¿Qué patrones temporales de generación eléctrica caracterizan a las centrales TER CMPC Laja, TER CMPC Pacífico y TER CMPC Santa Fe durante el período enero–agosto de 2026?**

La pregunta articula las cuatro fases del proyecto: F1 define el problema y alcance; F2 prepara y valida los datos; F3 desarrolla el núcleo algorítmico; y F4 consolida el análisis, visualización e interpretación de los resultados.

---

## Problemática

La fuente pública del CEN presenta la información de Generación Real en formato ancho: cada registro corresponde a una combinación central–fecha y contiene 24 columnas horarias (`Hora 1` a `Hora 24`).

Esta estructura requiere transformación para desarrollar análisis temporales a nivel horario. Por ello, el proyecto implementa un flujo reproducible que permite cargar la fuente, verificar su estructura, delimitar el alcance a las tres centrales seleccionadas, transformar las 24 columnas horarias a formato largo, construir variables analíticas, validar la integridad del resultado y posteriormente analizar sus patrones temporales.

La **unidad de observación final** corresponde a una central en una fecha y hora determinada, con su generación eléctrica reportada en MWh.

---

## Objetivo general

Caracterizar los patrones temporales de generación eléctrica de las centrales **TER CMPC Laja, TER CMPC Pacífico y TER CMPC Santa Fe** durante enero–agosto de 2026, utilizando datos públicos de Generación Real del Coordinador Eléctrico Nacional y un proceso reproducible de preparación, validación y análisis.

---

## Objetivos específicos

1. Caracterizar la distribución horaria, diaria y mensual de la generación eléctrica de las tres centrales seleccionadas.
2. Comparar los patrones temporales de generación entre TER CMPC Laja, TER CMPC Pacífico y TER CMPC Santa Fe.
3. Caracterizar la frecuencia y distribución temporal de los registros con generación igual a `0 MWh`, sin atribuir una causa operacional no respaldada por la fuente.
4. Identificar regularidades y diferencias en el comportamiento temporal de las centrales.

---

## Fuente de datos

La fuente utilizada corresponde a la publicación pública **Generación Real** del Coordinador Eléctrico Nacional:

**Fuente oficial:**  
https://www.coordinador.cl/operacion/graficos/operacion-real/generacion-real-/

**Diccionario de Datos Web SIP:**  
https://www.coordinador.cl/wp-content/uploads/2022/11/B43-DIN-04-Diccionario-de-Datos-Web-SIP.pdf

El diccionario utilizado como respaldo documental también se encuentra en:

```text
docs/B43-DIN-04-Diccionario-de-Datos-Web-SIP.pdf
```

El archivo original utilizado para el procesamiento se conserva localmente como:

```text
data/raw/generacion_real_cen_ene_ago_2026.csv
```

El archivo fuente `data/raw/generacion_real_cen_ene_ago_2026.csv` se mantiene versionado en el repositorio para favorecer la reproducibilidad del proyecto y permitir la ejecución completa del flujo F1–F4. Los datos provienen de la fuente pública del Coordinador Eléctrico Nacional (CEN).

### Verificación de integridad de la fuente

Para comprobar que se trabaja con el mismo archivo original y con el mismo dataset procesado, se registran sus características:

| Archivo | Tamaño | Filas × columnas | SHA-256 |
|---|---|---|---|
| `data/raw/generacion_real_cen_ene_ago_2026.csv` | 84.923.560 bytes | 359.891 × 33 | `82c754f772fcc556364a4d47fd82c40ac084b6deecfefcbd3a1e0206be13bdab` |
| `data/processed/dataset_cen_centrales_cmpc_ene_ago_2026.csv` | 2.883.275 bytes | 17.496 × 13 | `a4c5ac11a4e2460d947beef917160914d9b81ee100e1486364f2c9aaf730c3b7` |

Verificación en Windows (PowerShell):

```powershell
certutil -hashfile data\raw\generacion_real_cen_ene_ago_2026.csv SHA256
```

Verificación en Linux o macOS:

```bash
sha256sum data/raw/generacion_real_cen_ene_ago_2026.csv
```

> Los valores corresponden a los archivos tal como se usan en Windows (saltos de línea CRLF). Si Git convierte los saltos de línea al clonar el repositorio en otro sistema, el tamaño y el hash pueden diferir; en ese caso se comparan el número de filas y de columnas.

> El proyecto identifica la información como una fuente de acceso público. No se atribuye una licencia abierta específica mientras esta no haya sido verificada expresamente en los términos de publicación del CEN.

---

## Características del dataset

### Dataset original

La descarga correspondiente al período analizado contiene:

- **359.891 registros**
- **33 columnas**
- período **01-01-2026 a 31-08-2026**
- 24 columnas horarias: `Hora 1` a `Hora 24`
- variables descriptivas como año, mes, central, coordinado, tipo y subtipo

Al delimitar el alcance a las tres centrales seleccionadas se obtienen **729 registros en formato ancho**, equivalentes a **243 fechas por central**.

### Dataset procesado

La transformación ancho → largo genera:

- **17.496 observaciones**
- **13 variables**
- **3 centrales**
- **243 fechas por central**
- **24 observaciones por central y fecha**
- granularidad horaria
- sin valores faltantes
- sin duplicados de la clave analítica
- sin identificadores duplicados
- sin valores negativos de generación

Archivo procesado:

```text
data/processed/dataset_cen_centrales_cmpc_ene_ago_2026.csv
```

---

## Variables del dataset procesado

| Variable | Rol analítico |
|---|---|
| `ID_Observacion` | Identificador único |
| `Año` | Variable temporal |
| `Mes` | Variable temporal discreta |
| `Llave` | Identificador proveniente de la fuente |
| `Central` | Variable categórica nominal |
| `Coordinado` | Variable categórica |
| `Grupo_Reporte` | Variable categórica |
| `Tipo` | Variable categórica |
| `Subtipo` | Variable categórica |
| `Fecha` | Variable temporal |
| `Dia_Semana` | Variable temporal derivada |
| `Hora` | Variable temporal discreta |
| `Generacion_MWh` | Variable cuantitativa continua de interés |

Dentro del alcance de las tres centrales seleccionadas, `Coordinado`, `Tipo` y `Subtipo` presentan un único valor observado. Se conservan para mantener contexto y trazabilidad respecto de la fuente.

---

## Tratamiento de los registros con 0 MWh

Los registros con generación igual a `0 MWh` se conservan como observaciones válidas.

En el dataset procesado se identificaron **4.438 registros con generación igual a 0 MWh**, equivalentes aproximadamente al **25,37 %** de las observaciones.

Su distribución no es homogénea entre las centrales:

- TER CMPC Laja: **3.193 registros (54,75 %)**
- TER CMPC Pacífico: **371 registros (6,36 %)**
- TER CMPC Santa Fe: **874 registros (14,99 %)**

El proyecto **no interpreta automáticamente estos valores como detenciones, fallas o mantenciones**, ya que la fuente utilizada no proporciona evidencia suficiente para atribuirles una causa operacional específica.

---

## Estructura del proyecto

```text
Proyecto/
│
├── F1/
│   └── F1_definicion.ipynb
│
├── F2/
│   └── F2_preparacion_datos.ipynb
│
├── F3/
│   ├── F3_nucleo_algoritmico.ipynb
│   └── README_F3.md
│
├── F4/
│   ├── F4_Consolidado_Proyecto.ipynb
│   └── figuras/              # figuras exportadas por el notebook (PNG, 200 dpi)
│
├── data/
│   ├── raw/
│   │   └── generacion_real_cen_ene_ago_2026.csv
│   └── processed/
│       └── dataset_cen_centrales_cmpc_ene_ago_2026.csv
│
├── docs/
│   ├── B43-DIN-04-Diccionario-de-Datos-Web-SIP.pdf
│   ├── Informe_Tecnico_Sumativa1_Grupo2.docx
│   ├── f3_s02_entregable_grupo2.pdf
│   ├── f4_s03_evaluacion_entregable_grupo2.docx
│   └── evidencias/
│
├── src/
│   ├── __init__.py
│   ├── carga.py
│   ├── exportacion.py
│   ├── transformacion.py
│   ├── validacion.py
│   ├── nucleo_poo.py
│   ├── agregacion_temporal.py
│   └── secuencias.py
│
├── .gitignore
├── .mailmap
├── README.md
├── changelog.md
└── requirements.txt
```

---

## Modularización del código

La lógica reutilizable se encuentra organizada en módulos Python dentro de `src/`.

### `src/carga.py`

Gestiona la comprobación de existencia y carga del archivo de Generación Real del CEN.

### `src/transformacion.py`

Contiene la lógica reutilizable de preparación y transformación del dataset, incluida la transformación desde el formato ancho original al formato largo utilizado para el análisis.

### `src/exportacion.py`

Centraliza la exportación y relectura controlada del dataset procesado para apoyar la reproducibilidad del flujo.

### `src/validacion.py`

Contiene reglas de validación independientes, entre ellas controles de nulos, duplicados, valores negativos, granularidad y categorías esperadas. `validar_dataset_procesado()` compone las reglas para validar integralmente el resultado y mantener compatibilidad con F2 y las fases posteriores.

### `src/nucleo_poo.py`

Implementa la abstracción `Transformador` y cuatro transformadores concretos:

1. `FiltradorPeriodo`
2. `FiltradorCentrales`
3. `TransformadorAnchoLargo`
4. `ConstructorVariablesDerivadas`

La clase `Pipeline` compone estos transformadores y permite ejecutar el flujo de forma secuencial y polimórfica, reutilizando la lógica existente en los módulos funcionales.

### `src/agregacion_temporal.py`

Implementa el patrón de diseño **Strategy** mediante:

- `AgregacionHoraria`
- `AgregacionDiaria`
- `AgregacionMensual`
- `AgregacionPorDiaSemana`
- `CaracterizadorTemporal`

Esto permite intercambiar estrategias de caracterización temporal sin modificar la clase que las utiliza.

### `src/secuencias.py`

Contiene implementaciones iterativa y recursiva para analizar secuencias consecutivas de registros con generación igual a `0 MWh`, junto con funciones utilizadas para resumir estas secuencias por central.

---

# Fases del proyecto

## Fase 1 – Definición del proyecto

`F1/F1_definicion.ipynb` contiene:

- pregunta de investigación;
- problemática;
- objetivo general y objetivos específicos;
- fuente pública y diccionario de datos;
- alcance temporal y analítico;
- unidad de observación;
- variables y roles;
- supuestos y exclusiones;
- reproducibilidad y trazabilidad;
- registro de decisiones;
- configuración del entorno;
- localización reproducible de la raíz;
- carga inicial y validación de estructura.

---

## Fase 2 – Preparación, transformación y validación

`F2/F2_preparacion_datos.ipynb` implementa:

1. carga reproducible;
2. validación del esquema;
3. exploración inicial;
4. conversión y validación de fechas;
5. delimitación reproducible del período y de las tres centrales;
6. transformación ancho → largo;
7. construcción de variables derivadas;
8. validaciones de calidad e integridad;
9. comprobación de variables sin variación;
10. caracterización descriptiva de registros `0 MWh`;
11. validación de 24 observaciones por central y fecha;
12. visualizaciones exploratorias;
13. validación integral mediante `src/validacion.py`;
14. pruebas de caso normal, límite y excepción;
15. exportación y relectura del dataset procesado.

---

## Fase 3 – Núcleo algorítmico, eficiencia y programación orientada a objetos

`F3/F3_nucleo_algoritmico.ipynb` reorganiza y amplía el procesamiento bajo un diseño modular y orientado a objetos, preservando la equivalencia funcional con F2.

El pipeline de F3 posee **cuatro etapas**:

```text
FiltradorPeriodo
      ↓
FiltradorCentrales
      ↓
TransformadorAnchoLargo
      ↓
ConstructorVariablesDerivadas
```

F3 incorpora:

1. clase base `Transformador`, con contrato común para los transformadores;
2. cuatro transformadores concretos;
3. clase `Pipeline`, que ejecuta los pasos de forma polimórfica;
4. reutilización de la lógica funcional existente en `src/`;
5. verificación de equivalencia con el dataset oficial de F2 mediante `pd.testing.assert_frame_equal`;
6. benchmark entre transformación vectorizada con `pandas.melt` e implementación iterativa con `iterrows`;
7. medición de tiempo mediante `timeit`;
8. medición de memoria mediante `tracemalloc`;
9. patrón **Strategy** para agregaciones horaria, diaria, mensual y por día de la semana;
10. análisis de secuencias consecutivas de `0 MWh` mediante enfoques iterativo y recursivo.

### Uso de recursividad

La recursividad no se incorpora artificialmente al pipeline principal porque sus cuatro etapas son fijas y conocidas. Se utiliza en el problema específico de análisis de secuencias consecutivas, donde puede compararse de forma justificada con una implementación iterativa.

---

## Fase 4 – Consolidación, visualización y comunicación de resultados

`F4/F4_Consolidado_Proyecto.ipynb` integra los resultados de las fases anteriores y responde la pregunta de investigación mediante análisis descriptivo y visual.

F4 incorpora:

1. recuperación de la pregunta, objetivos y alcance;
2. carga del dataset procesado de F2;
3. validación integral del dataset;
4. reutilización de las estrategias temporales desarrolladas en F3;
5. estadísticas descriptivas por central;
6. perfil horario de generación;
7. evolución diaria;
8. comportamiento mensual;
9. análisis complementario por día de la semana;
10. comparación entre centrales;
11. frecuencia y distribución temporal de registros `0 MWh`;
12. análisis de secuencias consecutivas de `0 MWh`;
13. síntesis de resultados;
14. discusión y limitaciones;
15. conclusiones vinculadas con los objetivos;
16. trazabilidad F1 → F2 → F3 → F4;
17. vinculación de la reflexión metodológica de la Fase 4 con las decisiones técnicas, la reproducibilidad y la trazabilidad del proyecto.


### Figuras exportadas

Al ejecutar F4, cada figura se guarda con `fig.savefig(..., dpi=200, bbox_inches="tight")` en `F4/figuras/`. Son las mismas figuras que usan el informe y el video, y se presentan como un relato en tres movimientos:

| Archivo | Figura | Movimiento |
|---|---|---|
| `figura_1_perfil_horario.png` | Perfil horario promedio por central | Contexto |
| `figura_2_media_mensual.png` | Generación media por hora, por mes | Contraste |
| `figura_3_horas_cero.png` | Porcentaje de horas con 0 MWh por central y mes | Resolución |
| `figura_A_evolucion_diaria.png` | Generación total diaria (complementaria) | — |
| `figura_B_dia_semana.png` | Generación media por día de la semana (complementaria) | — |

Bajo cada figura, el notebook responde qué muestra, qué se infiere, qué límite tiene y cómo aporta al relato.

### Principales resultados

Las estadísticas descriptivas muestran comportamientos diferenciados:

| Central | Media MWh | Mediana MWh | Registros 0 MWh | % 0 MWh |
|---|---:|---:|---:|---:|
| TER CMPC LAJA | 3,45 | 0,0 | 3.193 | 54,75 % |
| TER CMPC PACIFICO | 16,19 | 17,8 | 371 | 6,36 % |
| TER CMPC SANTA FE | 5,14 | 5,7 | 874 | 14,99 % |

TER CMPC Pacífico presenta el mayor nivel de generación durante el período analizado. TER CMPC Santa Fe presenta niveles intermedios, mientras que TER CMPC Laja registra la mayor proporción de observaciones iguales a `0 MWh`.

Las escalas horaria, diaria y mensual permiten observar que las diferencias entre centrales no se limitan al nivel medio de generación, sino que también se manifiestan en sus trayectorias temporales y en la distribución de los registros iguales a cero.

Estos resultados son **descriptivos** y no permiten atribuir causas técnicas u operacionales a las variaciones observadas.

---

## Decisiones de preprocesamiento

La inspección de la fuente no identificó valores nulos ni registros duplicados exactos dentro del dataset utilizado, por lo que no fue necesario aplicar imputación.

Tampoco se aplicó normalización o escalamiento a `Generacion_MWh`, porque el análisis busca preservar la magnitud original reportada en MWh.

Las principales operaciones corresponden a casting de tipos, delimitación del alcance, transformación ancho–largo, construcción de variables derivadas y validación de integridad.

---

## Reproducibilidad

La **reproducibilidad** corresponde a la capacidad de volver a ejecutar el procesamiento y análisis utilizando la fuente, código, estructura y entorno documentados.

El proyecto utiliza:

- Python;
- Jupyter Notebook;
- entorno virtual `.venv`;
- `requirements.txt`;
- rutas relativas;
- módulos reutilizables en `src/`;
- validaciones automáticas;
- fuente pública identificada;
- transformación codificada;
- notebooks ejecutables secuencialmente.

### Instalación de dependencias

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Verificación del entorno

Cada notebook (F1 a F4) imprime en su primera celda de código las versiones de Python, pandas y NumPy y comprueba que el entorno virtual esté activo:

```python
print("Entorno virtual activo:", sys.prefix != sys.base_prefix)
```

El resultado esperado es `True`. Si aparece `False`, el kernel no corresponde al `.venv` del proyecto y hay que seleccionarlo antes de ejecutar.

Si se agrega o actualiza alguna librería, `requirements.txt` debe regenerarse desde el mismo entorno donde se ejecutan los notebooks, para que las versiones declaradas sean las que realmente se usaron:

```powershell
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt
```

---

## Instrucciones de ejecución

### 1. Preparar la fuente

Descargar desde el CEN la información de Generación Real correspondiente a enero–agosto de 2026 y guardarla como:

```text
data/raw/generacion_real_cen_ene_ago_2026.csv
```

### 2. Instalar dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Ejecutar F1

Abrir:

```text
F1/F1_definicion.ipynb
```

Seleccionar el kernel del entorno virtual y ejecutar **Restart Kernel → Run All**.

### 4. Ejecutar F2

Abrir:

```text
F2/F2_preparacion_datos.ipynb
```

Ejecutar **Restart Kernel → Run All**.

Al finalizar debe generarse:

```text
data/processed/dataset_cen_centrales_cmpc_ene_ago_2026.csv
```

### 5. Ejecutar F3

Abrir:

```text
F3/F3_nucleo_algoritmico.ipynb
```

Ejecutar **Restart Kernel → Run All**. F3 utiliza el dataset procesado generado y validado en F2.

### 6. Ejecutar F4

Abrir:

```text
F4/F4_Consolidado_Proyecto.ipynb
```

Ejecutar **Restart Kernel → Run All**. F4 utiliza el dataset procesado y reutiliza componentes desarrollados en F3 para consolidar el análisis final.

El orden recomendado es:

```text
F1 → F2 → F3 → F4
```

---

## Trazabilidad y control de versiones

La **trazabilidad** permite reconstruir la evolución del proyecto, sus decisiones y contribuciones.

Se utilizan:

- Git para control de versiones local;
- GitHub como repositorio remoto;
- ramas de trabajo;
- commits descriptivos;
- merges colaborativos;
- `changelog.md`;
- notebooks documentados;
- README;
- evidencias de ejecución.

El archivo fuente utilizado por el proyecto se mantiene en `data/raw/` y el dataset procesado se incorpora en `data/processed/`, permitiendo reproducir y verificar el flujo completo de procesamiento.

---

## Validaciones técnicas

Las principales verificaciones incluyen:

- existencia del archivo fuente;
- esquema y columnas esperadas;
- presencia de las centrales definidas;
- dimensiones esperadas;
- unicidad de `ID_Observacion`;
- ausencia de duplicados central–fecha–hora;
- ausencia de valores faltantes;
- ausencia de generación negativa;
- cobertura temporal;
- exactamente 24 observaciones por central y fecha;
- categorías esperadas;
- exportación y relectura del resultado;
- pruebas de caso normal, límite y excepción;
- equivalencia funcional entre F2 y F3.

---

## Tecnologías utilizadas

- Python
- Jupyter Notebook
- Visual Studio Code
- Pandas
- NumPy
- Matplotlib
- Git
- GitHub

---

## Vinculación entre las fases

| Fase | Propósito | Resultado principal |
|---|---|---|
| **F1** | Definición | Problema, pregunta, objetivos, alcance y entorno reproducible |
| **F2** | Preparación | Dataset horario procesado y validado |
| **F3** | Núcleo algorítmico | POO, pipeline de cuatro etapas, Strategy, eficiencia y secuencias |
| **F4** | Consolidación | Análisis, visualizaciones, interpretación, discusión y conclusiones |

La integración de las cuatro fases permite mantener continuidad entre **problema → datos → procesamiento → algoritmos → análisis → resultados → conclusiones**.

---

## Estado actual

- F1 finalizado y ejecutado mediante `Restart Kernel → Run All`.
- F2 finalizado y ejecutado mediante `Restart Kernel → Run All`.
- F3 finalizado, con pipeline de cuatro etapas, POO, patrón Strategy, benchmark y análisis de secuencias.
- F4 finalizado y ejecutado mediante `Restart Kernel → Run All`.
- Dataset procesado validado: **17.496 observaciones y 13 variables**.
- Alcance final: **TER CMPC Laja, TER CMPC Pacífico y TER CMPC Santa Fe**.
- Análisis horario, diario, mensual y de registros `0 MWh` consolidado.
- Pipeline modularizado en `src/`.
- Diccionario de datos CEN incorporado en `docs/`.
- Fuente pública documentada.
- Repositorio gestionado mediante Git y GitHub.
- Trazabilidad F1 → F2 → F3 → F4 documentada.

---

## Contribuciones individuales

Las contribuciones de F3 se documentan en `F3/README_F3.md`. Las de F4 se resumen aquí; cada una se puede verificar con `git log --author="<nombre>" --oneline -- F4/`.

| Integrante | Contribución verificable en F4 |
|---|---|
| Verónica Durán Cisterna | Inicio de F4 con consolidación y análisis temporal (`3da2753`); desarrollo del análisis, visualizaciones e interpretación de resultados (`513d05b`); y fortalecimiento de la discusión metodológica (`64d8464`). |
| Raúl Moya Arriagada | Rediseño de las figuras analíticas con títulos orientados al hallazgo, color consistente por central y ejes desde cero (`7ad92d9`); además de ajustes finales asociados al entorno reproducible y pruebas del proyecto (`d9a94ab`). |
| Daniela Rojas Vilches | Limpieza de metadatos y outputs del notebook F4 (`024204c`) e incorporación de la prueba de equivalencia mediante `assert_frame_equal` (`3dc543e`). |
| Manuel Sánchez Cárcamo | Mejora de las figuras analíticas 1, 2 y 3 mediante incorporación de fuente e interpretación analítica (`9158bda`, `c7aaee2`, `9cdf8c7`). |


---

## Integrantes

- Verónica Durán Cisterna
- Raúl Moya Arriagada
- Daniela Rojas Vilches
- Manuel Sánchez Cárcamo

---

## Referencias principales

- Coordinador Eléctrico Nacional. *Generación Real*.  
  https://www.coordinador.cl/operacion/graficos/operacion-real/generacion-real-/

- Coordinador Eléctrico Nacional. *Diccionario de Datos Web SIP*.  
  https://www.coordinador.cl/wp-content/uploads/2022/11/B43-DIN-04-Diccionario-de-Datos-Web-SIP.pdf

- Python Software Foundation. *Python Documentation*.  
  https://docs.python.org/

- Pandas Development Team. *Pandas Documentation*.  
  https://pandas.pydata.org/docs/

- NumPy Developers. *NumPy Documentation*.  
  https://numpy.org/doc/

- Matplotlib Development Team. *Matplotlib Documentation*.  
  https://matplotlib.org/stable/

