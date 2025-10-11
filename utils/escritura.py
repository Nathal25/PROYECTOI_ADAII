import os


def escribir_salida(nombre_archivo: str, asignaciones: dict, costo: float, carpeta_salida: str = None):
    """
    Escribe la salida del problema en un archivo de texto con el formato solicitado.

    :param nombre_archivo: Ruta del archivo de salida
    :param asignaciones: dict con clave = código de estudiante,
                         valor = lista de tuplas (materia, prioridad)
    :param costo: costo de la solución (F<M,E>(A))
    """
    # Si se pasa carpeta_salida explícita, usarla
    if carpeta_salida:
        os.makedirs(carpeta_salida, exist_ok=True)
        nombre_archivo = os.path.join(carpeta_salida, nombre_archivo)
    else:
        # Si pasan sólo un basename y existe una carpeta 'Resultados' en el repo, usarla por defecto
        # Evitar crear 'Resultados/Resultados/..' si el nombre ya apunta dentro de Resultados
        if not os.path.isabs(nombre_archivo) and os.path.isdir("Resultados"):
            # si el usuario ya pasó 'Resultados/archivo' o 'Resultados\\archivo', no lo preponemos
            normalized = os.path.normpath(nombre_archivo)
            if not (normalized.startswith("Resultados") or normalized.startswith(os.path.join("..", "Resultados"))):
                nombre_archivo = os.path.join("Resultados", nombre_archivo)

    # Asegurarse de que el directorio destino exista
    parent_dir = os.path.dirname(nombre_archivo)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    # Devolver una ruta absoluta para evitar ambigüedades
    nombre_archivo = os.path.abspath(nombre_archivo)

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        # Primera línea: costo
        f.write(f"{costo:.6f}\n")

        # Por cada estudiante en orden
        for estudiante in sorted(asignaciones.keys()):
            materias_asignadas = asignaciones[estudiante]
            f.write(f"{estudiante},{len(materias_asignadas)}\n")

            for entry in materias_asignadas:
                # soportar dos formatos:
                # - [(materia, prioridad), ...]
                # - ['materia', 'materia', ...]
                if isinstance(entry, (list, tuple)) and len(entry) >= 1:
                    materia = entry[0]
                else:
                    materia = entry
                f.write(f"{materia}\n")
    return nombre_archivo
