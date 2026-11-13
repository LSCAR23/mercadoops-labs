# 06 — Metodología, disciplina de laboratorio y entregables

## Ciclo recomendado para cada reto

1. **Leer** el enunciado sin pedir solución a IA.
2. **Definir** los supuestos (negocio, timezone, estados, duplicados y eventos).
3. **Diseñar** pseudocódigo, diagrama de flujo o contrato de entrada/salida.
4. **Implementar** en `workspaces/` con autoría propia.
5. **Verificar** casos normales, vacíos, límites, negativos y de tenants cruzados.
6. **Medir** (tiempo, plan de SQL, memoria, consultas, errores cuando aplique).
7. **Documentar** resultado, decisiones y trade-offs.
8. **Solicitar feedback de Copilot Chat** sin solución completa (primera respuesta: solo evaluación y pistas).

## Nombres de archivos y contenido

- SQL: `workspaces/sql/SQL-001.sql`, etc., solo lo que el estudiante escriba.
- Python: `workspaces/python/PY-001.py`, etc., con funciones testeables, sin notebooks como único artefacto.
- Backend: `workspaces/backend/BE-001.md` para ADR, y código real en `src/mercadoops/` **solo al resolver**.
- Entregas: un `workspaces/LAB-REPORT.md` por reto terminado o una carpeta `reports/` creada por el estudiante.

## Plantilla de reporte (no es solución)

```markdown
# LAB-ID — Título
- Fecha y dataset/escala:
- Hipótesis y definición del indicador:
- Archivos implementados:
- Decisiones de diseño y alternativas:
- Casos de prueba (entradas/salidas, sin secretos):
- Resultados y evidencia (comandos reales):
- Rendimiento medido / EXPLAIN:
- Limitaciones y posibles fallos:
- Qué haría distinto en producción:
```

## Criterios transversales

- SQL correcto y deterministicamente explicable (documentar desempates y tratamiento de nulos).
- Python con tipos, errores explícitos, funciones pequeñas y sin mezclar I/O con lógica pura.
- Backend con contratos API consistentes, transacciones, seguridad y observabilidad.
- Ninguna solución acepta datos de otro tenant por ID aislado.
- Nunca se aprueba un ejercicio únicamente porque devuelve un número plausible.

## Modo de ayuda progresiva para Copilot Chat

1. **Hint 1:** definición conceptual o qué parte leer.
2. **Hint 2:** caso mínimo que podría romper la implementación.
3. **Hint 3:** pista de API/operador, sin código listo para copiar.
4. **Review:** críticas de tu implementación y test cases adicionales.
5. **Solución:** solo si el estudiante lo solicita expresamente; documentar que rompe el modo de evaluación independiente.

## Regla de no spoilers

Las especificaciones describen QUÉ y CÓMO PROBAR, no CÓMO IMPLEMENTAR. Los archivos de infraestructura contienen SQL y Python porque son necesarios para un entorno reproducible, no como respuestas de los ejercicios.
