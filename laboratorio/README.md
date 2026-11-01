# AREM S3 — Laboratorio: gobierno como código

Laboratorio de la **Sesión 3** del curso *Arquitectura Empresarial* (AREM), Unidad 3:
**Gobierno y Gobernanza de Arquitectura Empresarial**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

En la Actividad 3.2 el ARB escribe principios, diseña la revisión de cumplimiento, decide
excepciones y mide. Casi siempre todo eso termina en un PDF que se consulta una vez al mes. En
este laboratorio **los principios se ejecutan**: cada uno se convierte en una regla que revisa
el inventario de arquitectura de la organización y dice qué cumple, qué no y qué está cubierto
por una excepción vigente. En la industria esto se llama *política como código*, y las reglas
que vigilan una característica de la arquitectura se llaman *fitness functions*.

Los ocho principios son los del [documento de ejemplo](../documentos/1_actividad_3_2/AREM_S3_Informe_Ejemplo_Actividad_3_2.pdf)
de la Actividad 3.2, y la arquitectura es la de Red Salud Andina. Las reglas se escriben en
**Rego** y las ejecuta **Conftest**, dos herramientas de uso común para esto. No hay que saber
programar: en cinco de las seis actividades se leen reglas y se toman decisiones, y en la
restante se escribe una regla a partir de una plantilla.

---

## Qué hay en la carpeta

| Archivo | Qué es |
|---|---|
| `arquitectura/sistemas.yaml` | Los 13 sistemas del caso con los datos que leen las reglas. Lo que el dossier no trae está marcado en `supuestos`. |
| `arquitectura/interfaces.yaml` | Las diez integraciones que describe el dossier (sección 7). |
| `arquitectura/agentes.yaml` | Dos agentes de IA que la organización tiene o evalúa. Ningún principio los cubre todavía. |
| `politicas/principios.rego` | Una regla por principio, de P1 a P8, y una advertencia de observabilidad. |
| `politicas/excepciones.rego` | Cómo se cruza cada incumplimiento con el registro de excepciones, y las reglas del registro mismo. |
| `politicas/principios_test.rego` | Las pruebas de las reglas. |
| `politicas/plantilla_principio.rego.txt` | La plantilla para escribir un principio nuevo. |
| `excepciones.yaml` | El registro de excepciones del ARB. |
| `lineamientos.yaml` | Nubes aprobadas, mínimo de personas por sistema, plazo máximo de una excepción y principios no negociables. |
| `ci/gobierno.yml` | El mismo control como paso de GitHub Actions. |

---

## Requisitos

- **Docker Desktop** (Windows o Mac) o Docker Engine con el plugin Compose (Linux). Verifiquen con
  `docker compose version`.
- **Sin Docker en su equipo:** abran el repositorio en **GitHub Codespaces** (botón verde
  **`Code` → `Codespaces`**) y elijan la configuración **«AREM S3 · Laboratorio de gobierno como
  código»**. En la terminal, entren a la carpeta con `cd laboratorio`.

---

## Levantar el laboratorio

```bash
git clone https://github.com/CesarAVegaF312/AREM-S3_Gobierno_y_Control.git
cd AREM-S3_Gobierno_y_Control/laboratorio
docker compose build
docker compose run --rm gobierno probar
```

Todos los comandos de esta guía se ejecutan dentro de la carpeta `laboratorio/`. Si el último
dice que las pruebas pasaron, el laboratorio está listo.

Los tres comandos del laboratorio:

```bash
docker compose run --rm gobierno revisar     # qué cumple, qué no y qué está exceptuado
docker compose run --rm gobierno metricas    # las métricas de cumplimiento, guardadas en resultados/
docker compose run --rm gobierno probar      # las pruebas de las reglas
```

`revisar` y `metricas` aceptan `--fecha AAAA-MM-DD` para revisar en otra fecha de corte.

---

## Actividades

Hagan las seis en orden. Tiempo estimado: dos horas. Si una actividad les pide cambiar un
archivo, al terminar devuélvanlo como estaba (`git checkout -- <archivo>`), salvo que la
actividad diga lo contrario.

