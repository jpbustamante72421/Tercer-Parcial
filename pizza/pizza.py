import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

directorio_actual = os.path.dirname(os.path.abspath(__file__))
archivo = os.path.join(directorio_actual, "registros_pedido.txt")

precios_tam = {"Chica": 40, "Mediana": 80, "Grande": 120}
precios_ing = {"Jamón": 10, "Piña": 10, "Champiñones": 10}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pizzas - Piel Impresa")
        self.geometry("950x650")

        self.crear_cliente()
        self.crear_pedido()
        self.crear_tabla()
        self.crear_panel_ventas()
        
        # Cargar ventas al iniciar
        self.actualizar_panel_ventas()

    def crear_cliente(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="x")
        self.nombre = self.crear_input(frame, "Nombre", 0, 0)
        self.direccion = self.crear_input(frame, "Dirección", 0, 2)
        self.telefono = self.crear_input(frame, "Teléfono", 0, 4)

    def crear_input(self, frame, texto, fila, col):
        ctk.CTkLabel(frame, text=texto).grid(row=fila, column=col, padx=5, pady=5)
        entry = ctk.CTkEntry(frame, width=150)
        entry.grid(row=fila, column=col+1, padx=5)
        return entry

    def crear_pedido(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(frame, text="Tamaño").grid(row=0, column=0)
        self.tamano = tk.StringVar(value="Chica")
        for i, t in enumerate(precios_tam):
            ctk.CTkRadioButton(frame, text=t, variable=self.tamano, value=t).grid(row=1, column=i)

        ctk.CTkLabel(frame, text="Ingredientes").grid(row=0, column=3)
        self.vars_ing = {}
        for i, ing in enumerate(precios_ing):
            var = tk.BooleanVar()
            ctk.CTkCheckBox(frame, text=ing, variable=var).grid(row=1, column=3+i)
            self.vars_ing[ing] = var

        ctk.CTkLabel(frame, text="Cant.").grid(row=0, column=6)
        self.cantidad = ctk.CTkEntry(frame, width=50)
        self.cantidad.insert(0, "1")
        self.cantidad.grid(row=1, column=6)

        ctk.CTkButton(frame, text="Agregar", command=self.agregar).grid(row=1, column=7, padx=10)

    def crear_tabla(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.tabla = ttk.Treeview(frame, columns=("tam", "ing", "cant", "sub"), show="headings")
        self.tabla.heading("tam", text="Tamaño")
        self.tabla.heading("ing", text="Ingredientes")
        self.tabla.heading("cant", text="Pizzas")
        self.tabla.heading("sub", text="SubTotal")
        self.tabla.pack(side="left", fill="both", expand=True)

        botones = ctk.CTkFrame(self)
        botones.pack(pady=5)
        ctk.CTkButton(botones, text="Quitar", command=self.quitar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botones, text="TERMINAR Y GUARDAR", command=self.terminar).grid(row=0, column=1, padx=10)

    def crear_panel_ventas(self):
        self.panel = ctk.CTkFrame(self)
        self.panel.pack(padx=10, pady=10, fill="x")
        self.texto_ventas = ctk.CTkLabel(self.panel, text="", justify="left")
        self.texto_ventas.pack(pady=10)

    def agregar(self):
        tam = self.tamano.get()
        try:
            cant = int(self.cantidad.get())
        except:
            messagebox.showerror("Error", "Cantidad no válida")
            return

        ingredientes = [ing for ing, v in self.vars_ing.items() if v.get()]
        ing_txt = " + ".join(ingredientes) if ingredientes else "Sencilla"
        costo_ing = len(ingredientes) * 10
        subtotal = (precios_tam[tam] + costo_ing) * cant
        
        self.tabla.insert("", "end", values=(tam, ing_txt, cant, subtotal))

    def quitar(self):
        for s in self.tabla.selection():
            self.tabla.delete(s)

    def terminar(self):
        # 1. Validar que haya algo en la tabla
        items = self.tabla.get_children()
        if not items:
            messagebox.showwarning("Aviso", "No has agregado pizzas al pedido")
            return

        # 2. Validar que haya nombre
        nombre_cliente = self.nombre.get().strip()
        if not nombre_cliente:
            messagebox.showwarning("Aviso", "Debes poner el nombre del cliente")
            return

        # 3. PROCESO DE GUARDADO REFORZADO
        try:
            print(f"Intentando guardar en: {archivo}") # Debug en consola
            with open(archivo, "a", encoding="utf-8") as f:
                for item_id in items:
                    val = self.tabla.item(item_id)["values"]
                    # Formato: Nombre, Direccion, Teléfono, Tamaño, Ingredientes, Cantidad, Subtotal
                    linea = f"{nombre_cliente},{self.direccion.get()},{self.telefono.get()},{val[0]},{val[1]},{val[2]},{val[3]}\n"
                    f.write(linea)
                f.flush() # Fuerza la escritura en el disco
            
            messagebox.showinfo("Éxito", "Pedido guardado en " + archivo)
            self.limpiar_todo()
            self.actualizar_panel_ventas()
            
        except Exception as e:
            messagebox.showerror("Error Crítico", f"No se pudo escribir el archivo: {e}")

    def actualizar_panel_ventas(self):
        resumen = {}
        total_dia = 0
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split(",")
                    if len(partes) >= 7:
                        cliente = partes[0]
                        monto = float(partes[-1])
                        total_dia += monto
                        resumen[cliente] = resumen.get(cliente, 0) + monto
        
        txt = "VENTAS POR CLIENTE:\n" + "\n".join([f"- {k}: ${v}" for k, v in resumen.items()])
        txt += f"\n\nTOTAL GENERAL: ${total_dia}"
        self.texto_ventas.configure(text=txt)

    def limpiar_todo(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        self.nombre.delete(0, 'end')
        self.direccion.delete(0, 'end')
        self.telefono.delete(0, 'end')

if __name__ == "__main__":
    app = App()
    app.mainloop()