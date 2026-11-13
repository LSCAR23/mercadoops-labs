-- SQL-001 — Exploración controlada y filtros
--
-- Objetivo:
-- Construye consultas de exploración para órdenes de un tenant determinado,
-- un rango UTC, estados y moneda; devuelve columnas mínimas, una paginación
-- estable y orden explícito.
--
-- Aceptación / pruebas obligatorias:
-- - Probar tenant existente e inexistente.
-- - Probar rango vacío, rango de un día y timestamp en frontera.
-- - Probar página repetida y parámetros SQL.
-- - No usar SELECT * en el resultado final.
--
-- Entrega:
-- Este archivo debe contener tu consulta, junto con una explicación del rango
-- semiabierto y el plan de ejecución.
--
-- Restricciones:
-- No concatenar el tenant_id ni la fecha. Define claramente los límites
-- inclusivos y exclusivos.
--
-- TODO(student): implementa aquí tu solución.


--Answer:
SELECT
    o.tenant_id,
    o.id,
    o.ordered_at,
    o.order_status,
    o.currency
FROM core.orders as o
WHERE o.tenant_id = :tenant_id
  AND (:start_date IS NULL OR o.ordered_at >= :start_date)
  AND (:end_date IS NULL OR o.ordered_at < :end_date)
  AND (:ordered_status IS NULL OR o.order_status = :ordered_status)
  AND (:currency IS NULL OR o.currency = :currency)
ORDER BY o.ordered_at ASC, o.id ASC
LIMIT :limit OFFSET :offset;

-- en esta consulta se usa un rango semiabierto: el límite inferior es inclusivo
-- y el superior es exclusivo. Así, una fecha de fin de día en UTC se representa
-- como el inicio del día siguiente y evita incluir timestamps del día siguiente.
--
-- Plan de ejecución:
-- 1. Filtrar por tenant_id y el rango de ordered_at.
-- 2. Ordenar por ordered_at y id para obtener un orden estable.
-- 3. Aplicar LIMIT/OFFSET para paginar los resultados.
-- 4. Un índice compuesto sobre (tenant_id, ordered_at, id) permite recorrer el
--    rango en orden y limita el número de filas que deben ordenarse.


--------------------------------------
--SOLUCION CORRECTA
--------------------------------------
SELECT
    o.tenant_id,
    o.id,
    o.ordered_at,
    o.order_status,
    o.currency
FROM core.orders AS o
WHERE o.tenant_id = :tenant_id
  AND o.ordered_at >= :start_utc
  AND o.ordered_at < :end_utc
  AND o.order_status = :order_status
  AND o.currency = :currency
ORDER BY o.ordered_at ASC, o.id ASC
LIMIT :limit
OFFSET :offset;