### Actividad 1 — La revisión del estado actual

```bash
docker compose run --rm gobierno revisar --fecha 2026-11-01
```

Cada línea dice el principio, el sistema, la interfaz o la capacidad, y el motivo. «Exceptuado»
quiere decir que el ARB aprobó una excepción que sigue vigente. «Advierte» marca algo que vale la
pena mirar pero que no es un principio.

**Registren:** los incumplimientos abiertos por principio, y cuántos son de principios no
negociables (P1 y P6).

**Para pensar:** son 27 incumplimientos abiertos. El ARB que diseñaron, ¿puede atenderlos todos?
¿Con qué criterio los ordena? Los de P1 y P6 no admiten excepción: ¿qué tiene que pasar con ellos?

### Actividad 2 — De la regla al principio

Abran `politicas/principios.rego` y busquen la regla de P3. Compárenla con el enunciado de P3 en
el documento de ejemplo: «Toda integración entre sistemas usa una interfaz publicada y versionada
(API o mensaje); se prohíbe leer o escribir la base de datos de otro sistema».

**Para pensar:** ¿qué parte del principio captura la regla, y qué parte no? Hagan el mismo
ejercicio con P4: la regla detecta capacidades duplicadas, pero no puede saber si alguien
verificó el portafolio antes de comprar. Lo que una regla no puede verificar se queda como
pregunta en la lista de revisión del F-24.

### Actividad 3 — El ARB decide una excepción

El proveedor de AGENDA-WEB tiene su propia nube y el contrato sigue vigente. El ARB acepta, por
un tiempo, que AGENDA-WEB incumpla P5. Agreguen al final de `excepciones.yaml`, con la misma
sangría que las otras:

```yaml
  - principio: P5
    sujeto: AGENDA-WEB
    justificacion: El contrato con el proveedor sigue vigente; migrar antes cuesta más que esperar.
    aprobada_por: ARB
    acta: ARB-2026-10
    aprobada_en: "2026-10-20"
    vence: "2027-09-30"
```

Corran `revisar` otra vez: AGENDA-WEB pasa de «incumple» a «exceptuado» en P5. Ahora intenten dos
excepciones que el registro debe rechazar, una a la vez:

- una sobre **P6** para TELEMED, «porque es un piloto»;
- una sobre **P7** para PORTAL-B2B que venza en **abril de 2028**.

**Registren:** qué dice la revisión en cada caso y por qué.

**Para pensar:** esta es la ruta de excepción del F-24 escrita como regla. ¿Qué gana el ARB si el
registro rechaza solo una excepción mal hecha? ¿Qué sigue necesitando el criterio de una persona?

Dejen la excepción de P5 para la actividad 4; quiten las otras dos.

### Actividad 4 — El tiempo pasa

```bash
docker compose run --rm gobierno revisar --fecha 2027-03-15
docker compose run --rm gobierno metricas --fecha 2026-11-01
docker compose run --rm gobierno metricas --fecha 2027-03-15
```

La excepción de P3 sobre HIS-CORE → FACT-SALUD venció el 28 de febrero de 2027.

**Registren:** cómo cambian el reporte y las métricas M2, M3 y M4 entre las dos fechas.

**Para pensar:** cuando una excepción vence, ¿qué hace el ARB: la renueva, la cierra o la escala?
Una excepción que se renueva sin cambios cada año, ¿es una excepción o es la arquitectura real?

Al terminar, devuelvan `excepciones.yaml` como estaba.

### Actividad 5 — Un principio para la IA

`arquitectura/agentes.yaml` describe dos agentes de IA, y ninguno de los ocho principios los
cubre. Escriban **P9** como regla con este enunciado:

> **Ningún agente de IA escribe en un sistema asistencial sin aprobación humana.**

1. Copien la plantilla: `cp politicas/plantilla_principio.rego.txt politicas/p9_ia.rego`.
2. Cambien el motivo y escriban las condiciones. Los campos que necesitan están en
   `agentes.yaml`: `escribe_en` es una lista, y cada elemento tiene `sistema` y `asistencial`;
   el agente tiene además `aprobacion_humana`.
