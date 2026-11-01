"""Herramienta del laboratorio de gobierno como código.

  python gobierno.py revisar [--fecha AAAA-MM-DD]   corre las reglas sobre la arquitectura
  python gobierno.py metricas [--fecha AAAA-MM-DD]  calcula las métricas de cumplimiento
  python gobierno.py probar                         corre las pruebas de las reglas

Las reglas viven en politicas/ (Rego) y las ejecuta Conftest. Esta herramienta solo arma
la llamada, agrupa el resultado por principio y lo dice en español. "revisar" termina con
código distinto de cero si hay incumplimientos abiertos: así es como rompe un pipeline.
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict

LAB = os.environ.get("LAB", "/lab")
RESULTADOS = os.path.join(LAB, "resultados")
PRINCIPIOS = {
    "P1": "La continuidad de la atención prevalece (no negociable)",
    "P2": "Un solo paciente, una sola identidad",
    "P3": "Se integra por contrato, nunca por la base de datos",
    "P4": "Reutilizar antes de comprar, comprar antes de construir",
    "P5": "La nube se elige por lineamiento, no por proveedor",
    "P6": "Cumplimiento normativo desde el diseño (no negociable)",
    "P7": "Todo sistema tiene dueño y documentación",
    "P8": "El dato se corrige donde nace",
    "EXC": "Registro de excepciones",
    "OBS": "Advertencias de observabilidad (no son principios)",
}
PATRON = re.compile(r"^\[(?P<codigo>[A-Z]+\d*)\] (?P<sujeto>.+?): (?P<texto>.*)$")


def fecha_de_corte(args):
    if args.fecha:
        datetime.date.fromisoformat(args.fecha)  # falla con un mensaje claro si está mal escrita
        return args.fecha
    return datetime.date.today().isoformat()


def entradas():
    return sorted(glob.glob(os.path.join(LAB, "arquitectura", "*.yaml"))) + [os.path.join(LAB, "excepciones.yaml")]


def conftest_test(fecha):
    """Corre las reglas y devuelve la salida JSON de Conftest."""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(f'hoy: "{fecha}"\n')
        hoy = f.name
    orden = ["conftest", "test", *entradas(), "--policy", os.path.join(LAB, "politicas"),
             "--data", os.path.join(LAB, "lineamientos.yaml"),
             "--data", os.path.join(LAB, "excepciones.yaml"),
             "--data", hoy, "--all-namespaces", "--output", "json", "--no-color"]
    r = subprocess.run(orden, capture_output=True, text=True)
    os.unlink(hoy)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        print("Conftest no pudo evaluar las reglas. Esto dijo:\n")
        print(r.stderr or r.stdout)
        sys.exit(2)


def conftest_parse(ruta):
    r = subprocess.run(["conftest", "parse", ruta], capture_output=True, text=True, check=True)
    documento = json.loads(r.stdout)
    # Con un solo archivo, Conftest devuelve el documento; con varios, un objeto por archivo.
    return documento if "tipo" in documento else next(iter(documento.values()))


def clasificar(resultados):
    """Separa los mensajes en abiertos (deny), exceptuados y advertencias (warn)."""
    abiertos, exceptuados, advertencias = defaultdict(list), defaultdict(list), defaultdict(list)
    for archivo in resultados:
        for tipo, destino in (("failures", abiertos), ("warnings", None)):
            for item in archivo.get(tipo) or []:
                m = PATRON.match(item["msg"])
                if not m:
                    advertencias["?"].append((archivo["filename"], item["msg"]))
                    continue
                codigo, sujeto, texto = m["codigo"], m["sujeto"], m["texto"]
                if destino is not None:
                    destino[codigo].append((sujeto, texto))
                elif texto.startswith("exceptuado hasta"):
                    exceptuados[codigo].append((sujeto, texto))
                else:
                    advertencias[codigo].append((sujeto, texto))
    return abiertos, exceptuados, advertencias


def orden_codigos(codigos):
    def clave(c):
        m = re.match(r"P(\d+)$", c)
        return (0, int(m.group(1)), "") if m else (1, 0, c)
    return sorted(codigos, key=clave)


def revisar(args):
    fecha = fecha_de_corte(args)
    abiertos, exceptuados, advertencias = clasificar(conftest_test(fecha))
    print(f"Revisión de cumplimiento arquitectónico · corte {fecha}\n")
    for codigo in orden_codigos(set(abiertos) | set(exceptuados) | set(advertencias)):
        print(f"{codigo} · {PRINCIPIOS.get(codigo, 'principio agregado por el grupo')}")
        for sujeto, texto in sorted(abiertos.get(codigo, [])):
            print(f"  INCUMPLE    {sujeto}: {texto}")
        for sujeto, texto in sorted(exceptuados.get(codigo, [])):
            print(f"  EXCEPTUADO  {sujeto}: {texto}")
        for sujeto, texto in sorted(advertencias.get(codigo, [])):
            print(f"  ADVIERTE    {sujeto}: {texto}")
        print()
    n_abiertos = sum(len(v) for v in abiertos.values())
    n_exc = sum(len(v) for v in exceptuados.values())
    no_negociables = len(abiertos.get("P1", [])) + len(abiertos.get("P6", []))
    print(f"Incumplimientos abiertos: {n_abiertos} · cubiertos por excepción: {n_exc} · "
          f"sobre principios no negociables: {no_negociables}")
    if n_abiertos:
        print("Resultado: NO CUMPLE. En un pipeline, este cambio no pasaría.")
        sys.exit(1)
    print("Resultado: CUMPLE.")


def metricas(args):
    fecha = fecha_de_corte(args)
    abiertos, exceptuados, _ = clasificar(conftest_test(fecha))
    sistemas = conftest_parse(os.path.join(LAB, "arquitectura", "sistemas.yaml"))["sistemas"]
    interfaces = conftest_parse(os.path.join(LAB, "arquitectura", "interfaces.yaml"))["interfaces"]
    excepciones = conftest_parse(os.path.join(LAB, "excepciones.yaml")).get("excepciones") or []

    vencidas = [e for e in excepciones if str(e.get("vence", "")) < fecha]
    bajo_contrato = [i for i in interfaces if i["tipo_mecanismo"] in ("api", "mensajeria") and i.get("versionada")]
    nombres = {s["nombre"] for s in sistemas} | {i["nombre"] for i in interfaces}
    con_incumplimiento = {s for c, lista in abiertos.items() if re.match(r"P\d+$", c)
                          for s, _ in lista if s in nombres}

    def pct(a, b):
        return round(100 * a / b, 1) if b else 0.0

    valores = [
        {"id": "M2", "nombre": "Excepciones vencidas",
         "formula": "excepciones con vencimiento anterior al corte ÷ excepciones registradas × 100",
         "valor": pct(len(vencidas), len(excepciones)), "unidad": "%",
         "umbral": "> 0 %", "alerta": len(vencidas) > 0},
        {"id": "M3", "nombre": "Interfaces bajo contrato",
         "formula": "interfaces por API o mensajería con contrato versionado ÷ interfaces descritas × 100",
         "valor": pct(len(bajo_contrato), len(interfaces)), "unidad": "%",
         "umbral": "< 35 % (meta a 12 meses del informe de ejemplo)", "alerta": pct(len(bajo_contrato), len(interfaces)) < 35},
        {"id": "M4", "nombre": "Capacidades duplicadas sin excepción",
         "formula": "capacidades prestadas por dos o más sistemas sin excepción vigente",
         "valor": len(abiertos.get("P4", [])), "unidad": "",
         "umbral": "> 0", "alerta": len(abiertos.get("P4", [])) > 0},
        {"id": "C1", "nombre": "Sistemas e interfaces que cumplen todos los principios",
         "formula": "sistemas e interfaces sin incumplimientos abiertos ÷ sistemas e interfaces × 100",
         "valor": pct(len(nombres) - len(con_incumplimiento), len(nombres)), "unidad": "%",
         "umbral": "< 80 % (supuesto del laboratorio)", "alerta": pct(len(nombres) - len(con_incumplimiento), len(nombres)) < 80},
        {"id": "C2", "nombre": "Incumplimientos abiertos sobre principios no negociables",
         "formula": "incumplimientos abiertos de P1 y P6",
         "valor": len(abiertos.get("P1", [])) + len(abiertos.get("P6", [])), "unidad": "",
         "umbral": "> 0", "alerta": len(abiertos.get("P1", [])) + len(abiertos.get("P6", [])) > 0},
    ]

    print(f"Métricas de cumplimiento · corte {fecha}\n")
    for m in valores:
        estado = "ALERTA" if m["alerta"] else "ok"
        print(f"{m['id']} · {m['nombre']}: {m['valor']}{(' ' + m['unidad']) if m['unidad'] else ''}  [{estado}]")
        print(f"     Fórmula: {m['formula']}")
        print(f"     Umbral de alerta: {m['umbral']}")
    print("\nIncumplimientos abiertos y exceptuados por principio")
    for codigo in orden_codigos(set(abiertos) | set(exceptuados)):
        print(f"  {codigo:<4} abiertos {len(abiertos.get(codigo, [])):>3}   exceptuados {len(exceptuados.get(codigo, [])):>3}")
    print(f"\nM3 se calcula sobre las {len(interfaces)} interfaces descritas en interfaces.yaml, no sobre las 41 del "
          "inventario formal. M1 y M5 del documento de ejemplo no se pueden calcular aquí: necesitan las actas del "
          "ARB y el registro de solicitudes.")

    os.makedirs(RESULTADOS, exist_ok=True)
    ruta = os.path.join(RESULTADOS, f"metricas-{fecha}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"corte": fecha, "metricas": valores,
                   "por_principio": {c: {"abiertos": len(abiertos.get(c, [])), "exceptuados": len(exceptuados.get(c, []))}
                                     for c in orden_codigos(set(abiertos) | set(exceptuados))}},
                  f, ensure_ascii=False, indent=2)
    print(f"\nGuardado en resultados/{os.path.basename(ruta)}")


def probar(args):
    r = subprocess.run(["conftest", "verify", "--policy", os.path.join(LAB, "politicas"),
                        "--data", os.path.join(LAB, "lineamientos.yaml"), "--no-color"])
    sys.exit(r.returncode)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Gobierno como código: principios que se ejecutan")
    sub = p.add_subparsers(dest="comando", required=True)
    for nombre, funcion, ayuda in (("revisar", revisar, "corre las reglas sobre la arquitectura"),
                                   ("metricas", metricas, "calcula las métricas de cumplimiento")):
        s = sub.add_parser(nombre, help=ayuda)
        s.add_argument("--fecha", help="fecha de corte AAAA-MM-DD; por defecto, hoy")
        s.set_defaults(funcion=funcion)
    s = sub.add_parser("probar", help="corre las pruebas de las reglas")
    s.set_defaults(funcion=probar)
    args = p.parse_args()
    args.funcion(args)
