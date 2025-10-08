from utils.lectura import leer_entrada
import random


def rocV(archivo_entrada: str, use_local_search: bool = False, max_iter: int = 1000):
    """
    Algoritmo voraz para la asignación de materias.
    Compatible con la salida de `leer_entrada` (estudiantes: lista de dicts
    con keys "codigo" y "materias" donde "materias" es lista de (m, p)).

    Retorna:
      - asignaciones: dict {codigo_estudiante: [(materia, prioridad), ...]}
      - F: insatisfacción promedio (usar calcular_insatisfaccion)
    """

    # 1. Leer datos
    materias, estudiantes = leer_entrada(archivo_entrada)

    # 2. Inicializar asignaciones por código de estudiante
    asignaciones = {e["codigo"]: [] for e in estudiantes}

    # 3. Construir lista de solicitudes (prioridad, codigo, materia)
    solicitudes = []
    for e in estudiantes:
        codigo = e["codigo"]
        for (m, p) in e["materias"]:
            solicitudes.append((p, codigo, m))

    # 4. Ordenar solicitudes por prioridad descendente, desempate por código
    solicitudes.sort(key=lambda x: (-x[0], x[1]))

    # 5. Copia de cupos y asignación voraz
    cupos = materias.copy()
    for p, codigo, m in solicitudes:
        # usar get para evitar KeyError si la materia no existe en la entrada
        if cupos.get(m, 0) > 0 and not any(m == m_asig for (m_asig, _) in asignaciones[codigo]):
            asignaciones[codigo].append((m, p))
            cupos[m] = cupos.get(m, 0) - 1

    # 6. Opcional: mejora por búsqueda local (swap y relocate).
    # Por defecto stay voraz (use_local_search=False). Pasa use_local_search=True
    # si quieres ejecutar la fase de búsqueda local.
    if use_local_search:
        asignaciones = busqueda_local(asignaciones, materias, estudiantes, max_iter=max_iter)

    # 7. Calcular costo/insatisfacción usando la función auxiliar
    costo = calcular_insatisfaccion(estudiantes, asignaciones)

    return asignaciones, costo


def busqueda_local(asignaciones, materias, estudiantes, max_iter=1000):
    """
    Mejora la solución inicial mediante búsqueda local simple.
    - intentos de swap: intercambiar una materia entre dos estudiantes si ambos la
      habían solicitado y reduce el costo global.
    - intentos de relocate: mover una materia asignada de A a B si B la solicitó y
      la operación reduce el costo.

    Parámetros:
      asignaciones: dict {codigo: [(materia, prioridad), ...]}
      materias: dict {materia: capacidad}
      estudiantes: lista de dicts con 'codigo' y 'materias'
    Devuelve la asignación mejorada (posible la misma si no hay mejora).
    """
    # Mapear estudiante -> set de materias solicitadas y prioritades
    solicitudes_map = {e['codigo']: {m for (m, _) in e['materias']} for e in estudiantes}

    # helper para calcular costo usando la función existente
    def costo_actual(asigs):
        return calcular_insatisfaccion(estudiantes, asigs)

    # transformar asignaciones a forma mutable (listas) -- ya lo están
    current = {k: list(v) for k, v in asignaciones.items()}

    best_cost = costo_actual(current)
    improved = True
    it = 0

    student_codes = list(current.keys())
    while it < max_iter and improved:
        improved = False
        it += 1

        # Randomize order to escape local minima deterministically
        random.shuffle(student_codes)

        # Try swaps between pairs
        for i in range(len(student_codes)):
            a = student_codes[i]
            if not current[a]:
                continue
            for j in range(i+1, len(student_codes)):
                b = student_codes[j]
                if not current[b]:
                    continue

                # try all pairwise swaps of one assigned materia
                for idx_a, (ma, pa) in enumerate(current[a]):
                    for idx_b, (mb, pb) in enumerate(current[b]):
                        # only consider swap if each student requested the other's materia
                        if (mb in solicitudes_map[a]) and (ma in solicitudes_map[b]):
                            # apply swap
                            new_asigs = {k: list(v) for k, v in current.items()}
                            new_asigs[a][idx_a] = (mb, pb)
                            new_asigs[b][idx_b] = (ma, pa)
                            new_cost = costo_actual(new_asigs)
                            if new_cost + 1e-12 < best_cost:
                                current = new_asigs
                                best_cost = new_cost
                                improved = True
                                break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break

        if improved:
            # continue to next iteration looking for further improvements
            continue

        # Try relocates: move an assigned materia from a to b (if b requested and doesn't have it)
        for a in student_codes:
            if not current[a]:
                continue
            for idx_a, (ma, pa) in enumerate(list(current[a])):
                # find candidate b who requested ma and doesn't have it
                for b in student_codes:
                    if b == a:
                        continue
                    if ma in solicitudes_map[b] and not any(ma == m_as for (m_as, _) in current[b]):
                        new_asigs = {k: list(v) for k, v in current.items()}
                        # remove from a
                        del new_asigs[a][idx_a]
                        # add to b with original priority pa
                        new_asigs[b].append((ma, pa))
                        new_cost = costo_actual(new_asigs)
                        if new_cost + 1e-12 < best_cost:
                            current = new_asigs
                            best_cost = new_cost
                            improved = True
                            break
                if improved:
                    break
            if improved:
                break

    return current


def calcular_insatisfaccion(estudiantes, asignaciones):
    """
    Calcula el valor F<M,E>(A) de insatisfacción general.
    """
    total = 0
    estudiantes_con_solicitudes = 0
    for e in estudiantes:
        codigo = e["codigo"]
        msj = e["materias"]
        maj = asignaciones.get(codigo, [])

        # tamaños
        msj_size = len(msj)
        maj_size = len(maj)

        if msj_size == 0:
            continue

        estudiantes_con_solicitudes += 1

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

    # Evitar división por cero
    if estudiantes_con_solicitudes == 0:
        return 0
    return total / estudiantes_con_solicitudes
