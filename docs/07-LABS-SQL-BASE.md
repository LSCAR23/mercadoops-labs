# 07 — SQL esencial e intermedio

Secuencia SQL-001 a SQL-014. Prerrequisitos: migraciones y seed `tiny`. Para todos los reportes: define unidad temporal, estados válidos, dimensión tenant y forma de validación. La semilla no establece de forma implícita tus definiciones de negocio.

**Contrato general:** Copilot debe mostrar únicamente este enunciado, crear stubs bajo `workspaces/sql/` cuando el estudiante active el laboratorio y dejar la implementación pendiente. **No incluir soluciones, SQL de respuesta, algoritmos funcionales ni resultados precalculados.**

## SQL-001 — Exploración controlada y filtros

**Objetivo y trabajo solicitado.** Construye consultas de exploración para órdenes de un tenant determinado, un rango UTC, estados y moneda; devuelve columnas mínimas, una paginación estable y orden explícito.

**Aceptación / pruebas obligatorias.** Probar tenant existente/inexistente, rango vacío, rango de un día, timestamp en frontera, página repetida y parámetros SQL; sin `SELECT *` en resultado final.

**Entrega.** `workspaces/sql/SQL-001.sql` + explicación de rango semiabierto y plan de ejecución.

**Restricciones y extensiones.** No concatenar el `tenant_id` o la fecha; define claramente límites inclusivos/exclusivos.

## SQL-002 — Ventas mensuales y calendario

**Objetivo y trabajo solicitado.** Obtener una serie mensual de pedidos e importes por tenant para los 24 meses del dataset, incluyendo períodos sin actividad y cortes por `order_status`.

**Aceptación / pruebas obligatorias.** 24 meses por tenant en un reporte de ventana fija; meses sin pedidos visibles; totales consistentes al cambiar granularidad.

**Entrega.** `SQL-002.sql`, tabla de definiciones de métricas, tres pruebas.

**Restricciones y extensiones.** No infieras ingreso realizado solo porque un pedido exista; deja explícita la elección de estados.

## SQL-003 — Ranking de productos

**Objetivo y trabajo solicitado.** Construir ranking por unidades e importe de líneas, desglosado por tenant y categoría, conservando productos sin ventas.

**Aceptación / pruebas obligatorias.** Un mismo producto no debe duplicar sus ventas al agregar otras tablas; empates de orden deterministas.

**Entrega.** `SQL-003.sql`, justificación de JOIN y conteos.

**Restricciones y extensiones.** No usar precio actual para valorar ventas pasadas; considerar descuentos.

## SQL-004 — Adquisición de clientes

**Objetivo y trabajo solicitado.** Calcular altas mensuales por `acquisition_channel` y país; distinguir registro de primera compra.

**Aceptación / pruebas obligatorias.** Clientes sin pedidos sí aparecen en altas; fechas UTC y canales válidos; suma por canal igual al total general del mes.

**Entrega.** `SQL-004.sql` + glosario de indicadores.

**Restricciones y extensiones.** Explica las consecuencias de dos definiciones diferentes de “nuevo cliente”.

## SQL-005 — Anti-join para clientes sin compras

**Objetivo y trabajo solicitado.** Identificar clientes que nunca han comprado y otros que solo tienen pedidos cancelados; segmentar por tenant.

**Aceptación / pruebas obligatorias.** Diferenciar no tener órdenes y tener solo canceladas; no cruzar tenants; comprobar una fixture creada manualmente.

**Entrega.** `SQL-005.sql` + casos de prueba.

**Restricciones y extensiones.** No confundir NULL de un LEFT JOIN con valor nulo en una columna de negocio.

## SQL-006 — Cardinalidad y fan-out

**Objetivo y trabajo solicitado.** Comparar el cálculo de pagos por orden al unir órdenes, líneas y pagos; diseñar una consulta que evite multiplicación de montos.

**Aceptación / pruebas obligatorias.** En órdenes con 3 ítems, total de pagos no debe triplicarse; prueba con un pago y con dos pagos.

**Entrega.** `SQL-006.sql` + explicación del riesgo.

**Restricciones y extensiones.** Se valora el razonamiento sobre cardinalidad más que el número final.

## SQL-007 — Descuentos y margen aproximado

**Objetivo y trabajo solicitado.** Calcular descuento por ítem, pedido y categoría y una aproximación de margen bruto con limitaciones documentadas.

