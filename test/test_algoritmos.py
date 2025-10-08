import os
import unittest
from algoritmos.voraz import rocV
from utils.escritura import escribir_salida

class TestIntegracionVoraz(unittest.TestCase):

    def test_voraz_integration(self):
        entrada = "pruebas/Prueba1.txt"          # archivo de entrada
        salida = "Resultados/Resultado_test.txt"    # archivo de salida temporal

        # Ejecutar el algoritmo voraz
        asignaciones, costo = rocV(entrada)

        # Escribir la salida en archivo (la función devuelve la ruta final usada)
        salida_generada = escribir_salida(salida, asignaciones, costo)

        # Verificar que el archivo se haya creado (usar la ruta devuelta)
        self.assertTrue(os.path.exists(salida_generada))

        # Leer contenido del archivo de salida
        with open(salida_generada, "r", encoding="utf-8") as f:
            lineas = [line.strip() for line in f.readlines()]

        # 1) La primera línea debe ser el costo
        try:
            float(lineas[0])
        except ValueError:
            self.fail("La primera línea de salida no es un número válido de costo.")

        # 2) Verificar que cada bloque de estudiante tenga consistencia
        i = 1
        while i < len(lineas):
            if "," not in lineas[i]:
                self.fail(f"Línea inesperada en salida: {lineas[i]}")

            estudiante, num = lineas[i].split(",")
            num = int(num)

            # Deben venir 'num' líneas con materias después de esta
            materias = lineas[i+1:i+1+num]
            self.assertEqual(len(materias), num, f"El estudiante {estudiante} no tiene el número correcto de materias.")

            i += 1 + num  # saltar al siguiente estudiante

        # Limpieza (opcional)
        if os.path.exists(salida_generada):
            os.remove(salida_generada)

if __name__ == "__main__":
    unittest.main()
