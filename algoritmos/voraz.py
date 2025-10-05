from utils.lectura import leer_entrada

def rocV(archivo_entrada: str):
    """
    Algoritmo voraz para el problema de repartición óptima de cupos.
    Lee la entrada desde un archivo, asigna materias y calcula el costo de insatisfacción.
    """

    # 1. Leer datos de entrada
    materias, estudiantes = leer_entrada(archivo_entrada)

    # Estructura para almacenar asignaciones
    asignaciones = {e["codigo"]: [] for e in estudiantes}

    # 2. Estrategia voraz:
    # Ordenar las solicitudes por prioridad (más alta primero)
    solicitudes = []
    for e in estudiantes:
        for (materia, prioridad) in e["materias"]:
            solicitudes.append((prioridad, e["codigo"], materia))

    solicitudes.sort(reverse=True)  # ordenar de mayor a menor prioridad

    # 3. Asignar cupos de manera voraz
    for prioridad, estudiante, materia in solicitudes:
        if materias[materia] > 0:  # si hay cupo disponible
            asignaciones[estudiante].append((materia, prioridad))
            materias[materia] -= 1

    # 4. Calcular función de insatisfacción general
    costo = calcular_insatisfaccion(estudiantes, asignaciones)

    return asignaciones, costo


def calcular_insatisfaccion(estudiantes, asignaciones):
    """
    Calcula el valor F<M,E>(A) de insatisfacción general.
    """
    total = 0
    for e in estudiantes:
        codigo = e["codigo"]
        msj = e["materias"]
        maj = asignaciones[codigo]

        # tamaños
        msj_size = len(msj)
        maj_size = len(maj)

        if msj_size == 0:
            continue

        factor1 = 1 - (maj_size / msj_size)

        # prioridades de materias no asignadas
        no_asignadas = []
        for (m, p) in msj:
            if not any(m == m_asig for (m_asig, _) in maj):
                no_asignadas.append(p)

        suma_prioridades = sum(no_asignadas)

        gamma = 3 * msj_size - 1
        factor2 = suma_prioridades / gamma if gamma > 0 else 0

        fj = factor1 * factor2
        total += fj

    return total / len(estudiantes)
