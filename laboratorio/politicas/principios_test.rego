# Pruebas de las reglas. Una regla de gobierno también es código, y también puede estar mal:
# estas pruebas verifican que incumple lo que debe incumplir y que deja pasar lo que debe.
#   python gobierno.py probar
package main

sistema_ok := {"nombre": "SISTEMA-X", "asistencial": false, "crea_pacientes": false,
	"capacidades": ["Capacidad X"], "nube": null, "datos_sensibles": false,
	"dueno_negocio": "Negocio", "responsable_ti": "TI", "personas_que_lo_conocen": 3}

excepcion_p2 := {"principio": "P2", "sujeto": "SISTEMA-X", "justificacion": "j", "aprobada_por": "ARB",
	"acta": "A", "aprobada_en": "2026-08-01", "vence": "2027-01-31"}

test_sistema_sin_problemas_cumple if {
	r := incumplimiento with input as {"tipo": "sistemas", "sistemas": [sistema_ok]}
	count(r) == 0
}

test_p3_base_de_datos_incumple if {
	r := incumplimiento with input as {"tipo": "interfaces", "interfaces": [
		{"nombre": "A → B", "tipo_mecanismo": "base_de_datos", "versionada": false, "alertas": true}]}
	some v in r
	v.principio == "P3"
}

test_p3_api_versionada_cumple if {
	r := incumplimiento with input as {"tipo": "interfaces", "interfaces": [
		{"nombre": "A → B", "tipo_mecanismo": "api", "versionada": true, "alertas": true}]}
	count(r) == 0
}

test_p7_salida_prevista_cuenta if {
	s := object.union(sistema_ok, {"personas_que_lo_conocen": 2, "salidas_previstas": 1})
	r := incumplimiento with input as {"tipo": "sistemas", "sistemas": [s]}
	some v in r
	v.principio == "P7"
}

test_excepcion_vigente_exceptua if {
	s := object.union(sistema_ok, {"crea_pacientes": true})
	r := deny with input as {"tipo": "sistemas", "sistemas": [s]}
		with data.excepciones as [excepcion_p2]
		with data.hoy as "2026-11-01"
	count(r) == 0
}

test_excepcion_vencida_no_exceptua if {
	s := object.union(sistema_ok, {"crea_pacientes": true})
	r := deny with input as {"tipo": "sistemas", "sistemas": [s]}
		with data.excepciones as [excepcion_p2]
		with data.hoy as "2027-02-01"
	count(r) == 1
}

test_no_negociable_no_admite_excepcion if {
	r := deny with input as {"tipo": "excepciones", "excepciones": [{"principio": "P1", "sujeto": "SISTEMA-X",
		"justificacion": "j", "aprobada_por": "ARB", "acta": "A", "aprobada_en": "2026-08-01", "vence": "2027-01-31"}]}
		with data.hoy as "2026-11-01"
	some m in r
	contains(m, "no admite excepción")
}

test_excepcion_demasiado_larga_rechazada if {
	r := deny with input as {"tipo": "excepciones", "excepciones": [{"principio": "P3", "sujeto": "A → B",
		"justificacion": "j", "aprobada_por": "ARB", "acta": "A", "aprobada_en": "2026-01-01", "vence": "2027-12-31"}]}
		with data.hoy as "2026-11-01"
	some m in r
	contains(m, "el máximo es")
}

test_excepcion_demasiado_larga_no_exime if {
	s := object.union(sistema_ok, {"crea_pacientes": true})
	larga := object.union(excepcion_p2, {"aprobada_en": "2026-01-01", "vence": "2027-12-31"})
	r := deny with input as {"tipo": "sistemas", "sistemas": [s]}
		with data.excepciones as [larga]
		with data.hoy as "2026-11-01"
	count(r) == 1
}
