import os
import tempfile
import unittest
import random

from algoritmos.voraz import rocV


def write_input(content: str):
    tf = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt")
    tf.write(content)
    tf.close()
    return tf.name


class TestVorazAdditional(unittest.TestCase):

    def test_tie_on_priority(self):
        # M1 has 1 cupo, S1 and S2 request M1 with same priority
        content = """1
M1,1
2
S1,1
M1,10
S2,1
M1,10
"""
        path = write_input(content)
        try:
            asignaciones, costo = rocV(path)
            # tie-breaker: sorted by (-priority, codigo) so 'S1' < 'S2' -> S1 wins
            self.assertEqual(asignaciones['S1'], [('M1', 10)])
            self.assertEqual(asignaciones['S2'], [])
        finally:
            os.remove(path)

    def test_large_deterministic_consistency(self):
        random.seed(42)
        K = 10  # materias
        R = 50  # estudiantes

        # generate materias with capacities 1..5
        materias = [(f'M{i+1}', random.randint(1, 5)) for i in range(K)]

        # generate students with 1..5 requests chosen among materias
        estudiantes = []
        for i in range(R):
            codigo = f'S{i+1}'
            s = random.randint(1, 5)
            picks = random.sample([m for m, _ in materias], s)
            estudiantes.append((codigo, picks))

        # build content string
        lines = []
        lines.append(str(K))
        for m, c in materias:
            lines.append(f"{m},{c}")
        lines.append(str(R))
        for codigo, picks in estudiantes:
            lines.append(f"{codigo},{len(picks)}")
            for m in picks:
                # deterministic priority between 1 and 10
                p = random.randint(1, 10)
                lines.append(f"{m},{p}")

        content = "\n".join(lines) + "\n"
        path = write_input(content)
        try:
            # keep original capacities map for checks
            orig_caps = {m: c for m, c in materias}
            asignaciones, costo = rocV(path)

            # Check: no materia assigned more than its original capacity
            assigned_counts = {m: 0 for m, _ in materias}
            for estudiante, asigns in asignaciones.items():
                for m, p in asigns:
                    self.assertIn(m, assigned_counts)
                    assigned_counts[m] += 1

            for m, cnt in assigned_counts.items():
                self.assertLessEqual(cnt, orig_caps[m])

            # Check: every assigned materia was requested by that student in the input
            # Re-read input to a map of requests
            requests = {}
            with open(path, 'r', encoding='utf-8') as f:
                data = [ln.strip() for ln in f.readlines()]
            idx = 0
            k = int(data[idx]); idx += 1
            idx += k
            r = int(data[idx]); idx += 1
            for _ in range(r):
                codigo, s = data[idx].split(','); idx += 1
                s = int(s)
                reqs = []
                for _ in range(s):
                    m, p = data[idx].split(','); idx += 1
                    reqs.append(m)
                requests[codigo] = reqs

            for estudiante, asigns in asignaciones.items():
                for m, _ in asigns:
                    self.assertIn(m, requests[estudiante])

        finally:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
