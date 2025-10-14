import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from algoritmos.voraz import rocV
from algoritmos.fuerza_bruta import rocFB
from algoritmos.prog_dinamica import rocPD
from utils.escritura import escribir_salida
import os

class ProyectoADAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto ADA - Asignación de Materias")
        self.root.geometry("700x500")

        # ---- Frame superior con controles ----
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack(side=tk.TOP, fill=tk.X)

        # Botón cargar archivo
        self.btn_cargar = tk.Button(frame_top, text="Cargar archivo", command=self.cargar_archivo)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        # Selección de algoritmo
        tk.Label(frame_top, text="Algoritmo:").pack(side=tk.LEFT, padx=5)
        self.algoritmo_var = tk.StringVar()
        self.combo_algoritmo = ttk.Combobox(
            frame_top, textvariable=self.algoritmo_var,
            values=["Programación Voraz", "Fuerza Bruta", "Programación Dinámica"],
            state="readonly", width=25
        )
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.pack(side=tk.LEFT, padx=5)

    # Nota: la búsqueda local y el número de iteraciones se ejecutan siempre
    # por defecto en `rocV` (parámetros hardcodeados en el algoritmo).

        # Botón ejecutar
        self.btn_ejecutar = tk.Button(frame_top, text="Ejecutar", command=self.ejecutar_algoritmo)
        self.btn_ejecutar.pack(side=tk.LEFT, padx=5)

        # ---- Vista horizontal ----
        frame_main = tk.Frame(root)
        frame_main.pack(fill=tk.BOTH, expand=True)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=1)
        frame_main.rowconfigure(0, weight=1)

        # Entrada
        frame_entrada = tk.LabelFrame(frame_main, text="Entrada del problema")
        frame_entrada.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.txt_entrada = tk.Text(frame_entrada, wrap=tk.WORD)
        self.txt_entrada.pack(fill=tk.BOTH, expand=True)

        # Salida
        frame_salida = tk.LabelFrame(frame_main, text="Salida del problema")
        frame_salida.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.txt_salida = tk.Text(frame_salida, wrap=tk.WORD, bg="#f4f4f4")
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

        # Archivo cargado
        self.ruta_archivo = None

    def cargar_archivo(self):
        filetypes = [("Archivos de texto", "*.txt *.csv"), ("Todos", "*.*")]
        ruta = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=filetypes)
        if ruta:
            self.ruta_archivo = ruta
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.txt_entrada.delete(1.0, tk.END)
                self.txt_entrada.insert(tk.END, contenido)
                self.txt_salida.delete(1.0, tk.END)
                self.txt_salida.insert(tk.END, f"Archivo cargado: {ruta}\n")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def ejecutar_algoritmo(self):
        if not self.ruta_archivo:
            messagebox.showwarning("Advertencia", "Primero carga un archivo.")
            return
        algoritmo = self.algoritmo_var.get()
        self.txt_salida.delete(1.0, tk.END)

        # Deshabilitar controles mientras se ejecuta
        self.btn_cargar.config(state=tk.DISABLED)
        self.btn_ejecutar.config(state=tk.DISABLED)
        self.combo_algoritmo.config(state=tk.DISABLED)

        import time

        def worker():
            try:
                start = time.perf_counter()
                # Ejecutar el algoritmo seleccionado y capturar el resultado
                result = None
                if algoritmo == "Greedy (Voraz)":
                    # Llamar a rocV con los valores por defecto: siempre usa búsqueda local ligera
                    result = rocV(self.ruta_archivo)
                    nombre_salida = "Resultado_V_" + os.path.basename(self.ruta_archivo)
                elif algoritmo == "Fuerza Bruta":
                    result = rocFB(self.ruta_archivo)
                    nombre_salida = "Resultado_FB_" + os.path.basename(self.ruta_archivo)
                elif algoritmo == "Programación Dinámica":
                    result = rocPD(self.ruta_archivo)
                    nombre_salida = "Resultado_PD_" + os.path.basename(self.ruta_archivo)
                else:
                    raise RuntimeError("Algoritmo desconocido")
                elapsed = time.perf_counter() - start

                # Normalizar la salida: preferimos (asignaciones_dict, costo_float)
                asignaciones = None
                costo = None
                # Si devuelve tupla/iterable con >=2 elementos, tomamos los dos primeros
                if isinstance(result, tuple) or isinstance(result, list):
                    if len(result) >= 2:
                        asignaciones, costo = result[0], result[1]
                    elif len(result) == 1:
                        asignaciones = result[0]
                        costo = None
                    else:
                        asignaciones = {}
                        costo = None
                elif isinstance(result, dict):
                    asignaciones = result
                    costo = None
                else:
                    # Valor inesperado: convertir a representación segura y lanzar
                    raise RuntimeError(f"Resultado inesperado del algoritmo: {type(result)} -> {repr(result)[:200]}")

                # Asegurar que `asignaciones` sea un dict para el UI
                if not isinstance(asignaciones, dict):
                    try:
                        # intentar convertir secuencias indexadas en dict por orden de estudiantes
                        asignaciones = dict(asignaciones)
                    except Exception:
                        asignaciones = {}

                # Para escribir salida, si costo es None escribimos 0.0 y señalamos desconocido en UI
                costo_para_escribir = costo if isinstance(costo, (int, float)) else 0.0

                ruta_generada = escribir_salida(nombre_salida, asignaciones, costo_para_escribir, carpeta_salida="Resultados")

                # Programar la actualización de UI en el hilo principal
                def on_done():
                    self.txt_salida.insert(tk.END, f"✅ Algoritmo {algoritmo} ejecutado correctamente.\n\n")
                    self.txt_salida.insert(tk.END, f"Archivo de salida: {ruta_generada}\n")
                    # Mostrar costo formateado si está disponible
                    if isinstance(costo, (int, float)):
                        self.txt_salida.insert(tk.END, f"Costo total: {costo:.6f}\n")
                    else:
                        self.txt_salida.insert(tk.END, f"Costo total: Desconocido\n")
                    self.txt_salida.insert(tk.END, f"Tiempo de ejecución: {elapsed:.3f} s\n\n")
                    self.txt_salida.insert(tk.END, "Asignaciones:\n")
                    # asignaciones is expected to be dict {est: list}
                    for est, mat in asignaciones.items():
                        self.txt_salida.insert(tk.END, f"  {est} -> {mat}\n")

                    # re-enable controls
                    self.btn_cargar.config(state=tk.NORMAL)
                    self.btn_ejecutar.config(state=tk.NORMAL)
                    self.combo_algoritmo.config(state="readonly")

                self.root.after(0, on_done)

            except Exception as e:
                # Capture the exception into a local name so the scheduled callback
                # doesn't reference the exception variable after the except block
                # has exited (which can cause a NameError in tkinter callbacks).
                err = e
                def on_error(err=err):
                    messagebox.showerror("Error", f"Ocurrió un problema al ejecutar el algoritmo:\n{err}")
                    self.btn_cargar.config(state=tk.NORMAL)
                    self.btn_ejecutar.config(state=tk.NORMAL)
                    self.combo_algoritmo.config(state="readonly")
                self.root.after(0, on_error)

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProyectoADAApp(root)
    root.mainloop()
