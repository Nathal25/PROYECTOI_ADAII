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

    materias, estudiantes = leer_entrada(archivo_entrada)
    codigos_materias = list(materias.keys())
    pos_materia = {cod: i for i, cod in enumerate(codigos_materias)}
    cupos_iniciales = tuple(materias[cod] for cod in codigos_materias)
    r = len(estudiantes)
    prioridades = {est['codigo']: {m: p for m, p in est['materias']} for est in estudiantes}
    solicitudes_codigos = [[m for m, _ in est['materias']] for est in estudiantes]
    k = len(cupos_iniciales)
    cupos_max = [c for c in cupos_iniciales]

    """
    lista de factores, cada I es el producto de cupos máximos +1
    utilizado para calcular las posiciones como si el vector de cupos fuera un numero en una base mixta
    """
    I = [1]  # I[0] = 1
    for i in range(1, k):
        I.append(I[i - 1] * (cupos_max[i - 1] + 1))

    """
    Codificar el vector de cupos (tupla de enteros) en un numero único
    usando los factores previos
    """
    def vector_a_numero(cupos):
        """Convierte un vector de cupos a un número único"""
        n = 0
        for i in range(k):
            n += cupos[i] * I[i]
        return n

    """
    Dado un numero codificado reconstruye el vector original de cupos
    Hace divisiones sucesivas por factores de I
    """
    def numero_a_vector(n):
        """Convierte un número único a vector de cupos"""
        cupos = []
        for i in reversed(range(k)):
            div = I[i]
            ci = n // div
            n = n % div
            cupos.append(ci)
        # Como lo construimos al revés, invertimos para que coincida
        return tuple(reversed(cupos))

    # Tamaño total del espacio de estados para cupos
    C = 1
    for c in cupos_max:
        C *= (c + 1)

    # DP como matriz 2D: filas por estudiantes, columnas index por número de cupos restantes
    DP = [[None] * C for _ in range(r + 1)]

    def dp(idx, cupos_num):
        if DP[idx][cupos_num] is not None:
            return DP[idx][cupos_num]

        if idx == r:
            DP[idx][cupos_num] = (0.0, ())
            return DP[idx][cupos_num]

        cupos = numero_a_vector(cupos_num)

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
                    pos = pos_materia[m]
                    if cupos_list[pos] == 0:
                        factible = False
                        break
                    cupos_list[pos] -= 1
                if not factible:
                    continue

                f = calcular_insatisfaccion_individual(
                    total_solicitadas, len(materias_asignadas), prioridades[cod_est], materias_asignadas
                )
                proximo_cupos_num = vector_a_numero(tuple(cupos_list))
                costo_restante, asign_restante = dp(idx + 1, proximo_cupos_num)
                costo_total = f + costo_restante

                if costo_total < best_cost:
                    best_cost = costo_total
                    best_assignments = (materias_asignadas,) + asign_restante

        DP[idx][cupos_num] = (best_cost, best_assignments)
        return DP[idx][cupos_num]

    costo_total, asignaciones_tuple = dp(0, vector_a_numero(cupos_iniciales))

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

rocPD("Prueba1.txt")