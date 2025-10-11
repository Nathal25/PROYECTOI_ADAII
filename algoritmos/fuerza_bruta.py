from utils.lectura import leer_entrada
from itertools import combinations


def rocFB(archivo_entrada: str):
    """
    Algoritmo de fuerza bruta (correcta) que enumera, por estudiante,
    todas las combinaciones de materias solicitadas y devuelve la mejor
    asignación encontrada y su insatisfacción promedio.
    """
    materias, estudiantes = leer_entrada(archivo_entrada)

    # estructuras iniciales
    codigos_est = [e["codigo"] for e in estudiantes]
    asign_actual = {c: [] for c in codigos_est}
    cupos_inicial = materias.copy()

    mejor_asign = None
    mejor_costo = float('inf')

    # recursión por estudiante
    def backtrack(i, cupos, asignaciones):
        nonlocal mejor_asign, mejor_costo
        if i == len(estudiantes):
            # evaluar costo
            F = calcular_insatisfaccion(estudiantes, asignaciones)
            if F < mejor_costo:
                mejor_costo = F
                # deep copy of assignments
                mejor_asign = {k: list(v) for k, v in asignaciones.items()}
            return

        est = estudiantes[i]
        codigo = est["codigo"]
        prefs = [m for m, _ in est["materias"]]

        # probar todas las combinaciones de materias solicitadas para este estudiante
        n = len(prefs)
        for s in range(0, n + 1):
            for comb in combinations(range(n), s):
                factible = True
                usados = []
                for idx in comb:
                    m = prefs[idx]
                    if cupos.get(m, 0) <= 0:
                        factible = False
                        break
                    usados.append(m)

                if not factible:
                    continue

                # aplicar asignacion temporal
                for m in usados:
                    cupos[m] -= 1
                    # prioridad correspondiente
                    p = next(pv for mv, pv in est["materias"] if mv == m)
                    asignaciones[codigo].append((m, p))

                # recursar
                backtrack(i + 1, cupos, asignaciones)

                # deshacer asignacion temporal
                for m in usados:
                    cupos[m] += 1
                for _ in usados:
                    asignaciones[codigo].pop()

    backtrack(0, cupos_inicial, asign_actual)

    return mejor_asign, mejor_costo

def calcular_insatisfaccion(estudiantes, asignaciones):
    """
    Calcula la insatisfacción promedio F<M,E>(A) dada una asignación A.
    """
    total_insatisfaccion = 0.0
    for est in estudiantes:
        codigo = est["codigo"]
        materias_solicitadas = {m for m, _ in est["materias"]}
        prioridades = {m: p for m, p in est["materias"]}
        materias_asignadas = {m for m, _ in asignaciones[codigo]}
        total_solicitadas = len(materias_solicitadas)
        asignadas = len(materias_asignadas)
        
        if total_solicitadas == 0:
            continue
        
        materias_no_asignadas = materias_solicitadas - materias_asignadas
        suma_prioridades_no_asig = sum(prioridades[m] for m in materias_no_asignadas)
        
        insatisfaccion = (1.0 - (asignadas / total_solicitadas)) * (suma_prioridades_no_asig / ((3 * total_solicitadas) - 1))
        total_insatisfaccion += insatisfaccion

    return total_insatisfaccion / len(estudiantes) if estudiantes else 0.0

#rocFB('pruebas/Prueba1.txt')