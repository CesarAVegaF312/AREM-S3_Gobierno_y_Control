# AREM S3 — Gobierno y Control

Material de la **Sesión 3** del curso *Arquitectura Empresarial* (AREM), Unidad 3:
**Gobierno y Gobernanza de Arquitectura Empresarial**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

La unidad va de tener una arquitectura a **sostenerla**: quién decide si un diseño es aceptable,
con qué reglas, cómo se tratan las excepciones y cómo se sabe si el gobierno funciona. Marcos de
referencia: **TOGAF® Standard, 10th Edition** (documento *Enterprise Architecture Capability and
Governance*), **COBIT® 2019** e **ITIL® 4**.

Las actividades de la unidad, tal como están en la plataforma:

- **Actividad 3.1 — Presentación del reto** · individual · formativa, sin calificación · 4 horas.
  - **Entregable:** dos análisis comparativos de **1 página** cada uno: (a) el gobierno de TI según
    COBIT 2019 frente al gobierno arquitectónico según TOGAF, con sus puntos de articulación y sus
    diferencias; (b) un comparativo con la normativa nacional de Colombia y del Ministerio de las TIC.
  - La retroalimentación se da en la sesión sincrónica con el **F-27**.
- **Actividad 3.2 — Propuesta de sistema de gobierno arquitectónico** · grupal, de **3 a 4
  integrantes** · 20 % · 20 horas.
  - **Entregable:** un documento de gobierno arquitectónico en PDF, de **máximo 15 páginas**, en
    **norma APA 7**. Debe incluir: estructura del ARB, principios, proceso de cumplimiento,
    métricas, gestión de riesgos y articulación con COBIT 2019.
  - Se califica con la rúbrica de la actividad, de cuatro criterios: estructura del ARB y
    principios (1,5), proceso de cumplimiento arquitectónico (1,5), métricas y gestión de riesgos
    (1,25) y articulación COBIT 2019 / ITIL 4 (0,75).
  - **Los formatos F-22 a F-26 no se suben:** son el borrador de las secciones del documento.

---

## Empiecen aquí

1. **Lean el [mapa de la Actividad 3.2](documentos/1_actividad_3_2/AREM_S3_Mapa_Actividad_3_2.pdf).** Dos páginas: qué pide la actividad, con
   qué criterio se califica, en qué sección del documento va cada cosa y qué formato la prepara.
2. **Miren el [documento de ejemplo](documentos/1_actividad_3_2/AREM_S3_Informe_Ejemplo_Actividad_3_2.pdf).** Así se ve la 3.2 terminada, con Red Salud
   Andina. Cada sección abre con un recuadro que explica qué hay que hacer en ella.
3. **Relean las secciones 4, 10, 11 y 13 del [dossier](documentos/2_caso/AREM_Caso_Red_Salud_Andina.pdf)** —o lo equivalente de su caso—: partes
   interesadas, gobierno actual, cifras y restricciones. El gobierno se diseña contra el talento real.

Para trabajar sin conexión, descarguen el repositorio (botón verde **`Code` → `Download ZIP`**),
descomprímanlo y hagan doble clic en `index.html`: la portada abre todos los documentos y
herramientas.

---

## Paso a paso de la unidad

Los pasos siguen el orden en que conviene trabajar. El orden importa: **primero se leen los
episodios del caso, después se escriben los principios que los habrían evitado.** Un principio que
no nace de un hecho de la organización no restringe ninguna decisión.

Los formatos están en los [Instrumentos F-21 a F-28](documentos/3_como_se_hace/AREM_S3_Instrumentos.pdf), y cómo llenarlos con las
herramientas, en la [guía de herramientas y formatos](documentos/3_como_se_hace/AREM_S3_Guia_Herramientas_e_Instrumentos.pdf).

### Paso 0 · Los dos comparativos (Actividad 3.1)

