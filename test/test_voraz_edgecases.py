import os
import tempfile
import unittest
import math

from algoritmos.voraz import rocV


def write_input(content: str):
    tf = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt")
    tf.write(content)
    tf.close()
    return tf.name


class TestVorazEdgeCases(unittest.TestCase):

    def test_student_without_requests(self):
        # 1 materia, 1 estudiante, estudiante con 0 solicitudes
        content = """1
M1,1
1
S1,0
"""
        path = write_input(content)
        try:
            asignaciones, costo = rocV(path)
            self.assertIn('S1', asignaciones)
            self.assertEqual(asignaciones['S1'], [])
            self.assertEqual(costo, 0)
        finally:
            os.remove(path)

    def test_request_to_nonexistent_subject(self):
        # materia M1 existe, student requests M2 which doesn't exist
        content = """1
M1,1
1
S1,1
M2,5
"""
        path = write_input(content)
        try:
            asignaciones, costo = rocV(path)
            self.assertIn('S1', asignaciones)
            self.assertEqual(asignaciones['S1'], [])
            # cálculo manual: msj_size=1, maj_size=0, no_asignadas=[5]
            # gamma = 3*1-1 = 2 -> factor2 = 5/2 = 2.5, factor1 = 1 -> fj = 2.5
            self.assertTrue(math.isclose(costo, 2.5, rel_tol=1e-9))
        finally:
            os.remove(path)

    def test_multiple_students_competing(self):
        # una materia M1 con 1 cupo, dos estudiantes S1 (prioridad 10) y S2 (prioridad 5)
        content = """1
M1,1
2
S1,1
M1,10
S2,1
M1,5
"""
        path = write_input(content)
        try:
            asignaciones, costo = rocV(path)
            # S1 should get the cupo
            self.assertIn('S1', asignaciones)
            self.assertIn('S2', asignaciones)
            self.assertEqual(asignaciones['S1'], [('M1', 10)])
            self.assertEqual(asignaciones['S2'], [])
            # costo esperado: S1 fj=0, S2 fj=2.5 -> promedio 1.25
            self.assertTrue(math.isclose(costo, 1.25, rel_tol=1e-9))
        finally:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
