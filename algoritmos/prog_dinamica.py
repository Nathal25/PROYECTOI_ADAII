from utils.lectura import leer_entrada
from itertools import combinations
import math

def calcular_insatisfaccion_individual(total_solicitadas, asignadas, prioridades, materias_asignadas):
    """
    Calcula la insatisfacción individual de un estudiante según la fórmula dada.
    """
    if total_solicitadas == 0:
        return 0.0
    materias_no_asignadas = [m for m in prioridades if m not in materias_asignadas]
    suma_prioridades_no_asig = sum(prioridades[m] for m in materias_no_asignadas)
    return (1.0 - (asignadas / total_solicitadas)) * (suma_prioridades_no_asig / ((3 * total_solicitadas) - 1))

def rocPD(archivo_entrada: str):
    """
    Asigna cupos minimizando la insatisfacción total usando Programación Dinámica.
    """
    # Leer archivo
    materias_dict, estudiantes = leer_entrada(archivo_entrada)

    # Mapear materias a índices y cupos iniciales
    codigos_materias = list(materias_dict.keys())
    idx_por_materia = {cod: i for i, cod in enumerate(codigos_materias)} #indices de materias
    cupos_iniciales = tuple(materias_dict[cod] for cod in codigos_materias) #cupos de materias
    r = len(estudiantes) #cantidad de estudiantes

    # Crear tabla de prioridades: estudiante -> {materia: prioridad}
    prioridades = {est['codigo']: {m: p for m, p in est['materias']} for est in estudiantes}
    """"
    Objeto con estudiante y las materias solicitadas con su respectiva prioridad 
    {'100': {'1002': 4, '1000': 3, '1001': 5}, '101':...}
    """
    # Crear lista de materias solicitadas por estudiante
    solicitudes_codigos = [[m for m, _ in est['materias']] for est in estudiantes]
    """"
    ejemplo con el archivo de prueba 1
    [['1002', '1000', '1001'], ['1002'], ['1002', '1000'], ['1001', '1002', '1000'], ['1000', '1002']]
    codigos de materias con las solicitudes, cuantas veces se solicitaron materias en arrays diferentes
    """
    # ------------------------------------------------------------
    # PROGRAMACIÓN DINÁMICA MEMOIZADA
    # ------------------------------------------------------------

    DP = {} #estructura de almacenamiento
    def dp(idx, cupos): #para recursion
        """
        Devuelve una tupla (costo mínimo desde este estudiante, asignaciones óptimas restantes).
        - idx: índice del estudiante actual
        - cupos: tupla con los cupos restantes de cada materia
        """
        estado = (idx, cupos)
        if estado in DP:
            return DP[estado] #reutilizar resultados guardados
        
        if idx == r:
            DP[estado] = (0.0, ())
            return DP[estado]
        if idx == r: #indice por estudiante a analizar
            return 0.0, ()

        estudiante = estudiantes[idx]
        cod_est = estudiante['codigo']
        materias_solicitadas = solicitudes_codigos[idx]
        
        total_solicitadas = len(materias_solicitadas)
        
        n = len(materias_solicitadas)
        best_cost = math.inf
        best_assignments = None

        # Generar todas las combinaciones posibles de asignaciones factibles (incluye opción vacía)
        for s in range(0, n + 1):
            for comb in combinations(range(n), s):
                cupos_list = list(cupos)
                factible = True

                for i in comb:
                    materia = materias_solicitadas[i]
                    pos = idx_por_materia[materia]
                    if cupos_list[pos] == 0:
                        factible = False
                        break
                    cupos_list[pos] -= 1

                if not factible:
                    continue

                # Materias asignadas al estudiante actual
                materias_asignadas = tuple(materias_solicitadas[i] for i in comb)
                f = calcular_insatisfaccion_individual(total_solicitadas, len(materias_asignadas),
                                                      prioridades[cod_est], materias_asignadas)

                # Llamada recursiva para el siguiente estudiante
                costo_restante, asign_restante = dp(idx + 1, tuple(cupos_list))
                costo_total = f + costo_restante

                # Si es mejor, actualizar mejor solución
                if costo_total < best_cost:
                    best_cost = costo_total
                    best_assignments = (materias_asignadas,) + asign_restante

        # Si no se pudo asignar nada (muy raro), devolver costo infinito
        DP[estado] = (best_cost, best_assignments)
        return DP[estado]


    # Ejecutar DP desde el primer estudiante con todos los cupos disponibles
    costo_total, asignaciones_tuple = dp(0, cupos_iniciales)
    # asignaciones_tuple contiene para cada estudiante una tupla con los códigos de materias
    # Normalizar a lista de listas y convertir cada código a (materia, prioridad)
    asignaciones_list = []
    for i, a in enumerate(asignaciones_tuple):
        codigo_est = estudiantes[i]['codigo']
        # a es una tupla de códigos de materia, convertir a lista de (materia, prioridad)
        asign_for_student = []
        for m in a:
            # obtener prioridad desde la tabla 'prioridades'
            p = prioridades.get(codigo_est, {}).get(m, None)
            # si no hay prioridad (caso extraño), usamos 0 como fallback
            if p is None:
                p = 0
            asign_for_student.append((m, p))
        asignaciones_list.append(asign_for_student)

    # convertir a diccionario {codigo_estudiante: [(materia, prioridad), ...]}
    asignaciones_dict = {estudiantes[i]['codigo']: asignaciones_list[i] for i in range(len(estudiantes))}
    insat_promedio = costo_total / r if costo_total < math.inf else math.inf

    # print("\n=== Tabla de subestructuras almacenadas ===")
    # for estado, valor in DP.items():
    #     print(f"Estado {estado} -> Costo: {valor[0]:.4f}, Asignaciones parciales: {valor[1]}")
    return asignaciones_dict, insat_promedio