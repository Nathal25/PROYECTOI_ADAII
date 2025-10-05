from algoritmos.voraz import rocV
from utils.escritura import escribir_salida

if __name__ == "__main__":
    entrada = "Prueba4.txt"
    salida = "Resultado4.txt"

    asignaciones, costo = rocV(entrada)
    escribir_salida(salida, asignaciones, costo)

    print(f"Solución escrita en {salida} con costo {costo:.6f}")
    
