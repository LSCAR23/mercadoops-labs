# 15 — Plan de 20 semanas + evaluación de dominio

## Ruta sugerida (8–12 h/semana)

| Semana | Enfoque | Entregable verificable |
|---|---|---|
| 1 | Infra, migraciones y diccionario | Setup limpio + ejecución seed 2 veces |
| 2 | SQL fundamentos I | SQL-001–005 |
| 3 | SQL fundamentos II | SQL-006–010 |
| 4 | SQL fundamentos III | SQL-011–014 + revisión |
| 5 | Python bases I | PY-001–005 |
| 6 | Python bases II | PY-006–010 |
| 7 | Python bases III | PY-011–014 + refactor |
| 8 | SQL experto I | SQL-015–019 |
| 9 | SQL experto II | SQL-020–024 |
| 10 | SQL experto III | SQL-025–030 |
| 11 | Python experto I | PY-015–019 |
| 12 | Python experto II | PY-020–024 |
| 13 | Python experto III | PY-025–028 + benchmark |
| 14 | Backend base I | BE-001–006 |
| 15 | Backend base II | BE-007–012 |
| 16 | Backend senior I | BE-013–017 |
| 17 | Backend senior II | BE-018–022 |
| 18 | Backend senior III | BE-023–026 + QA-001–006 |
| 19 | QA/OPS + capstone | QA-007–012 y alcance MVP |
| 20 | Capstone y defensa | Proyecto elegido + demo de fallos |

Este calendario es intenso; es válido distribuirlo en más semanas. El objetivo no es marcar casillas: si un lab no supera pruebas, permanece pendiente.

## Rúbrica única por reto (100 puntos)

| Dimensión | Peso | Excelente exige |
|---|---:|---|
| Correctitud semántica | 30 | Business definition coherente, casos límite |
| Pruebas / reproducibilidad | 20 | Tests automatizados, dataset/seed y comandos |
| Calidad de código / SQL | 15 | Legibilidad, tipos, nombres, modularidad |
| Rendimiento / escalabilidad | 15 | Medición y elección proporcional al problema |
| Seguridad / integridad | 10 | Tenant isolation, sanitización, transacciones |
| Comunicación / decisiones | 10 | ADR o informe, limitaciones, explicaciones |

**Aprobación:** 80+ y sin falla crítica. **Nivel experto / senior:** 90+ en los retos finales, incluyendo pruebas de fallo real y defensa técnica. Una filtración cross-tenant o pérdida de dinero simulada es falla crítica aun si el puntaje numérico es alto.

## Criterios diferenciados

**Analista experto:** puede definir KPI con precisión, distinguir sesgos, defender técnicas estadísticas, conciliar fuentes, optimizar consultas y construir pipelines reproducibles con calidad de datos.

**Backend senior:** diseña contratos y evoluciona esquemas, anticipa simultaneidad, demuestra aislamiento y seguridad, maneja errores/transacciones/reintentos, mide sistemas y documenta decisiones y recuperación.

## Seguimiento sin spoilers

La tabla de progreso y las notas pueden almacenarse en `workspaces/PROGRESO.md` creada por el estudiante. Para cada lab registrar estado: no iniciado / bloqueado / en curso / aprobado / refactor. Copilot podrá puntuar **tu implementación**, no escribirla en tu lugar. En revisiones pedir tres preguntas técnicas de defensa sobre cada decisión importante.
