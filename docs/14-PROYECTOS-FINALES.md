# 14 — Proyectos finales de portafolio (sin soluciones)

Cada proyecto debe producir un repositorio/PR independiente, explicación de arquitectura, validación funcional, performance, documentación y demo. No usar datos reales ni despliegue que consuma dinero sin consentimiento.

## Capstone A — Intelligence Hub (Data Analyst Expert)

**Problema:** dirección comercial desea comprender retención, rentabilidad aproximada, salud del funnel y anomalías sin depender de consultas manuales.

**MVP obligatorio:**

1. Data dictionary y contrato de 10 KPI definidos por negocio.
2. Modelo analítico en star schema o alternativa justificada: hechos de ventas, pagos, devoluciones y eventos; dimensiones con claves verificadas.
3. ETL incremental reproducible desde core + events hacia tablas/vistas analíticas, con backfill.
4. Tabla de calidad de datos y cuarentena de importaciones raw.
5. Análisis cohortes de compra, retención, RFM, funnel y segmentos por tenant.
6. Informe de decisión ejecutiva (máx. 4 páginas) con incertidumbre y limitaciones.
7. Pipeline probado con escala `medium`; benchmark `large` opcional.

**Restricciones:** no duplicar revenue por joins, no confundir conversión de sesión con pagos, no mezclar cohorts de adquisición/compra, no usar fechas futuras como retención cero.

**Aceptación:** 10 métricas documentadas; 5+ invariantes probadas; ejecución idempotente; outputs auditables; mínimo dos motores analíticos comparados con mismo resultado; presentación comprensible para persona no técnica.

**Entregables:** `README`, ADR, SQL y Python propios, tests, datasets derivados (no incluir datasets enormes en Git), manifiestos, tablas de benchmark, memo ejecutivo.

## Capstone B — Commerce API (Backend Senior)

**Problema:** un marketplace requiere manejar pedidos concurrentes con cumplimiento de inventario y pagos simulados, sin duplicados ni acceso entre comercios.

**MVP obligatorio:**

1. API v1 versionada con catálogo, clientes (lectura), órdenes, líneas y pago fake.
2. Autenticación y autorización multi-tenant con roles admin/operator/reader.
3. Transacción de creación de orden y reserva de inventario.
4. Idempotency-Key para creación/captura segura ante reintentos concurrentes.
5. Máquina de estados explícita y auditoría.
6. Outbox + worker para evento `order.created` o equivalente.
7. Readiness, métricas, logs estructurados, trazas y errores de contrato.
8. CI e integración contra Postgres efímero.
9. Prueba de carga y dos incident drills documentados.

**Amenazas a demostrar:** IDOR, sobreventa, peticiones repetidas, pérdida de publicación, retrasos y colas saturadas, consulta N+1, leak de secretos.

**Aceptación:** bajo 50 requests simultáneas por stock escaso se conserva el invariante; requests repetidos con key equivalente no duplican órdenes; fallo de worker no pierde outbox pendiente; tenant A nunca accede a B; pruebas integrales y un runbook de recuperación.

**Entregables:** API funcional propia, OpenAPI versionado, migraciones nuevas, tests, Dockerfile, runbooks, load report, ADRs.

## Capstone C — Real-Time Signals (Integrado Analytics + Backend)

**Problema:** el negocio necesita detectar cambios de conversión e ingresos con retraso bajo sin comprometer las órdenes transaccionales.

**MVP obligatorio:**

1. Diseñar ingesta de eventos desde API -> cola -> staging/almacén analítico.
2. Especificar semántica al menos una vez, deduplicación y orden eventual.
3. Construir agregados por ventana de eventos y compararlos con batch diario.
4. Instrumentar lag de ingestión, errores, backlog, freshness y alertas.
5. Registrar datos tardíos, eventos duplicados y out-of-order.
6. Exponer endpoint de consulta de métricas segregado por tenant.
7. Evaluar arquitectura y costo: Redis + Postgres vs broker especializado.

**Aceptación:** replay de eventos no genera dobles conteos, fallo de consumer no pierde eventos, backfill posterior reconcilia con batch, latencia/throughput se miden con escenarios reproducibles.

**Entregables:** diagrama, contratos de eventos, pruebas de fallo, scripts de replay, evidencia de reconciliación, ADR de tecnologías y memo de tradeoffs.

## Formato de presentación final

- 10 minutos: contexto, alcance y decisiones.
- 10 minutos: demo real (incluye camino de fallo).
- 10 minutos: auditoría de pruebas y métricas.
- 10 minutos: preguntas críticas (consistencia, seguridad, coste, escalado).

## Exclusiones

No crear automáticamente los capstones terminados, dashboards con resultados precalculados, API de pagos reales o implementaciones que invadan los labs. Copilot solo prepara la estructura y guía la revisión progresiva.