3. Corran `revisar` y verifiquen que P9 marca al agente correcto, y solo a ese.

Después escriban **un segundo principio de IA propio**, por ejemplo sobre las *evals* o sobre los
datos que salen de la organización, con su enunciado y su regla.

**Registren:** el enunciado de cada principio, la regla y el resultado de la revisión.

**Opcional:** agreguen una prueba para P9 en `politicas/principios_test.rego` y córranla con
`probar`.

### Actividad 6 — La revisión en el pipeline

Hasta aquí la revisión se corre a mano. En un equipo, corre sola en cada cambio.

1. Hagan un *fork* del repositorio en su cuenta de GitHub y clónenlo.
2. Copien el workflow: `mkdir -p .github/workflows && cp laboratorio/ci/gobierno.yml .github/workflows/`
   (desde la raíz del repositorio), y súbanlo a `main`.
3. Creen una rama, cambien `versionada: false` por `versionada: true` en la interfaz
   AGENDA-WEB → HIS-CORE de `arquitectura/interfaces.yaml`, y abran un pull request.

El pull request queda en rojo mientras haya incumplimientos abiertos, y el detalle del paso
«Revisión de cumplimiento» muestra cuáles son.

**Para pensar:** un ARB que se reúne cada mes frente a un control que corre en cada cambio. ¿Qué
decisiones pueden quedar en el control y cuáles tienen que seguir en el ARB? ¿Qué le pasa a la
métrica M5 del documento de ejemplo, el tiempo de dictamen?

---

## Del laboratorio al documento

| Sección del documento de la 3.2 | Qué aporta el laboratorio |
|---|---|
| 3 · Principios | Cada principio puede citar su regla como implicación verificable. Lo que la regla no captura (actividad 2) es lo que el ARB revisa a mano. |
| 4 · Proceso de cumplimiento | La revisión automática como primer filtro de la Compliance Review, y el registro de excepciones con sus reglas. |
| 6 · Métricas | M2, M3 y M4 calculadas con fórmula, fuente y umbral, en una fecha de corte declarada. |
| 7 · Riesgos | Lo que la revisión deja ver: por ejemplo, P7 en HIS-CORE es el riesgo de concentración de conocimiento. |

Dos advertencias para el análisis:

- **Es un modelo de la arquitectura, no la arquitectura.** Las reglas solo ven lo que está en los
  archivos de `arquitectura/`, y varios datos son supuestos marcados como tales. Un inventario
  desactualizado da una revisión que parece rigurosa y no lo es.
- **M3 se calcula sobre las diez interfaces descritas**, no sobre las 41 del inventario formal. M1
  y M5 no se pueden calcular aquí: necesitan las actas del ARB y el registro de solicitudes.

---

## Problemas frecuentes

**«Conftest no pudo evaluar las reglas».**
Hay un error de sintaxis en un archivo `.rego`. El mensaje que sigue dice el archivo y la línea.
Revisen que las llaves estén cerradas y que cada condición esté en su propia línea.

**Una excepción no exime nada.**
El `sujeto` tiene que estar escrito exactamente como aparece en el reporte, incluida la flecha
de las interfaces (`→`). Revisen también que la excepción esté completa y dentro del plazo: si
no, el registro la rechaza y no exime.

**Un error de YAML al correr `revisar`.**
Casi siempre es la sangría. Cada excepción empieza con `  - ` (dos espacios, guion, espacio) y
sus campos van alineados debajo de la palabra `principio`.

**Mi regla nueva no reporta nada.**
Una condición que nunca se cumple deja la regla muda. Pruébenla con un agente que sepan que
incumple, y revisen que el archivo termine en `.rego`.

---

## Licencia

Este laboratorio es parte del repositorio de la Sesión 3 y se distribuye con su misma licencia,
[Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es),
incluido el código del laboratorio.

*Nota: Red Salud Andina es una organización simulada con fines pedagógicos.*