- **Cuándo:** antes de la sesión y durante la semana siguiente, de forma individual.
- **Con qué:** la [guía de la Actividad 3.1](documentos/3_como_se_hace/AREM_S3_Guia_Actividad_3_1.pdf) y las pestañas «COBIT frente a TOGAF» y
  «Normativa colombiana» del [Mapa COBIT · TOGAF · ITIL](interactivos/mapa_cobit_togaf_itil_interactivo.html).
- **Produce:** **F-21**, el esqueleto de los dos comparativos.
- **La pregunta central del segundo:** ¿qué obliga a su organización y qué es solo referencia? El
  Marco de Referencia de Arquitectura Empresarial del MinTIC obliga a entidades públicas y a
  particulares que cumplen funciones públicas; una IPS privada como Red Salud Andina no es sujeto
  obligado, pero sí de la regulación de salud y de protección de datos.

### Paso 1 · Diseñar el ARB

- **Cuándo:** en el **taller de la sesión** (las sillas que debían decidir el episodio); se termina fuera de clase.
- **Con qué:** [Diseñador de ARB](interactivos/disenador_arb_interactivo.html). Calcula el costo del ARB en horas contra la
  capacidad del área y avisa si faltan roles, si no hay nadie de negocio o si una silla depende de
  contratar.
- **Produce:** **F-22** — nombre, mandato, al menos **cuatro roles** con responsabilidades y el
  cargo real que los ocupa, frecuencia, quórum, regla de decisión y escalamiento.
- **Va al documento en:** sección 2.
- **Se califica en:** *Estructura del ARB y principios* (1,5).

### Paso 2 · Escribir los principios

- **Cuándo:** uno o dos en el taller de la sesión; el resto fuera de clase.
- **Con qué:** los episodios del caso y los cinco principios de la Unidad 1 (F-09) como punto de
  partida.
- **Produce:** **F-23** — al menos **ocho principios** con nombre, enunciado, motivación (un hecho
  del caso) e implicaciones.
- **Va al documento en:** sección 3.
- **Se califica en:** *Estructura del ARB y principios* (1,5).

### Paso 3 · Diseñar la revisión de cumplimiento y probarla

- **Cuándo:** en el **taller de la sesión**, con un episodio recorrido hasta el dictamen; se completa fuera de clase.
- **Con qué:** [Compliance Review](interactivos/compliance_review_interactivo.html). Trae los tres episodios de Red Salud Andina
  recorridos, y no deja registrar una excepción sin vencimiento ni sobre un principio no negociable.
- **Produce:** **F-24** — tipos de iniciativa, momentos de revisión, lista de revisión atada a los
  principios, dictámenes y **ruta de excepción**, probados con al menos un episodio real.
- **Va al documento en:** sección 4.
- **Se califica en:** *Proceso de cumplimiento arquitectónico* (1,5). Sin gestión de excepciones no
  hay nota máxima.

### Paso 4 · Articular con COBIT 2019 e ITIL 4

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** [Mapa COBIT · TOGAF · ITIL](interactivos/mapa_cobit_togaf_itil_interactivo.html), pestaña «Mapa de articulación».
- **Produce:** **F-25** — **APO03** y al menos otro objetivo **de gestión**, con qué parte del
  sistema lo opera y su nivel de capacidad actual y objetivo, con plazo; al menos una práctica de
  ITIL 4. Ojo: EDM01 es un objetivo de **gobierno**; se puede mencionar, pero no cuenta como el
  segundo.
- **Va al documento en:** sección 5.
- **Se califica en:** *Articulación COBIT 2019 / ITIL 4* (0,75).

### Paso 5 · Métricas y riesgos

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** [Métricas y riesgos](interactivos/metricas_riesgos_interactivo.html). No guarda una métrica sin fórmula ni umbral, y
  avisa cuando un control no se puede verificar.
- **Produce:** **F-26** — **cinco métricas** con nombre, definición, fórmula, fuente, frecuencia y
  umbral; **tres riesgos** con controles concretos y dueño.
- **Va al documento en:** secciones 6 y 7.
- **Se califica en:** *Métricas y gestión de riesgos* (1,25).

### Paso 6 · Armar el documento y verificar

