# Cómo se cruza cada incumplimiento con el registro de excepciones del ARB, y qué se
# exige del registro mismo.
#
# "data.hoy" es la fecha de corte de la revisión. La herramienta la pone; con
# --fecha se puede simular el paso del tiempo.
package main

hoy_ns := time.parse_ns("2006-01-02", data.hoy)

no_negociable(p) if p in data.lineamientos.no_negociables

campos_obligatorios := ["justificacion", "aprobada_por", "acta", "aprobada_en", "vence"]

vigente(e) if time.parse_ns("2006-01-02", e.vence) >= hoy_ns

completa(e) if every campo in campos_obligatorios { object.get(e, campo, "") != "" }

duracion_dias(e) := (time.parse_ns("2006-01-02", e.vence) - time.parse_ns("2006-01-02", e.aprobada_en)) / ((24 * 60) * 60e9)

dentro_del_plazo(e) if duracion_dias(e) <= data.lineamientos.plazo_maximo_excepcion_dias

# Solo exime una excepción válida: completa, dentro del plazo, vigente y sobre un principio
# que admite excepciones.
excepcion_vigente(p, s) := e if {
	some e in data.excepciones
	e.principio == p
	e.sujeto == s
	not no_negociable(p)
	completa(e)
	dentro_del_plazo(e)
	vigente(e)
}

# Incumplimiento sin excepción vigente: rompe la revisión.
deny contains sprintf("[%s] %s: %s", [v.principio, v.sujeto, v.motivo]) if {
	some v in incumplimiento
	not excepcion_vigente(v.principio, v.sujeto)
}

# Incumplimiento cubierto por una excepción vigente: se informa, no rompe.
warn contains sprintf("[%s] %s: exceptuado hasta %s (%s). %s",
	[v.principio, v.sujeto, e.vence, e.acta, v.motivo]) if {
	some v in incumplimiento
	e := excepcion_vigente(v.principio, v.sujeto)
}

# Reglas sobre el registro de excepciones.

deny contains sprintf("[EXC] %s en %s: %s no admite excepción", [e.principio, e.sujeto, e.principio]) if {
	input.tipo == "excepciones"
	some e in input.excepciones
	no_negociable(e.principio)
}

deny contains sprintf("[EXC] %s en %s: le falta %s", [e.principio, e.sujeto, campo]) if {
	input.tipo == "excepciones"
	some e in input.excepciones
	some campo in campos_obligatorios
	object.get(e, campo, "") == ""
}

deny contains sprintf("[EXC] %s en %s: venció el %s", [e.principio, e.sujeto, e.vence]) if {
	input.tipo == "excepciones"
	some e in input.excepciones
	not no_negociable(e.principio)
	completa(e)
	not vigente(e)
}

deny contains sprintf("[EXC] %s en %s: dura %d días; el máximo es %d",
	[e.principio, e.sujeto, duracion_dias(e), data.lineamientos.plazo_maximo_excepcion_dias]) if {
	input.tipo == "excepciones"
	some e in input.excepciones
	completa(e)
	not dentro_del_plazo(e)
}
