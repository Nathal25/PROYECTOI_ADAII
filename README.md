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

### Ejecutar la aplicación (GUI)

Requisitos básicos:

- Python 3.8+ (el proyecto se probó con Python 3.13). En Windows suele incluirse la librería `tkinter` necesaria para la interfaz.

Paso a paso (PowerShell):

1. (Opcional) Crear y activar un entorno virtual recomendado:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Instale las dependencias de requirements.txt:

```powershell
pip install -r requirements.txt
```

3. Ejecutar la aplicación (abrirá una ventana gráfica basada en tkinter):

```powershell
python main.py
```

4. Usar la interfaz para cargar el archivo de entrada (por ejemplo `pruebas/Prueba1.txt`) y ejecutar el algoritmo deseado. El programa escribirá el archivo de salida (`salida.txt`) y mostrará el tiempo de ejecución en la ventana.

### Ejecutar pruebas automáticas

Para ejecutar la suite de tests con unittest (desde la raíz del proyecto):

```powershell
python -m unittest discover -s test -p "test_*.py" -v
```

Notas:

- Si su instalación de Python no incluye `tkinter`, deberá instalarlo o usar una versión de Python que lo incluya (en Windows suele venir por defecto).
- Los comandos anteriores están pensados para PowerShell en Windows; en otras shells (bash, cmd) la sintaxis para activar el virtualenv puede cambiar.


## Créditos

- **Autores**: Nathalia Ortiz Granada 202372231, Nicole Narvaez Medina 202156947 
- **Profesor**: Jesús Alexander Aranda
- **Monitor**: Mauricio Muñoz
- **Curso**: Análisis de Algoritmos II, septiembre de 2025