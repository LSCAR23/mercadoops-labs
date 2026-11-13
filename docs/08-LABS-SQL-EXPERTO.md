# 08 — SQL avanzado y analítica experta

SQL-015 a SQL-030. Requiere completar fundamentos, comprender EXPLAIN, estadística descriptiva y distinción entre datos operacionales y analíticos. Varios retos requieren una BD descartable dedicada.

**Contrato general:** el agente de Cursor debe mostrar únicamente este enunciado, crear stubs bajo `workspaces/sql/` cuando el estudiante lo pida y dejar la implementación pendiente. **No incluir soluciones, SQL de respuesta, algoritmos funcionales ni resultados precalculados.**

## SQL-015 — Ranking top-N por grupo

**Objetivo y trabajo solicitado.** Ranking de categorías/productos por ingreso neto y unidades, top-N por tenant/mes; resolver empates y mostrar comparación con mes previo.

**Aceptación / pruebas obligatorias.** Con N=3 y empates se sabe si hay exactamente tres filas o más por política declarada; test con tenant sin ventas.

**Entrega.** `SQL-015.sql`, notas sobre ranking y desempate.

**Restricciones y extensiones.** Usar ventana analítica apropiada; prohibido asumir que ORDER BY interno garantiza orden final.

## SQL-016 — Ventanas móviles 7/30 días

**Objetivo y trabajo solicitado.** Crear series diarias, sumas móviles, medias y diferencia porcentual con días faltantes y primeros días de serie.

**Aceptación / pruebas obligatorias.** Fechas sin ventas presentes; no dividir por cero; definir si “7 días” incluye el actual.

**Entrega.** `SQL-016.sql` + diagrama de ventana y prueba de frontera.

**Restricciones y extensiones.** Separar fecha de pedido vs cobro; analizar coste de una serie densa.

## SQL-017 — Retención por cohortes

**Objetivo y trabajo solicitado.** Medir cohorts de primera compra y retención M0–M12 con elegibilidad de observación, activos por período y denominador estable.

**Aceptación / pruebas obligatorias.** Nunca se evalúa un mes futuro; cohortes sin meses observables se distinguen de retención cero; no contar dos veces cliente activo en un mes.

**Entrega.** `SQL-017.sql` + heatmap opcional creado por el estudiante + documento de definiciones.

**Restricciones y extensiones.** Explica survival bias, truncamiento temporal y adquisición versus primera compra.

## SQL-018 — Funnel temporal por sesión

**Objetivo y trabajo solicitado.** Construir funnel page_view -> product_view -> add_to_cart -> checkout_started -> purchase respetando orden temporal y sesiones con eventos duplicados/faltantes.

**Aceptación / pruebas obligatorias.** Conversión por etapa no excede denominador bajo definición secuencial; test de evento purchase antes de checkout.

**Entrega.** `SQL-018.sql` + diagrama y tests sintéticos.

**Restricciones y extensiones.** No asumir que la existencia de eventos en la misma sesión implica secuencia válida.

## SQL-019 — Atribución de campañas

**Objetivo y trabajo solicitado.** Asignar a cada compra una fuente según modelo last-touch no directo dentro de una ventana configurable; comparar con first-touch.

**Aceptación / pruebas obligatorias.** Sesiones sin fuente atribuible tienen categoría explícita; empate temporal determinista; multi-tenant aislado.

**Entrega.** `SQL-019.sql`, reglas de atribución y comparativa.

**Restricciones y extensiones.** No confundir evento purchase sintético con pago confirmado; explica la limitación.

## SQL-020 — Segmentación RFM rigurosa

**Objetivo y trabajo solicitado.** Crear recency/frequency/monetary por cliente y segmentos con cuantiles o cortes documentados; calcular sensibilidad con dos métodos.

**Aceptación / pruebas obligatorias.** Cliente sin compra válido en grupo separado; no usar fecha del sistema si es distinta al ancla del dataset; reproducible.

**Entrega.** `SQL-020.sql` + catálogo de segmentos, metodología.

**Restricciones y extensiones.** Define categorías para empates en cuantiles y períodos de observación.

## SQL-021 — Market basket y pares de productos

**Objetivo y trabajo solicitado.** Analizar coocurrencia de productos distintos en una misma orden y calcular medidas de asociación con soporte mínimo.

**Aceptación / pruebas obligatorias.** Pares simétricos no duplicados; no autopares; productos repetidos dentro de un pedido tratados según política.

**Entrega.** `SQL-021.sql` + cuadro de interpretación y cardinalidades.

**Restricciones y extensiones.** Restringir pares por tenant y evitar O(N²) sin justificarlo.

## SQL-022 — Detección heurística de anomalías de pagos

**Objetivo y trabajo solicitado.** Diseñar consultas para localizar ráfagas de órdenes por cliente, discrepancias con pagos y reembolsos inusuales, sin etiquetar automáticamente como fraude.

**Aceptación / pruebas obligatorias.** Mínimo 3 patrones, falsos positivos explicados, ventana temporal documentada y pruebas con datos controlados.

