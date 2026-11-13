# 18 — Calidad, seguridad y reglas para producción simulada

## Datos y privacidad

- Correos sintéticos `.example` y nombres ficticios; nunca datos reales de clientes.
- El `.env` se ignora en Git, los secretos nunca se imprimen, no se guardan contraseñas en logs.
- Datos de entrada de usuarios pasan por validación de Pydantic/servicio y SQL con parámetros.
- Para demos y portafolio usa solo datos generados y capturas sin secretos.

## Reglas multi-tenant

1. Toda consulta/actualización se filtra por tenant de **contexto autenticado**, no por un campo arbitrario de petición.
2. Para referencias cliente/producto/pedido se valida relación por tenant. Las FKs compuestas del esquema son última barrera, no sustituyen autorización.
3. Los IDs UUID no son autorización; no devolver status, monto, email o existencia de otra empresa de forma inadvertida.
4. Caché, colas, idempotencia, eventos y métricas requieren dimensión tenant cuando proceda.

## Integridad financiera y concurrencia

- Dinero en NUMERIC/Decimal y USD en dataset. Para moneda adicional requerir contrato explícito de FX y redondeo.
- No confiar en monto calculado por frontend; el servidor construye totales a partir del estado autorizado.
- Stock no puede quedar negativo; es necesario sincronizar escrituras con transacciones o técnica equivalente.
- Captura y reembolso no deben exceder montos autorizados, contabilizando operaciones previas.
- Reintentos de mutaciones deben tener política de idempotencia y semántica de error estable.
- Test de simultaneidad ejecutado contra DB real, no solo mock.

## Seguridad HTTP

- Autenticación de usuario/servicio con expiración, protección frente a replay y rotación cuando corresponda.
- Autorización en todas las rutas (incluyendo reportes y exportaciones), RBAC o ABAC justificado.
- Límites de tamaño, límites de tasa, validación de tipo contenido, CSP/CORS según entorno.
- Timeouts en DB/HTTP/cola; evitar reintentos ilimitados.
- No registrar request bodies sensibles en logging automático.
- Selección de estado HTTP coherente: 422 input inválido, 409 conflicto de negocio, 403 prohibido, etc.

## Seguridad de SQL y migraciones

- Nunca interpolar IDs/inputs en strings SQL sin binding.
- Consultas SQL y test de performance sobre dataset de prueba.
- Índices no se construyen “a ojo”; priorizar evidencia de SELECT real y coste de escritura.
- Migration reviews: DDL transaccional, rollback probado, backfills por lotes, plan de bloqueo y disponibilidad.
- Scripts de borrado solo en DB descartable confirmada y con backup válido.

## Antipatrón que Copilot debe detectar

`except: pass`; `except Exception: return []`; uso de float como dinero; `.all()` sobre millones sin paginación; llamadas a servicios dentro de transacción abierta; locks sin timeout; operaciones de stock read-modify-write sin exclusión; secretos hardcodeados; filtrado por tenant solo en frontend; N+1 queries; `SELECT *` sin contrato; tests que necesitan ejecutarse en orden; afirmaciones sin métricas.

## Política de evidencia

Para declarar “correcto” una función o consulta se requiere evidencia de caso normal, límite y fallo. Para declarar “más rápido” se requiere dataset, hardware, procedimiento, número de repeticiones y métricas registradas. Para declarar “seguro” se requiere threat model y tests negativos; no se debe confundir seguridad supuesta con verificada.
