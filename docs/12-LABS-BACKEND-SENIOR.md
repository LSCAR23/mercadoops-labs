# 12 — Backend developer senior: sistemas resilientes

BE-013 a BE-026. Aquí se espera razonar sobre semántica de fallos, simultaneidad, seguridad y arquitectura. Usa solo pasarelas de pago falsas y datos sintéticos.

**Contrato general:** el agente de Cursor debe mostrar únicamente este enunciado, crear stubs bajo `workspaces/backend/` cuando el estudiante lo pida y dejar la implementación pendiente. **No incluir soluciones, SQL de respuesta, algoritmos funcionales ni resultados precalculados.**

## BE-013 — Autenticación y autorización multi-tenant

**Objetivo y trabajo solicitado.** Diseñar identidad (JWT o sesiones), mapping de roles y políticas sobre resources; elegir mecanismo y defenderlo.

**Aceptación / pruebas obligatorias.** Usuario de tenant A no accede a B aun con UUID válido; token vencido/revocado; permisos lectura/escritura; bypass de ruta anidada.

**Entrega.** ADR seguridad, middleware/dependencies y suite aislamiento.

**Restricciones y extensiones.** Usar secreto seguro local, expiraciones, validaciones de emisor/audiencia si JWT.

## BE-014 — Reserva de inventario concurrente

**Objetivo y trabajo solicitado.** Implementar reserva atómica de stock ante 20 compras simultáneas sobre último producto disponible; definir política de sobreventa.

**Aceptación / pruebas obligatorias.** Stock nunca negativo; a lo sumo compras autorizadas; rollback libera reserva; pruebas de carrera real con transacciones.

**Entrega.** Servicio, suite concurrencia y diagrama de locking.

**Restricciones y extensiones.** Comparar SELECT FOR UPDATE, UPDATE condicional y optimista; no aceptar check-then-update fuera de transacción.

## BE-015 — Idempotency-Key real

**Objetivo y trabajo solicitado.** Procesar POST/orders idempotentemente ante retries y duplicación concurrente, usando tabla ops.

**Aceptación / pruebas obligatorias.** Misma key+payload devuelve misma respuesta; misma key+otro payload conflicto; requests simultáneos; expiración; crash antes/después de commit.

**Entrega.** Contrato HTTP, implementación y pruebas de carrera.

**Restricciones y extensiones.** No hacer una búsqueda previa insegura sin restricción única; documentar recovery.

## BE-016 — Transactional outbox

**Objetivo y trabajo solicitado.** Guardar orden y evento outbox en una sola transacción, y despachar evento en worker separado con reintentos.

**Aceptación / pruebas obligatorias.** Crash entre commit/publicación; redelivery; idempotencia del consumidor; retries con backoff; no perder evento.

**Entrega.** Worker, ADR, observabilidad y tests de fallos.

**Restricciones y extensiones.** El patrón es al menos una vez: no prometer exactamente una vez sin evidencia.

## BE-017 — Workers asíncronos y colas

**Objetivo y trabajo solicitado.** Procesar trabajo pesado (reportes, notificaciones fake) vía Redis y cola, con timeout, retry, DLQ y límites.

**Aceptación / pruebas obligatorias.** Trabajo fallido/atascado, reintento, reinicio de worker, tarea cancelada, backpressure.

**Entrega.** Implementación propia + runbook.

**Restricciones y extensiones.** No procesar trabajos largos en request web; no enviar notificaciones reales.

## BE-018 — Caché y consistencia

**Objetivo y trabajo solicitado.** Añadir cache para lectura de catálogo o reporte con invalidación definida, tenant-safe y medición de hit rate.

**Aceptación / pruebas obligatorias.** Cambiar precio invalida resultado, dos tenants con misma query separados; TTL; fallo Redis con fallback seguro.

**Entrega.** ADRs + tests consistencia + mediciones.

**Restricciones y extensiones.** No usar caché para mantener consistencia de stock sin mecanismo transaccional.

## BE-019 — Resiliencia y timeouts

**Objetivo y trabajo solicitado.** Introducir deadlines, retries con jitter y circuito para proveedor externo FAKE.

