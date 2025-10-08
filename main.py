import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from algoritmos.voraz import rocV
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
        btn_cargar = tk.Button(frame_top, text="Cargar archivo", command=self.cargar_archivo)
        btn_cargar.pack(side=tk.LEFT, padx=5)

        # Selección de algoritmo
        tk.Label(frame_top, text="Algoritmo:").pack(side=tk.LEFT, padx=5)
        self.algoritmo_var = tk.StringVar()
        self.combo_algoritmo = ttk.Combobox(
            frame_top, textvariable=self.algoritmo_var,
            values=["Greedy (Voraz)", "Fuerza Bruta", "Programación Dinámica"],
            state="readonly", width=25
        )
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.pack(side=tk.LEFT, padx=5)

        # Botón ejecutar
        btn_ejecutar = tk.Button(frame_top, text="Ejecutar", command=self.ejecutar_algoritmo)
        btn_ejecutar.pack(side=tk.LEFT, padx=5)

        # ---- Vista horizontal ----
        frame_main = tk.Frame(root)
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Entrada
        frame_entrada = tk.LabelFrame(frame_main, text="Entrada del problema")
        frame_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.txt_entrada = tk.Text(frame_entrada, wrap=tk.WORD)
        self.txt_entrada.pack(fill=tk.BOTH, expand=True)

        # Salida
        frame_salida = tk.LabelFrame(frame_main, text="Salida del problema")
        frame_salida.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

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

        try:
            if algoritmo == "Greedy (Voraz)":
                asignaciones, costo = rocV(self.ruta_archivo)

                # Crear nombre de salida y guardarlo en la carpeta 'Resultados'
                nombre_salida = "Resultado_" + os.path.basename(self.ruta_archivo)
                ruta_generada = escribir_salida(nombre_salida, asignaciones, costo, carpeta_salida="Resultados")

                self.txt_salida.insert(tk.END, f"✅ Algoritmo voraz ejecutado correctamente.\n\n")
                self.txt_salida.insert(tk.END, f"Archivo de salida: {ruta_generada}\n")
                self.txt_salida.insert(tk.END, f"Costo total: {costo:.6f}\n\n")
                self.txt_salida.insert(tk.END, "Asignaciones:\n")
                for est, mat in asignaciones.items():
                    self.txt_salida.insert(tk.END, f"  {est} -> {mat}\n")

            elif algoritmo == "Fuerza Bruta":
                self.txt_salida.insert(tk.END, ">> Implementación pendiente de fuerza bruta.\n")

            elif algoritmo == "Programación Dinámica":
                self.txt_salida.insert(tk.END, ">> Implementación pendiente de programación dinámica.\n")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al ejecutar el algoritmo:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProyectoADAApp(root)
    root.mainloop()
