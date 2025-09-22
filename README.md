# Repartición Óptima de Cupos

## Objetivo

El propósito de este proyecto es aplicar diferentes técnicas de diseño de algoritmos (fuerza bruta, voraz y programación dinámica) para solucionar un problema de asignación combinatoria: la repartición óptima de cupos en materias universitarias, minimizando la insatisfacción general de los estudiantes. Los resultados permiten comparar la eficiencia y optimalidad de cada enfoque, reconociendo ventajas y desventajas prácticas de estos algoritmos en el contexto del problema propuesto.

## Descripción de Archivos

- **`main.py`**: Punto de entrada del proyecto desde el cual se elige el algoritmo, se cargan los datos de entrada y se generan los resultados.

- **`algoritmos/fuerza_bruta.py`**, **`algoritmos/voraz.py`**, **`algoritmos/prog_dinamica.py`**: Implementan las funciones principales `rocFB`, `rocV` y `rocPD` (fuerza bruta, voraz, y programación dinámica) respectivamente.

- **`utils/lectura.py`**: Funciones para la lectura y validación del archivo de entrada.

- **`utils/escritura.py`**: Funciones para la generación del archivo de salida.

- **`entrada.txt`**: Archivo de entrada que debe seguir el formato especificado en el enunciado.

- **`salida.txt`**: Archivo de salida que se genera automáticamente tras la ejecución.

- **`tests/`**: Carpeta opcional con pruebas automáticas de los algoritmos (si aplica).

- **`README.md`**: Este archivo, con las instrucciones de uso y la descripción de contenidos.

## Instrucciones de Ejecución

1. Verificar que el archivo `entrada.txt` contiene los datos de entrada con el formato solicitado.

2. Ejecutar `main.py` indicando el algoritmo deseado.

3. El resultado se guardará automáticamente en `salida.txt`, respetando el formato de salida requerido.

4. Consultar este README para detalles sobre la estructura de archivos y el objetivo general.

## Créditos

- **Autores**: Nathalia Ortiz Granada 202372231, Nicole Narvaez Medina 202156947 
- **Profesor**: Jesús Alexander Aranda
- **Monitor**: Mauricio Muñoz
- **Curso**: Análisis de Algoritmos II, septiembre de 2025