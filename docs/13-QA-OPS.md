# 13 — Calidad, CI/CD, DevOps y observabilidad

El ingeniero senior demuestra cómo valida, despliega, opera y recupera un sistema, no solo cómo escribe endpoints. **Estos son ejercicios; no implementarlos automáticamente en el bootstrap.** La base incluye solo `tests/test_bootstrap.py` y un workflow CI mínimo para comprobar salud estructural.

## QA-001 — Pirámide de pruebas realista

Diseña suites unitarias (funciones puras), integración (Postgres real desechable), contrato (OpenAPI), E2E (flujo de órdenes) y concurrencia (inventario). Definir fixtures, tiempos máximos por suite y qué se permite simular. **Aceptar:** tests deterministas, cada nivel ejecutable por separado, fallo intencional detectado.

## QA-002 — Testcontainers o Docker dedicado

Configura ejecución sobre Postgres efímero, alejado del dataset de prácticas. **Aceptar:** inicializa schema por Alembic, crea datos aislados, borra contenedor al terminar, no exige puertos fijos y falla claramente si Docker no está disponible.

## QA-003 — Property-based testing

Escoge validaciones monetarias, transiciones de estados o idempotencia; expresa invariantes y verifica combinaciones generativas. **Aceptar:** ejemplo contrafactual reproducible, shrunk failing case, estrategia sin números flotantes para dinero.

## QA-004 — Mutation testing

Evalúa si las pruebas detectan bugs intencionales como comparación `>=` por `>`, filtro tenant omitido, commit antes de completar ítems. **Aceptar:** documenta mutantes sobrevivientes y plan de mejoras. No ocultar mutantes con tests hardcodeados.

## QA-005 — CI con múltiples gates

Extiende `.github/workflows/ci.yml` para lint, mypy, tests unitarios, integración, migraciones, seguridad de dependencias y publicación de reportes. **Aceptar:** fallo en un gate impide merge y ejecuta al menos una migración real en base descartable.

## QA-006 — CD local/staging controlado

Crear Dockerfile multi-stage, usuario no root, imagen sin archivos secretos, healthchecks y estrategia deploy/rollback. **Aceptar:** build reproducible, variables por entorno, estrategia para migraciones antes/después de despliegue y rollback de app sin pérdida de datos.

## QA-007 — Métricas RED/USE y SLO

Instrumentar request rate, errors, duration, saturación de pool, queue lag y fallos de jobs. **Aceptar:** dashboard o export de métricas, umbrales y alertas de ejemplo, cardinalidad controlada; no etiquetar emails ni IDs de clientes como dimensiones de métricas.

## QA-008 — Logs y trazas correlacionables

Diseñar estructura JSON con request_id, trace_id, tenant lógico y estado; propagar a servicios internos y workers. **Aceptar:** seguir una solicitud con error desde HTTP a SQL/outbox con correlación; redactar secretos/PII.

## QA-009 — Chaos engineering local

Simular caída del contenedor Redis, desconexión de BD, latencia, error parcial de pagos fake y worker duplicado. **Aceptar:** matriz de escenarios, resultado observado, semántica retry y garantía de consistencia que se preserva.

## QA-010 — Backups y recuperación

Diseñar backup PostgreSQL y restore en una base **diferente**. **Aceptar:** RPO/RTO objetivos, comprobación de conteos/constraints y documentación de pasos. Restaurar el mismo volumen sin copia validada no es una prueba segura.

## QA-011 — Threat modeling

Identificar activos, fronteras de confianza, STRIDE básico, casos de IDOR/BOLA, secretos, inyección SQL, replay e información sensible en logs. **Aceptar:** matriz de riesgos con severidad, probabilidad, mitigación, test correspondiente y responsable.

## QA-012 — Revisión de coste y capacidad

Estimar storage de 2M eventos, crecimiento mensual, índices, backup, CPU, pool y latencia; comparar mediciones con hipótesis y calcular margen de seguridad. **Aceptar:** supuestos verificables, intervalos, recomendaciones y plan para escalar verticalmente antes de introducir sistemas nuevos.

## Umbral de aprobación senior

No se aprueba si el único criterio es “funciona localmente”. El estudiante debe entregar casos de error, pruebas de múltiples tenants, evidencia de carga, tradeoffs, runbooks y planes de recuperación. Copilot puede crear stubs de las pruebas y pipelines **solo tras activar el lab** y nunca escribir una referencia que resuelva la lógica de negocio.
