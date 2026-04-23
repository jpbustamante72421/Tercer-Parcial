import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

precio = 5.0
dinero = 0.0

# 💰 valores permitidos
valores_validos = [0.5, 1, 2, 5, 10]

stock = {
    "Coca-Cola": 5,
    "Fanta": 5,
    "Sprite": 5,
    "Jarrito": 5,
    "Mundet": 5,
    "Aga": 5
}

ventana = ctk.CTk()
ventana.title("Máquina Expendedora")
ventana.geometry("600x550")

def cargar_imagen(ruta):
    try:
        img = Image.open(ruta)
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)
    except:
        return None

imagenes = {
    "Coca-Cola": cargar_imagen("coca.png"),
    "Fanta": cargar_imagen("fanta.jpg"),
    "Sprite": cargar_imagen("sprite.jpg"),
    "Jarrito": cargar_imagen("jarritos.png"),
    "Mundet": cargar_imagen("mundet.jpg"),
    "Aga": cargar_imagen("aga.jpg")
}

def actualizar_dinero():
    label_dinero.configure(text=f"${dinero:.2f}")

def actualizar_precio():
    label_precio.configure(text=f"Precio: ${precio}")

def actualizar_botones():
    for bebida in radios:
        if dinero >= precio and stock[bebida] > 0:
            radios[bebida].configure(state="normal")
        else:
            radios[bebida].configure(state="disabled")

def mostrar_imagen():
    bebida = seleccion.get()
    if bebida and imagenes[bebida]:
        label_imagen.configure(image=imagenes[bebida], text="")
        label_imagen.image = imagenes[bebida]
    else:
        label_imagen.configure(text="Sin imagen")

# 🔥 FUNCIÓN MODIFICADA
def agregar_dinero():
    global dinero
    valor = entry_dinero.get()

    try:
        valor = float(valor)

        if valor not in valores_validos:
            messagebox.showerror("Error", "Solo se aceptan: 0.5, 1, 2, 5, 10")
            return

        dinero += valor
        actualizar_dinero()
        actualizar_botones()
        entry_dinero.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Ingresa un número válido")

def tomar_refresco():
    global dinero

    bebida = seleccion.get()

    if bebida == "":
        messagebox.showwarning("Error", "Selecciona un refresco")
        return

    if stock[bebida] <= 0:
        messagebox.showerror("Error", "Producto agotado")
        return

    if dinero < precio:
        messagebox.showerror("Error", "Dinero insuficiente")
        return

    stock[bebida] -= 1
    cambio = dinero - precio

    win = ctk.CTkToplevel(ventana)
    win.title("Compra exitosa")
    win.geometry("300x350")

    win.grab_set()
    win.focus()

    img_label = ctk.CTkLabel(win, text="", image=imagenes[bebida])
    img_label.pack(pady=10)

    ctk.CTkLabel(win, text="Disfruta tu refresco").pack(pady=5)

    if cambio > 0:
        ctk.CTkLabel(win, text=f"Tu cambio es: ${cambio:.2f}",
                     font=("Arial", 14)).pack(pady=5)
    else:
        ctk.CTkLabel(win, text="Sin cambio",
                     font=("Arial", 14)).pack(pady=5)

    ctk.CTkButton(win, text="Aceptar", command=win.destroy).pack(pady=15)

    dinero = 0
    seleccion.set("")
    label_imagen.configure(image=None, text="")
    label_imagen.image = None

    actualizar_dinero()
    actualizar_botones()
    actualizar_stock()

def actualizar_stock():
    texto = ""
    for bebida, cant in stock.items():
        texto += f"{bebida}: {cant}\n"
    label_stock.configure(text=texto)

def surtir():
    win = ctk.CTkToplevel(ventana)
    win.title("Surtir")
    win.geometry("300x200")

    win.grab_set()
    win.focus()

    ctk.CTkLabel(win, text="Selecciona bebida").pack(pady=5)
    combo = ctk.CTkComboBox(win, values=list(stock.keys()))
    combo.pack(pady=5)

    ctk.CTkLabel(win, text="Cantidad").pack(pady=5)
    cantidad = ctk.CTkEntry(win)
    cantidad.pack(pady=5)

    def confirmar():
        b = combo.get()
        c = cantidad.get()

        if not c.isdigit() or int(c) <= 0:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        stock[b] += int(c)
        actualizar_stock()
        win.destroy()

    ctk.CTkButton(win, text="Agregar", command=confirmar).pack(pady=10)

def cambiar_precio():
    global precio

    win = ctk.CTkToplevel(ventana)
    win.title("Cambiar Precio")
    win.geometry("300x150")

    win.grab_set()
    win.focus()

    ctk.CTkLabel(win, text="Nuevo precio").pack(pady=5)
    entry = ctk.CTkEntry(win)
    entry.pack(pady=5)

    def confirmar():
        global precio
        p = entry.get()

        if not p.isdigit() or int(p) <= 0:
            messagebox.showerror("Error", "Precio inválido")
            return

        precio = float(p)
        actualizar_precio()
        actualizar_botones()
        win.destroy()

    ctk.CTkButton(win, text="Cambiar", command=confirmar).pack(pady=10)

# menú
menu = tk.Menu(ventana)
ventana.config(menu=menu)

menu_opciones = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Opciones", menu=menu_opciones)

menu_opciones.add_command(label="Surtir", command=surtir)
menu_opciones.add_command(label="Cambiar precio", command=cambiar_precio)

# frames
frame_left = ctk.CTkFrame(ventana)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

frame_center = ctk.CTkFrame(ventana)
frame_center.grid(row=0, column=1, padx=10, pady=10)

frame_right = ctk.CTkFrame(ventana)
frame_right.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

# izquierda
ctk.CTkLabel(frame_left, text="Dinero").pack(pady=5)

label_dinero = ctk.CTkLabel(frame_left, text="$0.00", font=("Arial", 20, "bold"))
label_dinero.pack()

label_precio = ctk.CTkLabel(frame_left, text=f"Precio: ${precio}")
label_precio.pack(pady=5)

ctk.CTkLabel(frame_left, text="Ingresa dinero").pack(pady=5)

entry_dinero = ctk.CTkEntry(frame_left)
entry_dinero.pack(pady=5)

ctk.CTkLabel(frame_left, text="Acepta: 0.5, 1, 2, 5, 10").pack(pady=2)

ctk.CTkButton(frame_left, text="Agregar dinero", command=agregar_dinero).pack(pady=5)

# centro
ctk.CTkLabel(frame_center, text="Producto").pack(pady=10)

label_imagen = ctk.CTkLabel(frame_center, text="")
label_imagen.pack()

# derecha
ctk.CTkLabel(frame_right, text="Selecciona bebida").pack(pady=5)

seleccion = tk.StringVar()

radios = {}
for bebida in stock:
    rb = ctk.CTkRadioButton(frame_right, text=bebida,
                            variable=seleccion,
                            value=bebida,
                            command=mostrar_imagen,
                            state="disabled")
    rb.pack(anchor="w")
    radios[bebida] = rb

ctk.CTkButton(frame_right, text="Tomar Refresco",
              command=tomar_refresco).pack(pady=10)

ctk.CTkLabel(frame_right, text="Stock").pack()

label_stock = ctk.CTkLabel(frame_right, text="", justify="left")
label_stock.pack()

actualizar_stock()
actualizar_botones()

ventana.mainloop()