- **Cuándo:** cuando los pasos 1 a 5 estén listos.
- **Con qué:** el [documento de ejemplo](documentos/1_actividad_3_2/AREM_S3_Informe_Ejemplo_Actividad_3_2.pdf) como guía de estructura y la lista
  del **F-28**, condición por condición, antes de subir.
- **Además de pasar los formatos,** se escriben la sección 1 (contexto, alcance, método y supuestos)
  y la sección 8 (conclusiones), con referencias en APA 7.

**No copien el caso: cópienle la estructura.** El ejemplo es de una IPS de salud; su organización
es otra.

---

## Qué hay en el repositorio

```text
AREM-S3_Gobierno_y_Control/
├── index.html          ← portada: desde aquí se abre todo lo demás
├── presentacion.html   ← la sesión como presentación web animada
├── README.md
├── LICENSE
├── documentos/                 ← PDF, en el orden en que se usan
│   ├── 1_actividad_3_2/        ← qué se entrega y cómo se ve: mapa, documento de ejemplo, enunciado
│   ├── 2_caso/                 ← dossier de Red Salud Andina
│   ├── 3_como_se_hace/         ← instrumentos F-21 a F-28 y guías
│   └── 4_clase/                ← deck de la sesión
├── interactivos/               ← las cuatro herramientas HTML
└── fuentes/                    ← los mismos documentos en Word, y el deck en PowerPoint
```

### `documentos/` — PDF

| Carpeta | Archivo | Descripción |
|---|---|---|
| `1_actividad_3_2` | [`AREM_S3_Mapa_Actividad_3_2.pdf`](documentos/1_actividad_3_2/AREM_S3_Mapa_Actividad_3_2.pdf) | Lo que pide la 3.2, su rúbrica y, para cada requisito, la sección, el formato, cuándo se trabaja y dónde está el ejemplo. |
| | [`AREM_S3_Informe_Ejemplo_Actividad_3_2.pdf`](documentos/1_actividad_3_2/AREM_S3_Informe_Ejemplo_Actividad_3_2.pdf) | Documento de gobierno terminado de Red Salud Andina (13 páginas), con un recuadro por sección. |
| | [`AREM_S3_Enunciado_Actividad_3_2.pdf`](documentos/1_actividad_3_2/AREM_S3_Enunciado_Actividad_3_2.pdf) | El taller de la sesión: la idea que lo organiza, las tareas minuto a minuto, el ejemplo resuelto y los conceptos. |
| `2_caso` | [`AREM_Caso_Red_Salud_Andina.pdf`](documentos/2_caso/AREM_Caso_Red_Salud_Andina.pdf) | El dossier del caso de respaldo, el mismo de las unidades anteriores. |
| `3_como_se_hace` | [`AREM_S3_Instrumentos.pdf`](documentos/3_como_se_hace/AREM_S3_Instrumentos.pdf) | Los ocho formatos F-21 a F-28. |
| | [`AREM_S3_Guia_Actividad_3_1.pdf`](documentos/3_como_se_hace/AREM_S3_Guia_Actividad_3_1.pdf) | Cómo hacer los dos comparativos, con las tablas de referencia de COBIT, TOGAF y la normativa colombiana. |
| | [`AREM_S3_Guia_Herramientas_e_Instrumentos.pdf`](documentos/3_como_se_hace/AREM_S3_Guia_Herramientas_e_Instrumentos.pdf) | Las cuatro herramientas recorridas con el caso y los formatos campo por campo. |
| raíz | [`presentacion.html`](presentacion.html) | La misma sesión como presentación web animada: índice (I), glosario de códigos (G), reloj de la sesión (S) y cronómetro del taller (T). |
| `fuentes` | Los seis documentos en `.docx` y el deck en `.pptx` | Para adaptarlos: cambien lo que necesiten y expórtenlos a PDF. Son los archivos con los que se produjeron los PDF de `documentos/`. |
| `4_clase` | [`AREM_S3_Deck_Reto_U3.pdf`](documentos/4_clase/AREM_S3_Deck_Reto_U3.pdf) | Las 20 diapositivas del encuentro sincrónico: significado, seis ejemplos guiados y el taller. |

