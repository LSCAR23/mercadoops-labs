# 17 — Contratos API objetivo (especificación, NO implementación)

La única API implementada en el starter es `GET /health/live` y `GET /health/ready`. **Todo lo siguiente es el diseño de contratos para los labs BE y capstones, no código ni respuestas.** Los endpoints se agregan conforme el estudiante los resuelva.

## Convenciones HTTP

- Base URI: `/api/v1`.
- JSON UTF-8; timestamps ISO 8601 con offset explícito (preferiblemente `Z`).
- Montos como **strings decimales** (por ejemplo, `"49.90"`) en requests/responses, nunca double JSON cuando se requiere exactitud.
- Identificadores UUID; paginación por `limit` y cursor opaco; evitar offset alto.
- Correlation ID en header `X-Request-ID`; el servidor debe generarlo si no se proporciona y validarlo.
- Autenticación/identidad del tenant se implementa en BE-013; no confiar solo en un header `X-Tenant-ID` público.
- Encabezado `Idempotency-Key` en POST críticos cuando se implemente BE-015.

## Rutas objetivo y dueño del laboratorio

| Método / ruta | Lab | Entrada | Salida de éxito | Errores a contemplar |
|---|---|---|---|---|
| `GET /api/v1/products` | BE-002 | filtros, cursor, limit | `items`, `next_cursor` | 400, 401, 403 |
| `POST /api/v1/products` | BE-003 | SKU, categoría, precio, costo | producto creado | 400, 401, 403, 409, 422 |
| `GET /api/v1/orders` | BE-004 | filtros, cursor | lista paginada | 400, 401, 403 |
| `GET /api/v1/orders/{order_id}` | BE-004 | UUID | pedido, líneas, pagos autorizados | 401, 403, 404 |
| `POST /api/v1/orders` | BE-005, BE-014, BE-015 | cliente, líneas, descuentos, idempotencia | orden nueva | 401, 403, 409, 422 |
| `PATCH /api/v1/orders/{order_id}/status` | BE-006 | `target_status` | estado actualizado | 401, 403, 404, 409 |
| `POST /api/v1/payments/{payment_id}/capture` | BE-012 | capture fake | pago actualizado | 401, 403, 404, 409 |
| `GET /api/v1/reports/daily-sales` | Capstone | fecha inicial/final | agregados por tenant | 400, 401, 403 |

## Modelo ejemplo de request (especificación de entrada)

```json
{
  "customer_id": "11111111-1111-4111-8111-111111111111",
  "items": [
    {
      "product_id": "22222222-2222-4222-8222-222222222222",
      "quantity": 2,
      "discount_amount": "0.00"
    }
  ]
}
```

Los UUID del ejemplo no son necesariamente registros existentes. **El estudiante debe decidir/implementar** cómo obtener el precio en BD, cuáles estados iniciales corresponden, si se reserva stock y cómo garantiza idempotencia.

## Formato objetivo de error (contrato a implementar en BE-008)

```json
{
  "error": {
    "code": "RESOURCE_CONFLICT",
    "message": "The requested operation conflicts with the current state",
    "request_id": "example-request-id",
    "details": []
  }
}
```

Las descripciones de error **no** deben incluir SQL, credenciales, stack traces ni información de otros tenants.

## Semántica que debe documentarse antes de escribir lógica

- Qué significa un producto activo y qué hacer con stock insuficiente.
- Qué ocurre si dos clientes compran la última unidad a la vez.
- Qué sucede si una petición se repite con la misma key pero diferente payload.
- Cuándo un pago fake se captura y cuándo puede reembolsarse.
- Qué estados permiten rollback y qué operaciones requieren compensación.
- Cómo se distinguen 401/403/404 cuando evitar enumeración de recursos importa.
- Política de versionado, deprecación y compatibilidad.

## Suite contractual de seguridad (solo casos, no implementación)

Usuario tenant A intenta listar productos B, leer orden B, crear ítem con producto B, capturar pago B y usar idempotency-key de B. Ninguna operación debe devolver datos ni cambiar estado B. Probar también token expirado, scope insuficiente y tenant deshabilitado cuando el estudiante lo modele.
