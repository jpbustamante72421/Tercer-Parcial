import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
#precios
precios_tamano = {
    "Chica": 40,
    "Mediana": 80,
    "Grande": 120
}

precios_ingredientes = {
    "Jamón": 10,
    "Piña": 10,
    "Champiñones": 10
}

archivo = "registros_pedido.txt"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pizzas")
        self.geometry("850x550")

        self.total = 0

        # datos 
        frame1 = ctk.CTkFrame(self)
        frame1.pack(padx=10, pady=10)

        ctk.CTkLabel(frame1, text="Nombre").grid(row=0, column=0)
        self.nombre = ctk.CTkEntry(frame1)
        self.nombre.grid(row=0, column=1)

        ctk.CTkLabel(frame1, text="Dirección").grid(row=0, column=2)
        self.direccion = ctk.CTkEntry(frame1)
        self.direccion.grid(row=0, column=3)

        ctk.CTkLabel(frame1, text="Teléfono").grid(row=1, column=0)
        self.telefono = ctk.CTkEntry(frame1)
        self.telefono.grid(row=1, column=1)

        ctk.CTkLabel(frame1, text="Fecha").grid(row=1, column=2)
        self.fecha = ctk.CTkEntry(frame1)
        self.fecha.grid(row=1, column=3)

        # -------- PEDIDO --------
        frame2 = ctk.CTkFrame(self)
        frame2.pack(padx=10, pady=10)

        ctk.CTkLabel(frame2, text="Tamaño").grid(row=0, column=0)
        self.tamano = ctk.CTkComboBox(frame2, values=["Chica", "Mediana", "Grande"])
        self.tamano.grid(row=0, column=1)

        ctk.CTkLabel(frame2, text="Ingredientes").grid(row=0, column=2)

        self.vars_ing = {}
        col = 3
        for ing in precios_ingredientes:
            var = tk.BooleanVar()
            ctk.CTkCheckBox(frame2, text=ing, variable=var).grid(row=0, column=col)
            self.vars_ing[ing] = var
            col += 1

        ctk.CTkLabel(frame2, text="Cant").grid(row=0, column=col)
        self.cantidad = ctk.CTkEntry(frame2, width=60)
        self.cantidad.grid(row=0, column=col+1)

        # botones
        ctk.CTkButton(frame2, text="Agregar", command=self.agregar).grid(row=1, column=1)
        ctk.CTkButton(frame2, text="Quitar", command=self.quitar).grid(row=1, column=2)
        ctk.CTkButton(frame2, text="Terminar", command=self.terminar).grid(row=1, column=3)
        ctk.CTkButton(frame2, text="Ver ventas", command=self.ver_ventas).grid(row=1, column=4)

        # -------- TABLA --------
        self.tabla = ttk.Treeview(self, columns=("tam","ing","cant","sub"), show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla.heading("tam", text="Tamaño")
        self.tabla.heading("ing", text="Ingredientes")
        self.tabla.heading("cant", text="Cantidad")
        self.tabla.heading("sub", text="Subtotal")

        self.total_label = ctk.CTkLabel(self, text="Total: $0")
        self.total_label.pack()

# agregar seccion
    def agregar(self):
        tam = self.tamano.get()

        if tam not in precios_tamano:
            messagebox.showerror("Error", "Escoge tamaño")
            return

        try:
            cant = int(self.cantidad.get())
        except:
            messagebox.showerror("Error", "Cantidad mal")
            return

        ingredientes = []
        extra = 0

        for ing, var in self.vars_ing.items():
            if var.get():
                ingredientes.append(ing)
                extra += precios_ingredientes[ing]

        subtotal = (precios_tamano[tam] + extra) * cant
        self.total += subtotal

        self.tabla.insert("", "end", values=(tam, ", ".join(ingredientes), cant, subtotal))
        self.total_label.configure(text=f"Total: ${self.total}")

        self.cantidad.delete(0, "end")

    #  quitar seleccion
    def quitar(self):
        sel = self.tabla.selection()
        if not sel:
            return

        datos = self.tabla.item(sel)["values"]
        self.total -= int(datos[3])

        self.tabla.delete(sel)
        self.total_label.configure(text=f"Total: ${self.total}")

    # -pagar
    def terminar(self):
        if self.total == 0:
            return

        with open(archivo, "a") as f:
            for item in self.tabla.get_children():
                d = self.tabla.item(item)["values"]
                f.write(f"{self.nombre.get()},{self.direccion.get()},{self.telefono.get()},{self.fecha.get()},{d[0]},{d[1]},{d[2]},{d[3]}\n")

        messagebox.showinfo("Pago", f"Total: ${self.total}")

        self.total = 0
        self.total_label.configure(text="Total: $0")

        for item in self.tabla.get_children():
            self.tabla.delete(item)

    # ventana de las ventas
    def ver_ventas(self):
        v = tk.Toplevel(self)
        v.title("Ventas")

        tabla = ttk.Treeview(v, columns=("a","b","c","d","e","f","g","h"), show="headings")
        tabla.pack(fill="both", expand=True)

        nombres = ["Nombre","Dirección","Tel","Fecha","Tamaño","Ingredientes","Cant","Sub"]

        for col, nom in zip(tabla["columns"], nombres):
            tabla.heading(col, text=nom)

        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                for linea in f:
                    tabla.insert("", "end", values=linea.strip().split(","))

if __name__ == "__main__":
    app = App()
    app.mainloop()