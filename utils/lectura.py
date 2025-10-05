def leer_entrada(archivo_entrada: str):
    """
    Lee el archivo de entrada y retorna:
    - materias: dict con código -> cupo
    - estudiantes: lista con cada estudiante y sus solicitudes
    """
    with open(archivo_entrada, "r") as f:
        lineas = [line.strip() for line in f.readlines()]


    k = int(lineas[0])  # número de materias
    materias = {}
    idx = 1
    for _ in range(k):
        codigo, cupo = lineas[idx].split(",")
        materias[codigo] = int(cupo)
        idx += 1

    r = int(lineas[idx])  # número de estudiantes
    idx += 1

    estudiantes = []
    for _ in range(r):
        codigo, s = lineas[idx].split(",")
        idx += 1
        s = int(s)
        materias_solicitadas = []
        for _ in range(s):
            m, p = lineas[idx].split(",")
            materias_solicitadas.append((m, int(p)))
            idx += 1
        estudiantes.append({
            "codigo": codigo,
            "materias": materias_solicitadas
        })

    return materias, estudiantes
