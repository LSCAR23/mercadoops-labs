# 09 — Laboratorios Python: bases profesionales

PY-001 a PY-014. Enfocados en código de producción testeable para análisis de datos. Se exige Python moderno, funciones pequeñas, manejo de errores, typing y separación de IO/transformación.

**Contrato general:** Copilot debe mostrar únicamente este enunciado, crear stubs bajo `workspaces/python/` cuando el estudiante active el laboratorio y dejar la implementación pendiente. **No incluir soluciones, SQL de respuesta, algoritmos funcionales ni resultados precalculados.**

## PY-001 — Tipado, validación y parsing

**Objetivo y trabajo solicitado.** Implementar un parser de un registro de venta externo (diccionario JSON) a tipo inmutable, sin depender de la BD. Validar importe, moneda, email y timestamp.

**Aceptación / pruebas obligatorias.** Input válido; nulos; clave ausente; cantidad negativa; formato erróneo; zona horaria ausente; retorna errores definidos, no traceback crudo.

**Entrega.** `workspaces/python/PY-001.py` + `tests/student/test_py001.py` propios.

**Restricciones y extensiones.** No arreglar silenciosamente errores sin un contrato; `Decimal` para dinero.

## PY-002 — Normalización de entradas

**Objetivo y trabajo solicitado.** Diseñar una transformación de texto configurable: espacios, casing, código ISO y valores faltantes, sin perder el valor original.

**Aceptación / pruebas obligatorias.** Operación idempotente; caracteres Unicode; cadena vacía; no muta estructuras de entrada; casos invalidos.

**Entrega.** `PY-002.py` + matriz input/expected creada por estudiante.

**Restricciones y extensiones.** Separar limpieza de validación y registrar pérdida de información.

## PY-003 — Lectura batch CSV/JSONL

**Objetivo y trabajo solicitado.** Crear lector streaming de archivos de grandes volúmenes con manejo de codificación, filas inválidas y métrica de progreso.

**Aceptación / pruebas obligatorias.** Archivo vacío, línea truncada, encoding incorrecto, 1M líneas sin cargar todo en memoria.

**Entrega.** `PY-003.py`, CLI y fixtures generados por estudiante.

**Restricciones y extensiones.** Evitar `read()` del archivo completo; reportar ubicación de error.

## PY-004 — Extracción SQL parametrizada

**Objetivo y trabajo solicitado.** Diseñar función que lea paginadamente órdenes de un tenant/rango y entregue lotes tipados a transformación posterior.

**Aceptación / pruebas obligatorias.** No inyección SQL, manejo de desconexión, tenant inexistente, orden estable, página final parcial.

**Entrega.** `PY-004.py` + test con BD de prueba.

**Restricciones y extensiones.** Prohibido usar `OFFSET` sin explicar degradación en volúmenes grandes.

## PY-005 — Pandas: agrupación y precisión

**Objetivo y trabajo solicitado.** Crear DataFrame de líneas/pagos, definir tipos, agregar por mes y detectar inconsistencias por join.

**Aceptación / pruebas obligatorias.** Pérdida nula de filas inesperada; test de duplicados y valores nulos; precisión monetaria contrastada con SQL.

**Entrega.** `PY-005.py` + reporte tabular.

**Restricciones y extensiones.** No usar float para afirmar concordancia exacta en dinero; validar tipos.

## PY-006 — Fechas, zonas y calendario

**Objetivo y trabajo solicitado.** Transformar timestamps UTC a calendario empresarial parametrizable y modelar semanas, meses, años fiscales.

**Aceptación / pruebas obligatorias.** Cambios de horario de verano en zonas que los usan; fin de mes y año; timestamps sin tz rechazados o tratados por política explícita.

**Entrega.** `PY-006.py` + pruebas de frontera.

**Restricciones y extensiones.** No asumir que Costa Rica y todas las zonas tienen DST.

## PY-007 — Funciones puras y testabilidad

**Objetivo y trabajo solicitado.** Separar lógica de cálculo de KPI de acceso SQL/IO; definir interfaces y fixtures de casos límite.