### `interactivos/` — herramientas HTML

Son **autocontenidas**: todo el HTML, CSS y JavaScript va dentro de un solo archivo. No requieren
instalación, ni servidor, ni conexión a internet. Lo que se escribe en ellas se guarda solo en el
navegador de quien las usa.

| Archivo | Para qué sirve | Paso |
|---|---|---|
| [`mapa_cobit_togaf_itil_interactivo.html`](interactivos/mapa_cobit_togaf_itil_interactivo.html) | Objetivos de COBIT 2019 frente a los mecanismos de gobierno de TOGAF y las prácticas de ITIL 4, con niveles de capacidad; tablas de la Actividad 3.1. | 0 y 4 |
| [`disenador_arb_interactivo.html`](interactivos/disenador_arb_interactivo.html) | El ARB silla por silla, con su costo en horas y la revisión de lo que pide la rúbrica. | 1 |
| [`compliance_review_interactivo.html`](interactivos/compliance_review_interactivo.html) | Del tipo de iniciativa al dictamen, con registro de excepciones. | 3 |
| [`metricas_riesgos_interactivo.html`](interactivos/metricas_riesgos_interactivo.html) | Constructor de métricas y matriz de riesgos. | 5 |

Las cuatro abren con **Red Salud Andina** y tienen el botón **«Empezar con el caso del grupo»**.
Para abrirlas directamente en blanco, agreguen `?caso=grupo` al final de la dirección.

> Las Sesiones 1 y 2 están en sus propios repositorios:
> [AREM-S1_Marcos_y_Capacidades](https://github.com/CesarAVegaF312/AREM-S1_Marcos_y_Capacidades-repositorio) y
> [AREM-S2_Modelado_y_Decision](https://github.com/CesarAVegaF312/AREM-S2_Modelado_y_Decision).
> El registro de deuda de la Unidad 2 (F-18) recibe las excepciones de esta unidad que dejan deuda.

---

## Problemas frecuentes

**Al hacer clic en un `.html` dentro de GitHub se ve código, no la herramienta.**
GitHub muestra el código fuente, no lo ejecuta. Descarguen el repositorio y ábranlo desde su
computador, o usen el enlace publicado que comparte el docente.

**El doble clic sobre un `.html` abre un editor de texto.**
Clic derecho → **Abrir con** → Chrome, Edge o Firefox.

**La herramienta muestra lo que escribí la última vez.**
Se guarda en el navegador para que no se pierda. Para volver al ejemplo, pulsen
**«Caso Red Salud Andina»**.

---

## Referencias

- Axelos. (2019). *ITIL® foundation: ITIL 4 edition*. TSO.
- Hohpe, G. (2020). *The software architect elevator: Redefining the architect's role in the
  digital enterprise*. O'Reilly Media.
- ISACA. (2018). *COBIT® 2019 framework: Governance and management objectives*. ISACA.
- Ministerio de Tecnologías de la Información y las Comunicaciones. (2023). *Resolución 1978 de
  2023, por la cual se adopta el Marco de Referencia de Arquitectura Empresarial*.
- The Open Group. (2022). *The TOGAF® standard, 10th edition: Enterprise architecture capability
  and governance*. Van Haren Publishing.

La normativa colombiana completa, con su vigencia verificada en septiembre de 2026, está en la
[guía de la Actividad 3.1](documentos/3_como_se_hace/AREM_S3_Guia_Actividad_3_1.pdf).

---

## Licencia

Publicado bajo la **Licencia MIT** — ver [`LICENSE`](LICENSE).

*Nota: TOGAF® es marca registrada de The Open Group; COBIT® de ISACA; ITIL® de AXELOS Limited.
Este repositorio contiene material docente que los explica; la licencia MIT aplica a estos
materiales, no a los marcos originales. Red Salud Andina es una organización simulada con fines
pedagógicos.*
