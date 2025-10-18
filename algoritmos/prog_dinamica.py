from utils.lectura import leer_entrada
from itertools import combinations
import math

def calcular_insatisfaccion_individual(total_solicitadas, asignadas, prioridades, materias_asignadas):
    """
    Calcular la insatisfacción por estudiante
    """
    if total_solicitadas == 0:
        return 0.0
    materias_no_asignadas = [m for m in prioridades if m not in materias_asignadas]
    suma_prioridades_no_asig = sum(prioridades[m] for m in materias_no_asignadas)
    return (1.0 - (asignadas / total_solicitadas)) * (suma_prioridades_no_asig / ((3 * total_solicitadas) - 1))

def rocPD(archivo_entrada: str):
    materias_dict, estudiantes = leer_entrada(archivo_entrada)

    codigos_materias = list(materias_dict.keys())
    idx_por_materia = {cod: i for i, cod in enumerate(codigos_materias)}
    cupos_iniciales = tuple(materias_dict[cod] for cod in codigos_materias)
    r = len(estudiantes)

    prioridades = {est['codigo']: {m: p for m, p in est['materias']} for est in estudiantes}
    solicitudes_codigos = [[m for m, _ in est['materias']] for est in estudiantes]

    # Matriz: cada fila corresponde a un estudiante, cada columna es un diccionario de cupos
    DP = [ dict() for _ in range(r+1) ]

    def dp(idx, cupos):
        if cupos in DP[idx]:
            return DP[idx][cupos]

        if idx == r:
            DP[idx][cupos] = (0.0, ())
            return DP[idx][cupos]

        estudiante = estudiantes[idx]
        cod_est = estudiante['codigo']
        materias_solicitadas = solicitudes_codigos[idx]
        total_solicitadas = len(materias_solicitadas)

        best_cost = math.inf
        best_assignments = None

        n = total_solicitadas

        insat_por_materia = {}
        for m in materias_solicitadas:
            insat_por_materia[m] = calcular_insatisfaccion_individual(
                total_solicitadas, 1, prioridades[cod_est], (m,)
            )
        materias_ordenadas = sorted(materias_solicitadas, key=lambda x: insat_por_materia[x])

        for s in range(0, n + 1):
            for comb in combinations(range(n), s):
                cupos_list = list(cupos)
                factible = True
                materias_asignadas = tuple(materias_ordenadas[i] for i in comb)
                for m in materias_asignadas:
                    pos = idx_por_materia[m]
                    if cupos_list[pos] == 0:
                        factible = False
                        break
                    cupos_list[pos] -= 1
                if not factible:
                    continue

                f = calcular_insatisfaccion_individual(
                    total_solicitadas, len(materias_asignadas), prioridades[cod_est], materias_asignadas
                )
                proximo_cupos = tuple(cupos_list)
                costo_restante, asign_restante = dp(idx + 1, proximo_cupos)
                costo_total = f + costo_restante

                if costo_total < best_cost:
                    best_cost = costo_total
                    best_assignments = (materias_asignadas,) + asign_restante

        DP[idx][cupos] = (best_cost, best_assignments)
        return DP[idx][cupos]

    costo_total, asignaciones_tuple = dp(0, cupos_iniciales)

    asignaciones_list = []
    for i, a in enumerate(asignaciones_tuple):
        codigo_est = estudiantes[i]['codigo']
        asign_for_student = []
        for m in a:
            p = prioridades.get(codigo_est, {}).get(m, 0)
            asign_for_student.append((m, p))
        asignaciones_list.append(asign_for_student)

    asignaciones_dict = {estudiantes[i]['codigo']: asignaciones_list[i] for i in range(len(estudiantes))}
    insat_promedio = costo_total / r if costo_total < math.inf else math.inf

    return asignaciones_dict, insat_promedio