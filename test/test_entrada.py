from utils.lectura import leer_entrada  

materias, estudiantes = leer_entrada("Prueba1.txt")

print("Materias:")
print(materias)
print("\nEstudiantes:")
for est in estudiantes:
    print(est)