**Aceptación / pruebas obligatorias.** Función pura produce igual output para igual input, sin conexiones; mutación de input detectada; 0 órdenes.

**Entrega.** `PY-007.py` + tests propios.

**Restricciones y extensiones.** No usar un notebook como única implementación verificable.

## PY-008 — Exportación Parquet y contrato de schema

**Objetivo y trabajo solicitado.** Construir exportador de órdenes a Parquet particionado, con schema explícito, metadata y archivo manifest.

**Aceptación / pruebas obligatorias.** Relectura conserva dtypes de UUID, timestamps y dinero según contrato; particiones vacías y reejecución.

**Entrega.** `PY-008.py` + manifest de ejemplo.

**Restricciones y extensiones.** No sobrescribir resultados de otra fecha/tenant inadvertidamente.

## PY-009 — CLI robusta

**Objetivo y trabajo solicitado.** Crear comando de línea de comandos para ejecutar una transformación de dataset por tenant, ventana y salida, con flags de dry-run.

**Aceptación / pruebas obligatorias.** Argumentos inválidos salen con código no cero; `--help` completo; no elimina archivos existentes sin flag.

**Entrega.** `PY-009.py` + ejemplos de comandos.

**Restricciones y extensiones.** La lógica y CLI deben estar desacopladas; no filtrar secretos por consola.

## PY-010 — Calidad de datos mediante reglas

**Objetivo y trabajo solicitado.** Definir reglas pluggable de validación para `raw_orders` y reporte por rule_id / severidad; sin corregir automáticamente datos.

**Aceptación / pruebas obligatorias.** Registros pueden fallar varias reglas; no se pierde información; comportamiento ante JSON incompleto y campos inesperados.

**Entrega.** `PY-010.py` + suite de casos.

**Restricciones y extensiones.** La tabla `analytics.data_quality_issues` sigue vacía hasta que el estudiante implemente pipeline.

## PY-011 — Visualización responsable

**Objetivo y trabajo solicitado.** Construir visualizaciones de tendencia, segmentos y distribución usando datos propios y ejes apropiados.

**Aceptación / pruebas obligatorias.** Anotar fuente, definición, fecha de corte, nulos y tamaño de muestra; no utilizar ejes engañosos.

**Entrega.** `PY-011.py` o notebook + gráficos exportados.

**Restricciones y extensiones.** No confundir correlación con causalidad.

## PY-012 — Validación cruzada SQL/Python

**Objetivo y trabajo solicitado.** Seleccionar dos KPIs implementados en SQL y reimplementarlos en Python, comparar resultados por tenant/mes y reportar discrepancias.

**Aceptación / pruebas obligatorias.** Comparar mismos filtros, estados, timezone y precisión; discrepancias trazables por grupo.

**Entrega.** `PY-012.py` + reporte de reconciliación.

**Restricciones y extensiones.** Prohibido copiar simplemente el resultado SQL a Python y llamarlo validación.

## PY-013 — Profiling de rendimiento y memoria

**Objetivo y trabajo solicitado.** Comparar iteración fila a fila versus operaciones vectorizadas en muestra controlada, preservando resultados y midiendo memoria.

**Aceptación / pruebas obligatorias.** Tres repeticiones, tamaños de datos anotados, calentamiento, exactitud del output.

**Entrega.** `PY-013.py` + tabla de benchmarks.

**Restricciones y extensiones.** No declarar una opción más rápida sin medir; controlar overhead de lectura.

## PY-014 — Refactor de un pipeline heredado

**Objetivo y trabajo solicitado.** Tomar una implementación propia anterior y eliminar funciones largas, side effects, estados globales, duplicación y errores silenciosos.

**Aceptación / pruebas obligatorias.** Comparar tests antes/después, complejidad y cobertura de errores sin alterar resultados.

**Entrega.** `PY-014.py` + informe de cambios.

**Restricciones y extensiones.** Debe existir versión original del estudiante; Copilot no inventará el código heredado.

## Evaluación

No basta con que el resultado parezca razonable: el estudiante debe justificar semántica, comprobar bordes, declarar supuestos, defender costes y documentar cómo verificó sus resultados. La IA revisará, no sustituirá, la implementación.
