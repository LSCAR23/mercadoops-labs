# 11 — Backend Python: bases sólidas

BE-001 a BE-012. Se implementan **después** de los laboratorios SQL/Python de base. Escribir código únicamente cuando el estudiante inicia ese ejercicio; el bootstrap conserva solo health checks.

**Contrato general:** Copilot debe mostrar únicamente este enunciado, crear stubs bajo `workspaces/backend/` cuando el estudiante active el laboratorio y dejar la implementación pendiente. **No incluir soluciones, SQL de respuesta, algoritmos funcionales ni resultados precalculados.**

## BE-001 — Diseño de capas y dependencias

**Objetivo y trabajo solicitado.** Definir arquitectura módulos FastAPI: routes, schemas, services, repositories y transacciones; separar dominio de HTTP.

**Aceptación / pruebas obligatorias.** Diagrama de dependencias sin ciclos, tests por capa y ausencia de acceso DB desde lógica pura.

**Entrega.** ADR + estructura de módulos que crea el estudiante.

**Restricciones y extensiones.** No modificar rutas de health salvo compatibilidad; evitar abstracción especulativa.

## BE-002 — GET catálogo paginado

**Objetivo y trabajo solicitado.** Implementar endpoint de productos por tenant con filtros, orden estable y keyset pagination; esquema de errores claro.

**Aceptación / pruebas obligatorias.** Tenant inexistente, usuario sin permiso, next cursor inválido, 0 productos, sorting consistente, no leakage.

**Entrega.** Endpoint, OpenAPI y tests con base efímera.

**Restricciones y extensiones.** No confiar en tenant_id suministrado sin autorización; limitar page_size.

## BE-003 — POST productos con validación

**Objetivo y trabajo solicitado.** Implementar alta de producto con SKU único por tenant, validación de precios/moneda y error de conflicto.

**Aceptación / pruebas obligatorias.** Precio inválido, categoría de otro tenant, SKU duplicado, rollback ante fallo; 201 y 409 coherentes.

**Entrega.** Endpoint y tests de integración.

**Restricciones y extensiones.** No capturar todas las excepciones como 500 sin diagnóstico.

## BE-004 — GET órdenes y detalle

**Objetivo y trabajo solicitado.** Diseñar listado y detalle con ítems/pagos bajo tenant y permisos; evitar N+1 y leaks de datos.

**Aceptación / pruebas obligatorias.** Múltiples líneas, orden inexistente, acceso cross-tenant, paginación, nombre en respuesta.

**Entrega.** Esquemas Pydantic, rutas y tests.

**Restricciones y extensiones.** Medir consulta para detectar N+1; no exponer datos sensibles innecesarios.

## BE-005 — POST órdenes atómico

**Objetivo y trabajo solicitado.** Crear orden más líneas en una sola transacción, validando productos y descuentos y retornando un recurso consistente.

**Aceptación / pruebas obligatorias.** Fallo del ítem N revierte todos los cambios; producto inactivo; cero ítems; otro tenant; totals precisos.

**Entrega.** Servicio, endpoint, test rollback.

**Restricciones y extensiones.** No implementar reserva de stock aún; se introduce en BE-014.

## BE-006 — PATCH estados y máquina finita

**Objetivo y trabajo solicitado.** Diseñar transición explícita de estados de orden y rechazar transiciones inválidas con respuesta contractual.

**Aceptación / pruebas obligatorias.** Estados terminales, secuencias válidas, idempotencia de repetición documentada, auditoría futura.

**Entrega.** Tabla de transiciones, código y tests.

**Restricciones y extensiones.** No aceptar `order_status` arbitrario sin reglas de negocio.

## BE-007 — Filtros avanzados y performance

**Objetivo y trabajo solicitado.** Exponer filtros por fechas, status y customer_id evitando N+1, índices insuficientes y SQL no parametrizado.

**Aceptación / pruebas obligatorias.** Pruebas de tamaño página y límites UTC, error de filtro, EXPLAIN antes/después.

**Entrega.** API + reporte de plan.

**Restricciones y extensiones.** No usar offset alto sin explicar el coste.

## BE-008 — Contratos de errores

**Objetivo y trabajo solicitado.** Homogeneizar errores con código estable, request id, status HTTP y validación de inputs; sin exponer tracebacks.

**Aceptación / pruebas obligatorias.** 400/401/403/404/409/422/500, secreto omitido, request id correlacionable, mensajes accionables.

**Entrega.** Middleware o handler propio + tests.

**Restricciones y extensiones.** Nunca devolver excepción cruda de PostgreSQL al cliente.

## BE-009 — Estrategia de tests y fixtures

**Objetivo y trabajo solicitado.** Construir fixtures aisladas por tenant y transacción, factories y pruebas de endpoint semánticas.

**Aceptación / pruebas obligatorias.** Ejecutar suites en cualquier orden; no dependen del seed compartido; fixture limpieza confiable.

**Entrega.** pytest fixtures propias y pipeline básico.

**Restricciones y extensiones.** No reutilizar credenciales de producción; tests con DB descartable.

## BE-010 — Observabilidad HTTP

**Objetivo y trabajo solicitado.** Introducir logs estructurados, correlation ID y métricas de latencia/error de manera segura.

**Aceptación / pruebas obligatorias.** Request ID por respuesta, logs redaccionados, no PII, medición histograma y error ratio.

**Entrega.** Implementación propia + ejemplo de trazas locales.

**Restricciones y extensiones.** No publicar tokens ni customer emails en logs.

## BE-011 — Versionado de contratos

**Objetivo y trabajo solicitado.** Introducir versionado `/api/v1`, política de compatibilidad y schema OpenAPI exportable.

**Aceptación / pruebas obligatorias.** Contratos v1 estables, cambios breaking identificados, deprecation documentada.

**Entrega.** ADR + OpenAPI + tests contractuales.

**Restricciones y extensiones.** No agregar v2 solo por decoración; justificar un cambio de contrato.

## BE-012 — Procesado de pagos simulado

**Objetivo y trabajo solicitado.** Crear flujo de captura de pago FAKE con adapter, validar montos y estados sin integrar proveedores reales.

**Aceptación / pruebas obligatorias.** Captura duplicada, fallo simulado, estado inesperado, retry, pago sobre pedido ajeno.

**Entrega.** Interfaz/adapter fake, servicio, endpoints y tests.

**Restricciones y extensiones.** No almacenar PAN, CVV ni integrar dinero real en laboratorios.

## Evaluación

No basta con que el resultado parezca razonable: el estudiante debe justificar semántica, comprobar bordes, declarar supuestos, defender costes y documentar cómo verificó sus resultados. La IA revisará, no sustituirá, la implementación.
