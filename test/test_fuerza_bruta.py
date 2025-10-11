import unittest
import math

from algoritmos.fuerza_bruta import rocFB


class TestFuerzaBrutaPrueba1(unittest.TestCase):
    def test_rocFB_prueba1_optimal(self):
        # Ejecuta fuerza bruta sobre la instancia de prueba 1
        asignaciones, costo = rocFB('pruebas/Prueba1.txt')

        # Estructuras mínimas
        self.assertIsInstance(asignaciones, dict)
        self.assertIsInstance(costo, float)

        # El costo óptimo conocido aproximado para esta instancia es ~0.176667
        self.assertTrue(math.isclose(costo, 0.17666666666666667, rel_tol=1e-6), f"Costo esperado ~0.176667, obtenido {costo}")


if __name__ == '__main__':
    unittest.main()