**Entrega.** `SQL-022.sql` + ficha de señales/limitaciones.

**Restricciones y extensiones.** No elaborar sistema de decisión automatizada sobre personas reales; dataset sintético.

## SQL-023 — Pipeline incremental de daily_sales

**Objetivo y trabajo solicitado.** Diseñar y materializar un proceso que complete `analytics.daily_sales` con partición por tenant/fecha; soportar reejecución y backfill de períodos.

**Aceptación / pruebas obligatorias.** Ejecutar dos veces y comparar conteos/totales; cambiar un pago en una BD efímera y recuperar métricas; no tocar otros tenants.

**Entrega.** `SQL-023.sql` + plan de backfill y documentación de métricas.

**Restricciones y extensiones.** Esta tabla empieza vacía. Cursor NO debe implementarlo; el estudiante elige criterios de ingreso y consistencia.

## SQL-024 — Alertas por desviaciones

**Objetivo y trabajo solicitado.** Detectar días atípicos de ventas/conversión con método estadístico robusto y comparación por día de semana o temporada.

**Aceptación / pruebas obligatorias.** Primero tratar series escasas y variación cero; explicar umbral y falsos positivos; reproducibilidad de ventana.

**Entrega.** `SQL-024.sql` + reporte de umbrales.

**Restricciones y extensiones.** Prohibido presentar anomalías como causas confirmadas.

## SQL-025 — Diagnóstico con EXPLAIN

**Objetivo y trabajo solicitado.** Seleccionar tres consultas propias y justificar plan, estimaciones vs filas reales, nodos caros y efecto de ANALYZE.

**Aceptación / pruebas obligatorias.** Guardar dos planes (antes/después de una mejora propia), medición repetida y metodología de comparación.

**Entrega.** `SQL-025.md` + SQL y planes con hardware/escala.

**Restricciones y extensiones.** No reportar velocidad ficticia. `EXPLAIN ANALYZE` ejecuta consultas, cuidado con UPDATE/DELETE.

## SQL-026 — Tuning e índices en 1 millón de eventos

**Objetivo y trabajo solicitado.** Escalar a `large` (1M eventos total), proponer índices o particiones basados en consultas reales y medir escritura y lectura.

**Aceptación / pruebas obligatorias.** Comparar plan, tiempo y almacenamiento antes/después; mínimo 3 consultas con selectividades distintas.

**Entrega.** `SQL-026.sql` + migración creada por el estudiante + benchmarks.

**Restricciones y extensiones.** Los índices de la migración base son mínimos; no crear índices a ciegas ni medir con caché sin registrarlo.

## SQL-027 — Transacciones y anomalías MVCC

**Objetivo y trabajo solicitado.** En dos sesiones concurrentes reproducir una anomalía de inventario y demostrar mitigación con aislamiento/locks adecuados.

**Aceptación / pruebas obligatorias.** Guion de dos sesiones, estado inicial/final, niveles de aislamiento, tratamiento de deadlock y reintento.

**Entrega.** `SQL-027.md` + scripts de sesión A/B.

**Restricciones y extensiones.** Ejecutar únicamente en base de prueba; no cambiar inventario compartido sin restaurarlo.

## SQL-028 — Sessionization sin identificador

**Objetivo y trabajo solicitado.** Reconstruir sesiones a partir de customer_id y gaps temporales sobre eventos; comparar con session_id proporcionado.

**Aceptación / pruebas obligatorias.** Eventos con mismo timestamp, device distinto y actividad muy espaciada; porcentajes de discrepancia documentados.

**Entrega.** `SQL-028.sql` + discusión de criterios.

**Restricciones y extensiones.** La reconstrucción es una inferencia; no asumir que la session real siempre es perfecta.

## SQL-029 — Particionado de tablas de eventos

**Objetivo y trabajo solicitado.** Diseñar particionado temporal para nueva tabla de eventos de alto volumen y planificar migración sin pérdida de datos.

**Aceptación / pruebas obligatorias.** Demostrar consultas con y sin pruning, constraints/índices compatibles, estrategia de retention y rollback en BD efímera.

**Entrega.** `SQL-029.md` + migración propia y resultados.

**Restricciones y extensiones.** No reemplazar tabla original durante el bootstrap. `CONCURRENTLY` requiere manejo transaccional especial.

## SQL-030 — Materialized views y freshness

**Objetivo y trabajo solicitado.** Diseñar una arquitectura de consulta pesada que elija entre materialized view, tabla incremental y consulta ad-hoc, con freshness y costo de refresh.

**Aceptación / pruebas obligatorias.** SLO definido, estrategia de invalidación, mediciones y posibilidad de recuperación ante fallo de refresh.

**Entrega.** `SQL-030.md` + esquema y PoC del estudiante.

**Restricciones y extensiones.** No se exige que una MV sea siempre la mejor opción; debes justificar descartarla.

## Evaluación

No basta con que el resultado parezca razonable: el estudiante debe justificar semántica, comprobar bordes, declarar supuestos, defender costes y documentar cómo verificó sus resultados. La IA revisará, no sustituirá, la implementación.