**Aceptación / pruebas obligatorias.** Cascada de fallos, proveedor lento, reintentos no seguros en POST, límites de concurrencia.

**Entrega.** Adapter simulado, políticas y pruebas.

**Restricciones y extensiones.** No reintentar operaciones no idempotentes sin control de duplicados.

## BE-020 — Sagas / compensaciones

**Objetivo y trabajo solicitado.** Modelar compra de varios pasos (reservar, cobrar fake, enviar) y definir compensación ante error parcial.

**Aceptación / pruebas obligatorias.** Fallo en paso 2/3, duplicación, fallos de compensación, recuperación tras reinicio.

**Entrega.** Diagrama de estados, implementación incremental y tests.

**Restricciones y extensiones.** Distingue transacción DB de saga distribuida; no llamar rollback SQL a sistemas externos.

## BE-021 — Auditoría tamper-evident

**Objetivo y trabajo solicitado.** Registrar acciones de modificación en ops.audit_logs con actor, entidad, tenant y metadata redactada; diseñar control de integridad.

**Aceptación / pruebas obligatorias.** No almacenar secretos, múltiples actores, acciones concurrentes, logs no omitidos en fallo, conservación explicada.

**Entrega.** Implementación, test y política de retención.

**Restricciones y extensiones.** No afirmar inmutabilidad absoluta solo por guardar filas en base.

## BE-022 — Rate limits, abuso y seguridad

**Objetivo y trabajo solicitado.** Limitar peticiones por identidad/tenant y aplicar validación de inputs, tamaño máximo, CORS y headers apropiados.

**Aceptación / pruebas obligatorias.** Burst, concurrency, reset de ventana, clientes legítimos, error 429 y bypass cross-tenant.

**Entrega.** Política de seguridad y suite bajo carga.

**Restricciones y extensiones.** No poner secretos en URLs ni habilitar CORS wildcard con credenciales.

## BE-023 — Migración sin downtime

**Objetivo y trabajo solicitado.** Planificar cambio no trivial al schema de payments con despliegue compatible hacia atrás y datos históricos.

**Aceptación / pruebas obligatorias.** Versiones app vieja/nueva coexisten, backfill seguro e idempotente, rollback de despliegue.

**Entrega.** ADRs, migraciones nuevas y runbook.

**Restricciones y extensiones.** Preferir expand/contract, no DROP directo de columna en uso.

## BE-024 — Performance bajo carga

**Objetivo y trabajo solicitado.** Evaluar p95, throughput y errores de GET/POST con concurrencia controlada, pool conexiones y consultas N+1.

**Aceptación / pruebas obligatorias.** Comparar tiny/medium, 10/50/100 clientes, p50/p95/p99, error rate y recurso limitante.

**Entrega.** Scripts Locust/k6 opcionales, reportes medidos y mejoras.

**Restricciones y extensiones.** No publicar un número inventado ni confundir máquina local con producción.

## BE-025 — Alta disponibilidad y degradación

**Objetivo y trabajo solicitado.** Definir dependencias críticas/no críticas, readiness/liveness y manejo de caídas de Redis/DB sin ocultar fallos.

**Aceptación / pruebas obligatorias.** Redis down, DB down, tiempo de recuperación, health/status apropiado; evitar retry storm.

**Entrega.** ADR + simulación de incidentes + resultados.

**Restricciones y extensiones.** No hacer restart infinito si falta un secreto o la configuración es inválida.

## BE-026 — Revisión arquitectónica senior

**Objetivo y trabajo solicitado.** Auditar el sistema completo: threat model, integridad, CQRS justificado o descartado, ADRs, ownership de datos y runbooks.

**Aceptación / pruebas obligatorias.** Entregar mínimo 8 riesgos priorizados con mitigación y evidencia, estimación de costos y plan de deudas técnicas.

**Entrega.** Informe senior y refactors elegidos por el estudiante.

**Restricciones y extensiones.** No introducir microservicios sin una necesidad observada.

## Evaluación

No basta con que el resultado parezca razonable: el estudiante debe justificar semántica, comprobar bordes, declarar supuestos, defender costes y documentar cómo verificó sus resultados. La IA revisará, no sustituirá, la implementación.
