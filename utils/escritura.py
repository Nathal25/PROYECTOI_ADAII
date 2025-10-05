def escribir_salida(nombre_archivo: str, asignaciones: dict, costo: float):
    """
    Escribe la salida del problema en un archivo de texto con el formato solicitado.

    :param nombre_archivo: Ruta del archivo de salida
    :param asignaciones: dict con clave = código de estudiante,
                         valor = lista de tuplas (materia, prioridad)
    :param costo: costo de la solución (F<M,E>(A))
    """
    with open(nombre_archivo, "w") as f:
        # Primera línea: costo
        f.write(f"{costo:.6f}\n")

        # Por cada estudiante en orden
        for estudiante in sorted(asignaciones.keys()):
            materias_asignadas = asignaciones[estudiante]
            f.write(f"{estudiante},{len(materias_asignadas)}\n")

            for materia, _ in materias_asignadas:
                f.write(f"{materia}\n")
