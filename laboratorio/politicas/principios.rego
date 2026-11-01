# Los principios del informe de ejemplo de la Actividad 3.2, escritos como reglas.
#
# Cada regla agrega un incumplimiento a "incumplimiento" con tres campos:
#   principio  P1 a P8
#   sujeto     el sistema, la interfaz o la capacidad que lo incumple
#   motivo     por qué, en una frase
#
# excepciones.rego decide después si el incumplimiento está cubierto por una excepción
# vigente del ARB o si queda abierto.
package main

# P1 · La continuidad de la atención prevalece. No negociable.
incumplimiento contains {"principio": "P1", "sujeto": s.nombre,
	"motivo": "soporta atención y no tiene una ruta de operación degradada probada"} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	s.asistencial
	not s.modo_degradado_probado
}

# P2 · Un solo paciente, una sola identidad.
incumplimiento contains {"principio": "P2", "sujeto": s.nombre,
	"motivo": "crea pacientes por su cuenta en lugar de consumir el índice maestro"} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	s.crea_pacientes
}

# P3 · Se integra por contrato, nunca por la base de datos.
incumplimiento contains {"principio": "P3", "sujeto": i.nombre,
	"motivo": sprintf("integra por %s, no por una interfaz publicada", [i.tipo_mecanismo])} if {
	input.tipo == "interfaces"
	some i in input.interfaces
	i.tipo_mecanismo in {"base_de_datos", "archivos"}
}

incumplimiento contains {"principio": "P3", "sujeto": i.nombre,
	"motivo": "tiene interfaz publicada pero el contrato no está versionado"} if {
	input.tipo == "interfaces"
	some i in input.interfaces
	i.tipo_mecanismo in {"api", "mensajeria"}
	not i.versionada
}

# P4 · Reutilizar antes de comprar, comprar antes de construir: no se duplican capacidades.
incumplimiento contains {"principio": "P4", "sujeto": capacidad,
	"motivo": sprintf("la prestan %d sistemas: %s", [count(quienes), concat(", ", sort(quienes))])} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	some capacidad in s.capacidades
	quienes := {t.nombre | some t in input.sistemas; capacidad in t.capacidades}
	count(quienes) > 1
}

# P5 · La nube se elige por lineamiento, no por proveedor.
incumplimiento contains {"principio": "P5", "sujeto": s.nombre,
	"motivo": sprintf("está en «%s», que no es una nube aprobada", [s.nube])} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	s.nube != null
	not s.nube in data.lineamientos.nubes_aprobadas
}

# P6 · Cumplimiento normativo desde el diseño. No negociable.
incumplimiento contains {"principio": "P6", "sujeto": s.nombre,
	"motivo": "trata datos de salud sin evaluación de impacto de datos personales (Ley 1581 de 2012)"} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	s.datos_sensibles
	not s.evaluacion_datos_personales
}

# P7 · Todo sistema tiene dueño y documentación.
incumplimiento contains {"principio": "P7", "sujeto": s.nombre,
	"motivo": sprintf("no tiene %s", [campo])} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	some campo in ["dueno_negocio", "responsable_ti"]
	object.get(s, campo, null) == null
}

incumplimiento contains {"principio": "P7", "sujeto": s.nombre,
	"motivo": sprintf("personas que lo conocen, descontando las salidas previstas: %d (mínimo %d)",
		[efectivas, data.lineamientos.minimo_personas_que_lo_conocen])} if {
	input.tipo == "sistemas"
	some s in input.sistemas
	efectivas := s.personas_que_lo_conocen - object.get(s, "salidas_previstas", 0)
	efectivas < data.lineamientos.minimo_personas_que_lo_conocen
}

# P8 · El dato se corrige donde nace: ni cargas manuales ni datos que se digitan otra vez.
incumplimiento contains {"principio": "P8", "sujeto": i.nombre,
	"motivo": "el dato pasa a mano de un sistema a otro"} if {
	input.tipo == "interfaces"
	some i in input.interfaces
	i.tipo_mecanismo in {"manual", "inexistente"}
}

# Advertencia, no principio: una integración sin alertas falla en silencio.
warn contains sprintf("[OBS] %s: no tiene alertas; si falla, nadie se entera", [i.nombre]) if {
	input.tipo == "interfaces"
	some i in input.interfaces
	not i.tipo_mecanismo in {"manual", "inexistente"}
	not i.alertas
}