**Aceptación / pruebas obligatorias.** Nunca resultan descuentos negativos con core válido; totales por ítem y total por pedido reconcilian; costo actual se rotula como aproximación.

**Entrega.** `SQL-007.sql` + definiciones y advertencias.

**Restricciones y extensiones.** Evitar operaciones con `float`; conservar precisión NUMERIC.

## SQL-008 — Conciliación pedido-pago

**Objetivo y trabajo solicitado.** Marcar órdenes cuya suma de líneas netas no coincide con pagos capturados, y diferenciar casos pendientes, fallidos y cancelados.

**Aceptación / pruebas obligatorias.** Casos: sin pago, múltiples pagos, pago parcial, diferencia de centavos, pedido cancelado; ninguna división por cero.

**Entrega.** `SQL-008.sql` + criterios de tolerancia.

**Restricciones y extensiones.** Documentar si concilias por estado y si un pago autorizado cuenta como cobrado.

## SQL-009 — Reembolsos y fechas

**Objetivo y trabajo solicitado.** Informar importes reembolsados por semana, estado y método de pago; reconocer posibles reembolsos parciales.

**Aceptación / pruebas obligatorias.** Un reembolso vinculado a pago se cuenta una vez; distinguir refund solicitado vs completado; fechas nulas tratadas.

**Entrega.** `SQL-009.sql` + tabla de reglas de negocio.

**Restricciones y extensiones.** No sumar montos de reembolsos al unir con líneas de pedido sin prevenir fan-out.

## SQL-010 — SLAs de envíos

**Objetivo y trabajo solicitado.** Calcular tiempo de despacho y entrega desde el pedido, percentiles y porcentaje que cumple un SLA definido por el estudiante.

**Aceptación / pruebas obligatorias.** Órdenes sin shipment, con envío creado y con timestamps incompletos no causan intervalos falsos; UTC consistente.

**Entrega.** `SQL-010.sql` + SLA asumido y 4 edge cases.

**Restricciones y extensiones.** Percentiles requieren población claramente especificada.

## SQL-011 — Segmentos país/canal/tenant

**Objetivo y trabajo solicitado.** Construir reporte multidimensional de compradores, pedidos y montos por país, canal y tenant, con filtros y un total general coherente.

**Aceptación / pruebas obligatorias.** Clientes con cero pedidos no inflan compras; un comprador puede tener N pedidos pero cuenta una sola vez por grupo.

**Entrega.** `SQL-011.sql` + comprobación de totales.

**Restricciones y extensiones.** No confundir conteo de filas con conteo de entidades.

## SQL-012 — JSONB de staging

**Objetivo y trabajo solicitado.** Explorar `analytics.raw_orders`: tipos de campos, ausencias, formatos inesperados y variabilidad de fuentes sin modificar registros.

**Aceptación / pruebas obligatorias.** No debe fallar al leer montos no numéricos; dar conteos por clase de defecto con definiciones propias.

**Entrega.** `SQL-012.sql` + perfil de atributos.

**Restricciones y extensiones.** Prohibido aplicar cast indiscriminado que lance error en los registros defectuosos.

## SQL-013 — HAVING y umbrales

**Objetivo y trabajo solicitado.** Definir una lista de clientes de alto valor y frecuencia configurable; diferenciar filtro pre-agregación y post-agregación.

**Aceptación / pruebas obligatorias.** Inclusión de fronteras de umbral comprobada; no contar pedidos cancelados si la definición los excluye.

**Entrega.** `SQL-013.sql` + parámetros del negocio.

**Restricciones y extensiones.** El resultado debe ser reproducible con otro umbral sin editar texto SQL inseguramente.

## SQL-014 — Reportes de resumen

**Objetivo y trabajo solicitado.** Construir resumen jerárquico tenant > canal > mes con subtotales identificables sin confundir NULL legítimos con filas de subtotal.

**Aceptación / pruebas obligatorias.** Subtotales reconciliados con detalle; etiqueta explícita del nivel; tenant isolation preservado.

**Entrega.** `SQL-014.sql` + nota de interpretabilidad.

**Restricciones y extensiones.** Justifica estrategia elegida entre GROUPING SETS, ROLLUP u otra.

## Evaluación

No basta con que el resultado parezca razonable: el estudiante debe justificar semántica, comprobar bordes, declarar supuestos, defender costes y documentar cómo verificó sus resultados. La IA revisará, no sustituirá, la implementación.
