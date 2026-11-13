# 10 — Python para analítica de nivel experto

PY-015 a PY-028. Retos de arquitectura de datos, validación estadística, rendimiento y resiliencia. Se prioriza diseño explicable y pruebas reproducibles sobre dependencia de una librería específica.

**Contrato general:** el agente de Cursor debe mostrar únicamente este enunciado, crear stubs bajo `workspaces/python/` cuando el estudiante lo pida y dejar la implementación pendiente. **No incluir soluciones, SQL de respuesta, algoritmos funcionales ni resultados precalculados.**

## PY-015 — Pipeline ETL incremental end-to-end

**Objetivo y trabajo solicitado.** Diseñar extractor SQL -> transformación validada -> carga idempotente de `analytics.daily_sales` con checkpoints y reintentos.

**Aceptación / pruebas obligatorias.** Segunda ejecución no duplica; reinicio tras fallo parcial; backfill de intervalo; recuperación tras entrada malformada.

**Entrega.** `PY-015.py`, módulos propios + tests integración + runbook.

**Restricciones y extensiones.** No resolver antes SQL-023; business logic debe ser explícita y revisable.

## PY-016 — Pandas vs Polars vs DuckDB

**Objetivo y trabajo solicitado.** Implementar mismo análisis sobre Parquet grande en tres motores y comparar semántica, CPU, memoria, claridad y coste de importación.

**Aceptación / pruebas obligatorias.** Equivalencia numérica, dataset `medium` o mayor, mediciones repetidas, memoria observada.

**Entrega.** `PY-016.py` + benchmark reproducible.

**Restricciones y extensiones.** No optimizar sacrificando semántica; justificar procesado lazy.

## PY-017 — Procesamiento streaming y backpressure

**Objetivo y trabajo solicitado.** Construir pipeline de transformación de eventos que no acumule todo en RAM y con límite de buffers.

**Aceptación / pruebas obligatorias.** Entrada de 1M eventos; caída de consumidor; entrada más rápida que salida; finalización ordenada.

**Entrega.** `PY-017.py` + tests de presión y métricas.

**Restricciones y extensiones.** Documentar cuándo usar generadores, colas y batch sizes.

## PY-018 — Detección estadística de anomalías

**Objetivo y trabajo solicitado.** Diseñar comparación robusta de ventas diarias con estacionalidad semanal y threshold calibrable; proporcionar intervalos y falsos positivos.

**Aceptación / pruebas obligatorias.** Sin datos suficientes, varianza cero, valores extremos, ventanas parciales; resultados comparados con baseline estadístico.

**Entrega.** `PY-018.py` + protocolo de validación.

**Restricciones y extensiones.** No afirmar causalidad ni utilizar modelos opacos innecesarios.

## PY-019 — Cohortes/retención escalables

**Objetivo y trabajo solicitado.** Construir matriz de retención desde órdenes y clientes sin cargar innecesariamente eventos; comparar contra SQL-017.

**Aceptación / pruebas obligatorias.** Cada cliente cuenta una vez por celda; cohortes recientes con observación truncada; manejar tenant sin actividad.

**Entrega.** `PY-019.py` + matriz y tests de consistencia.

**Restricciones y extensiones.** Definiciones reproducibles y fecha de ancla fija; no simplificar el sesgo temporal.

## PY-020 — Inferencia y tests de hipótesis

**Objetivo y trabajo solicitado.** Evaluar si cambia tasa de conversión entre dos períodos o grupos sintéticos, definiendo hipótesis, tamaño muestral y limitaciones.

**Aceptación / pruebas obligatorias.** Reportar efecto, incertidumbre, test y supuestos; casos con conteo cero y muestra pequeña.

**Entrega.** `PY-020.py` + breve memo de decisión.

**Restricciones y extensiones.** No usar p-values como garantía causal; explicar confusores.

## PY-021 — Experimento A/B reproducible

**Objetivo y trabajo solicitado.** Simular asignación aleatoria estable de sesiones a variantes e implementar evaluación con guardrails y métricas primarias.

