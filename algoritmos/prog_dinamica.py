from utils.lectura import leer_entrada
from functools import lru_cache
from itertools import combinations
from collections import defaultdict

def calcular_insatisfaccion_individual(total_solicitadas, asignadas):
    
    if total_solicitadas == 0:
        return 0.0
    no_asignadas = total_solicitadas - asignadas
    # formula dada
    return (1.0 - (asignadas / total_solicitadas)) * (no_asignadas / (3 * total_solicitadas - 1))


def rocPD(archivo_entrada: str):
    # 1) Leer entrada
    materias_dict, estudiantes = leer_entrada(archivo_entrada)  # materias: {codigo: cupos}, estudiantes: lista dicts
    #materias_dict diccionario con las materias y los cupos de cada una
    # Mapear materias a índices estables para representar el vector de cupos como tupla
    codigos_materias = list(materias_dict.keys()) #codigos de las materias
    idx_por_materia = {cod: i for i, cod in enumerate(codigos_materias)} #indice de las materias
    cupos_iniciales = tuple(materias_dict[c] for c in codigos_materias) #cupos para cada materia

    # Preparar estructura de estudiantes: lista ordenada de dicts
    # Cada estudiante: {"codigo": str, "materias": [(cod_materia, prioridad), ...]}
    # Asegurarse que materias estén en el mismo orden o cualquier orden está bien
    estudiantes_orden = estudiantes  # se procesan en el orden dado (puede cambiarse)
    
    r = len(estudiantes_orden) #cantidad de estudiantes
  
    # Para reconstrucción: guardaremos, en memo, la decisión óptima por estado
    decision = {}  # key = (idx_est, cupos_tuple) -> best_subset_assigned (as tuple of materia indices)

    # 2) DP con memoization: estado = (idx_est, cupos_tuple)
    @lru_cache(maxsize=None)
    def dp(idx_est, cupos_tuple):
        """
        Retorna (insatisfaccion_minima_acumulada_desde_idx_est, asignaciones_parciales)
        asignaciones_parciales se devolverá como None aquí para evitar copies pesadas;
        la reconstrucción se hará usando 'decision' dict poblado en paralelo.
        """
        # Caso base: todos los estudiantes procesados
        if idx_est >= r:
            return 0.0

        est = estudiantes_orden[idx_est]
        solicitudes = est['materias']  # lista de (codigo_materia, prioridad) -- prioridad no usada en formula actual
        s_len = len(solicitudes)

        # Convertir solicitudes a índices y mantener prioridades si se requiere luego
        sols_idx = []
        for cod, pr in solicitudes:
            if cod not in idx_por_materia:
                continue
            sols_idx.append((idx_por_materia[cod], cod, pr))

        # Generar todos los subconjuntos factibles de solicitudes del estudiante
        # Observación: si s_len es pequeño (enunciado sugiere valores como 3), enumerar subconjuntos es viable.
        mejor_cost = float('inf')
        mejor_subset = tuple()

        # Se itera por cardinalidad para poder priorizar subconjuntos con más asignaciones si hay empate
        # Pero lo correcto es probar todos y escoger el que minimice la insatisfacción total.
        n_sols = len(sols_idx)
        # Para performance: precomputar los indices y codigos
        indices = [t[0] for t in sols_idx]
        codigos = [t[1] for t in sols_idx]

        # Iterar todos los subconjuntos usando combinaciones
        # Nota: si n_sols es 0, se ejecutará la iteración vacía correctamente
        for r_comb in range(n_sols + 1):
            for comb in combinations(range(n_sols), r_comb):
                # Verificar factibilidad: para cada materia en comb, cupo > 0
                factible = True
                nuevos_cupos = list(cupos_tuple)
                for pos in comb:
                    mat_idx = indices[pos]
                    if nuevos_cupos[mat_idx] <= 0:
                        factible = False
                        break
                    nuevos_cupos[mat_idx] -= 1
                if not factible:
                    continue

                # Calcular insatisfacción del estudiante con este subconjunto (asignadas = len(comb))
                asignadas_cnt = len(comb)
                costo_ind = calcular_insatisfaccion_individual(s_len, asignadas_cnt)

                # Recursión para el siguiente estudiante con nuevos cupos (convertir a tupla)
                nuevos_cupos_t = tuple(nuevos_cupos)
                costo_rest = dp(idx_est + 1, nuevos_cupos_t)

                total_costo = costo_ind + costo_rest

                if total_costo < mejor_cost:
                    mejor_cost = total_costo
                    # Guardar la selección con códigos de materia para facilitar reconstrucción
                    mejor_subset = tuple(codigos[pos] for pos in comb)

        # Guardar decisión para reconstrucción
        decision[(idx_est, cupos_tuple)] = mejor_subset

        return mejor_cost

    # Ejecutar DP desde el primer estudiante y cupos iniciales
    costo_opt = dp(0, cupos_iniciales)

    # Reconstrucción de asignaciones por estudiante usando 'decision'
    asignaciones = {est['codigo']: [] for est in estudiantes_orden}
    idx = 0
    cupos_act = cupos_iniciales
    while idx < r:
        clave = (idx, cupos_act)
        subset = decision.get(clave, tuple())
        # Asignar las materias elegidas
        for cod_mat in subset:
            asignaciones[estudiantes_orden[idx]['codigo']].append(cod_mat)
            # decrementar cupo en cupos_act
            i_mat = idx_por_materia[cod_mat]
            cupos_act = list(cupos_act)
            cupos_act[i_mat] -= 1
            cupos_act = tuple(cupos_act)
        idx += 1

    # Salidas en formato requerido: costo total (insatisfacción promedio) y asignaciones por estudiante
    # Nota: la función de insatisfacción global ya es promedio por r en la definición original,
    # pero la dp acumuló sumatoria; si dp devolvió promedio por estudiante, no hay que dividir.
    # En la implementación dp suma f_j por cada estudiante, por lo que costo_opt ya es sumatoria.
    # Convertir a promedio:
    costo_promedio = costo_opt / r if r > 0 else 0.0

    # Imprimir resultados (formato simple)
    print("\n=== RESULTADOS PD (memoization) ===")
    print(f"Costo (promedio por estudiante): {costo_promedio}")
    for est in estudiantes_orden:
        codigo = est['codigo']
        asigns = asignaciones[codigo]
        print(f"{codigo},{len(asigns)}")
        for m in asigns:
            print(m)
    # Al final de la función rocPD justo antes de return

    print("\n=== RESULTADOS PD (memoization) ===")
    print(f"Insatisfacción general promedio: {costo_promedio}")

    for est in estudiantes_orden:
        codigo = est['codigo']
        asigns = asignaciones[codigo]
    print(f"Estudiante {codigo} pudo matricular {len(asigns)} materias: {asigns}")

    return asignaciones, costo_promedio


rocPD("Prueba1.txt")