# 16 — Prompts listos para pegar en GitHub Copilot Chat

## Prompt 1 — Auditoría del ZIP y bootstrap (ejecutar primero)

> Lee en este orden `README.md`, `.github/copilot-instructions.md`, `docs/00-CONTRATO-AGENTE.md`, `docs/01-ARQUITECTURA.md`, `docs/02-INSTALACION.md` y `docs/03-MIGRACIONES.md`. Tu tarea es validar y reparar SOLO el entorno de MercadoOps Labs. No implementes consultas, algoritmos, endpoints, dashboards ni resultados de los laboratorios. Comprueba archivos y dependencias; ejecuta los comandos de arranque (o señala el bloqueo real); aplica las 5 migraciones; carga `tiny`; comprueba idempotencia, tests de bootstrap y health checks. Si un comando falla, diagnostícalo con evidencia y vuelve a ejecutarlo. No declares pruebas exitosas sin ejecutarlas. Antes de modificar, di qué archivo cambiarás y por qué. Al final entrega un reporte exacto de comandos, archivos cambiados, tests y laboratorios que siguen sin resolver.

## Prompt 2 — Preparar un laboratorio SQL sin respuesta

> Quiero trabajar el laboratorio `SQL-___` definido en `docs/07-LABS-SQL-BASE.md` o `docs/08-LABS-SQL-EXPERTO.md`. Crea únicamente `workspaces/sql/SQL-___.sql` con un bloque de comentarios que copie el objetivo, parámetros, tablas permitidas, casos de prueba, limitaciones y una sección `-- TODO(student)`. No escribas ni siquiera una versión parcial de la consulta final. Solo indica preguntas guía para que yo decida la solución.

## Prompt 3 — Preparar un laboratorio Python sin respuesta

> Activa `PY-___` según la especificación. Crea un archivo vacío con docstring, tipos de las entradas/salidas y `raise NotImplementedError` para la función principal, únicamente cuando la firma se desprenda inequívocamente del contrato. No implementes lógica, no agregues pseudo-soluciones en comentarios ni tests que entreguen la lógica. Pregúntame primero mi diseño propuesto y después revísalo sin resolverlo.

## Prompt 4 — Preparar un laboratorio Backend sin respuesta

> Activa `BE-___`. Extrae solamente los contratos HTTP, entidades relacionadas, reglas de seguridad, transacciones exigidas, errores y casos de test. Crea un `workspaces/backend/BE-___.md` con checklist y un ADR vacío. No implementes rutas, servicios, repositorios ni lógica de negocio todavía. Ayúdame a planificarlo y espera mi implementación.

## Prompt 5 — Revisar mi implementación (modo mentor)

> Revisa mi solución del laboratorio `___` según su especificación. No la reescribas. Ejecuta tests/linter si están disponibles y enumera problemas como P0 (seguridad/integridad), P1 (correctitud), P2 (eficiencia), P3 (estilo). Dame como máximo 3 pistas, de menor a mayor especificidad; plantea 2 casos de prueba adicionales, sin código de solución. Da una calificación según `docs/15-RUTA-Y-RUBRICAS.md` y solicita mis correcciones.

## Prompt 6 — Evaluación estilo entrevista senior

> Asume rol de entrevistador técnico. Elige una funcionalidad que YA implementé en MercadoOps Labs. Hazme 5 preguntas una por una sobre transacciones, riesgos, performance, pruebas y alternativas. Tras cada respuesta evalúa razonamiento técnico y comunicación; no me entregues la solución antes de mi intento. Al final da recomendaciones precisas.

## Prompt 7 — Solicitar solo una pista

> Estoy bloqueado en el laboratorio `___`, específicamente en `___`. Mi intento actual es `___`. No resuelvas el problema. Dame un solo hint conceptual o un edge case que me permita descubrir el siguiente paso, y una pregunta que yo deba contestar.

## Prompt 8 — Crear nueva fase sin resolver la anterior

> Lee la rúbrica y el progreso. Prepara exclusivamente el entorno de la siguiente fase, sin editar archivos `workspaces/` completados ni modificar las migraciones existentes. Si necesitas una tabla o dependency nueva, explícala antes de implementarla y crea migración incremental. No anticipes ningún cálculo o ruta que corresponda a un lab posterior.

## Prompt 9 — Documentación sin spoilers

> Actualiza el README con instrucciones de ejecución, diagramas de arquitectura, inventario de migraciones, endpoints existentes y pruebas comprobadas. No agregues consultas de solución, código de algoritmo, dashboards de resultados o rutas que el estudiante todavía no implementó.

## Cuándo permitir soluciones

Solo cuando yo escriba expresamente “dame la solución completa de LAB-___” Copilot podrá entregar esa solución. Una petición como “prepárame el laboratorio”, “ayúdame”, “revísalo” o “explícamelo” **no** autoriza resolverlo.
