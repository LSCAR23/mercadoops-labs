# 05 — Datos sintéticos, escalas y calidad

## Generador incluido

Código: `scripts/seed.py`. No necesita Internet ni datos privados. Genera datos reproducibles con `uuid5`, `random.Random`, precio exacto `Decimal`, fecha ancla fija y `.example` para emails.

```powershell
uv run python scripts/seed.py --scale tiny --seed 20261101
```

## Escalas (cifras por tenant, hay 2 tenants)

| Escala | Clientes | Productos | Órdenes | Eventos web | Importaciones raw |
|---|---:|---:|---:|---:|---:|
| `tiny` | 120 | 48 | 600 | 2.500 | 35 |
| `small` | 500 | 120 | 2.500 | 15.000 | 150 |
| `medium` | 2.000 | 250 | 10.000 | 100.000 | 500 |
| `large` | 7.000 | 500 | 50.000 | 500.000 | 2.000 |

Sumar adicionalmente líneas de orden (1–4 por pedido), pagos, envíos y algunos reembolsos. Comienza en `tiny`; `large` puede ocupar recursos relevantes en una máquina de 8 GB.

## Por qué hay defectos intencionales

Los registros de `analytics.raw_orders` simulan recepción de datos externos **sin validación previa**, para practicar perfilado, reglas DQ, tratamiento de duplicados, errores en montos, fechas y datos faltantes. Los defectos **no** se cargan en tablas `core`. No se incluyen algoritmos para identificarlos o corregirlos.

## Idempotencia y precauciones

- Con la misma escala y el mismo seed, los UUID son deterministas y los INSERT usan `ON CONFLICT DO NOTHING`.
- Cambiar el seed **con la misma escala** no reemplaza filas existentes: IDs deterministas colisionarán y conservarán los valores viejos. Aumentar de escala puede agregar filas adicionales y cambiar su distribución. Para comparar semillas/escalas, usa una BD descartable nueva.
- El script no debe modificar tablas de resultados del estudiante (`analytics.daily_sales`, `analytics.data_quality_issues`).
- A diferencia del conjunto `core`, no todos los datos representan fenómenos perfectos; hay sesgos y limitaciones sintéticas que deben declararse en informes.
- Las cohortes de adquisición y las compras usan fechas anteriores o iguales a 2026-11-01.
- `core.inventory` se carga como snapshot inicial; `stock_movements` queda vacío para ejercicios de ledger.

## Perfilado y validación esperados (reto, NO solución)

El estudiante debe crear un informe que contemple conteos, nulos, duplicados por clave de negocio, rangos monetarios, integridad de timestamps, distribución por tenant, reglas de validez JSONB y desviaciones entre fuentes. Documentar si la anomalía implica rechazo, cuarentena o reparación. No generar automáticamente reportes ni aplicar reglas sin decisión del estudiante.

## Aislamiento de experimentos

Cada experimento destructivo debe usar un tenant de prueba o base efímera distinta. No modifiques el dataset semilla en medio de benchmark sin registrar el cambio. En producción no se debe usar el usuario `lab_user` como cuenta privilegiada de la aplicación; es exclusivamente un entorno de estudio.
