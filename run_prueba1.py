from algoritmos.voraz import rocV

path = "pruebas/Prueba1.txt"

print("Archivo de entrada:", path)

asig_greedy, cost_greedy = rocV(path, use_local_search=False)
print("\n=== Resultado voraz (sin búsqueda local) ===")
print(f"Costo: {cost_greedy:.6f}")
for estudiante in sorted(asig_greedy.keys()):
    print(f"{estudiante}: {asig_greedy[estudiante]}")

asig_local, cost_local = rocV(path, use_local_search=True, max_iter=500)
print("\n=== Resultado con búsqueda local ===")
print(f"Costo: {cost_local:.6f}")
for estudiante in sorted(asig_local.keys()):
    print(f"{estudiante}: {asig_local[estudiante]}")

impr = cost_greedy - cost_local
pct = (impr / cost_greedy * 100) if cost_greedy != 0 else 0
print(f"\nMejora absoluta: {impr:.6f}")
print(f"Mejora relativa: {pct:.2f}%")