**Aceptación / pruebas obligatorias.** Semilla controlada, grupos reproducibles, SRM check, intervalos de confianza, peeking policy.

**Entrega.** `PY-021.py` + protocolo A/B.

**Restricciones y extensiones.** No usar datos observacionales como si fueran experimentales sin advertencia.

## PY-022 — Data contracts versionados

**Objetivo y trabajo solicitado.** Definir schemas de entrada/salida para source raw y versión de contrato; manejar backcompat y registros de versión antigua.

**Aceptación / pruebas obligatorias.** Contrato v1/v2, compatibilidad explícita, campos añadidos/renombrados, dead-letter.

**Entrega.** `PY-022.py` + contratos y migración semántica.

**Restricciones y extensiones.** Los tests deben detectar cambios de schema inesperados.

## PY-023 — Orquestación y retries seguros

**Objetivo y trabajo solicitado.** Crear pequeño DAG ETL con dependencias, retry backoff, timeout, checkpoints y tareas idempotentes.

**Aceptación / pruebas obligatorias.** Fallo antes/después de commit; reejecución; no ejecución doble de paso irreversible.

**Entrega.** `PY-023.py` + diagrama de estado y runbook.

**Restricciones y extensiones.** No es obligatorio Airflow: justificar herramienta o librería mínima.

## PY-024 — Data quality con SLAs

**Objetivo y trabajo solicitado.** Diseñar motor de reglas de completitud, unicidad, rango, freshness, volumen y consistencia referencial; persistir findings.

**Aceptación / pruebas obligatorias.** Un run_id por ejecución, severidades, tendencias, reportes históricos, no duplicar hallazgos por retries.

**Entrega.** `PY-024.py` + reglas y tests con JSON corrupto.

**Restricciones y extensiones.** No enmascarar defectos arreglando automáticamente canonical core.

## PY-025 — Optimización de memoria en ETL

**Objetivo y trabajo solicitado.** Perfilado de consumo extremo al transformar 100k+ órdenes y eventos: introducir chunks, tipos compactos, pushdown selectivo.

**Aceptación / pruebas obligatorias.** Registro antes/después de RSS, memoria máxima, rendimiento, correctitud y escala.

**Entrega.** `PY-025.py` + informe de profiling.

**Restricciones y extensiones.** No usar muestreo engañoso para afirmar ahorro general.

## PY-026 — Diseño de librería analítica

**Objetivo y trabajo solicitado.** Convertir tres implementaciones propias a paquete modular con API estable, typing, docs, errores y versionado semántico.

**Aceptación / pruebas obligatorias.** Interfaces públicas documentadas, tests, instalación limpia, import sin efectos secundarios.

**Entrega.** `PY-026` package + README y changelog.

**Restricciones y extensiones.** Evitar dependencias cíclicas, globales y secretos en código.

## PY-027 — Validación de snapshots y diffs

**Objetivo y trabajo solicitado.** Comparar extractos Parquet de días distintos para cambios de esquema, altas/bajas, cambios de valores y drift de distribuciones.

**Aceptación / pruebas obligatorias.** Escala, igualdad por clave compuesta, nulos, duplicados, distribuciones vacías; hashes no dependen del orden.

**Entrega.** `PY-027.py` + reporte explicativo.

**Restricciones y extensiones.** No inferir baja real de un cliente solo por ausencia en muestra incompleta.

## PY-028 — Proyecto de detección de regresiones

**Objetivo y trabajo solicitado.** Diseñar suite que compare KPIs de dos versiones de pipeline y detecte drift por tenant con tolerancias justificadas.

**Aceptación / pruebas obligatorias.** Cobertura por categoría, outliers conocidos y comparación Decimal; failure cases reproducibles.

**Entrega.** `PY-028.py` + matriz de regresiones.

**Restricciones y extensiones.** No hardcodear valores de la semilla como única referencia.

## Evaluación

No basta con que el resultado parezca razonable: el estudiante debe justificar semántica, comprobar bordes, declarar supuestos, defender costes y documentar cómo verificó sus resultados. La IA revisará, no sustituirá, la implementación.
