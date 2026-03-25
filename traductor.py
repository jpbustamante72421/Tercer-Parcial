import tkinter as tk
from tkinter import messagebox

palabras_esp = {
    "hola": "hello",
    "adios": "bye"
}

palabras_ing = {
    "hello": "hola",
    "bye": "adios"
}

# cargar palabras desde archivo
def cargar_archivo():
    try:
        with open("trad.txt", "r") as f:
            for linea in f:
                esp, ing = linea.strip().split(",")
                palabras_esp[esp.lower()] = ing.lower()
                palabras_ing[ing.lower()] = esp.lower()
    except FileNotFoundError:
        pass  # Si no existe el archivo, no pasa nada

# guardar nueva palabra
def guardar_palabra(esp, ing):
    with open("trad.txt", "a") as f:
        f.write(f"{esp},{ing}\n")

def traducir():
    palabra = entrada_palabra.get().lower().strip()
    modo = var_modo.get()

    if palabra == "":
        messagebox.showerror("Error", "Escribe una palabra")
        return

    if modo == 1:  # Español-Inglés
        resultado = palabras_esp.get(palabra, "Palabra no encontrada")

    elif modo == 2:  # Inglés-Español
        resultado = palabras_ing.get(palabra, "Palabra no encontrada")

    lbl_resultado.config(text="Traducción: " + resultado)

def agregar_palabra():
    esp = entrada_esp.get().lower().strip()
    ing = entrada_ing.get().lower().strip()

    if esp == "" or ing == "":
        messagebox.showerror("Error", "Llena ambos campos")
        return

    palabras_esp[esp] = ing
    palabras_ing[ing] = esp

    guardar_palabra(esp, ing)  #guarda en archivo

    messagebox.showinfo("Éxito", "Palabra agregada")

    entrada_esp.delete(0, tk.END)
    entrada_ing.delete(0, tk.END)

# Ventana principal
ventana = tk.Tk()
ventana.title("Traductor")
ventana.geometry("400x500")

# Cargar archivo al iniciar
cargar_archivo()
tk.Label(ventana, text="Escribe una palabra:").pack(pady=10)

entrada_palabra= tk.Entry(ventana)
entrada_palabra.pack(pady=5)

# Traducción
var_modo = tk.IntVar(value=1)
tk.Radiobutton(ventana, text="Español -> Inglés", variable=var_modo, value=1).pack()
tk.Radiobutton(ventana, text="Inglés -> Español", variable=var_modo, value=2).pack()

btn_traducir = tk.Button(ventana, text="Traducir", command=traducir)
btn_traducir.pack(pady=20)

lbl_resultado = tk.Label(ventana, text="Traducción: ")
lbl_resultado.pack(pady=10)

tk.Label(ventana, text="Agregar nueva palabra").pack(pady=10)

entrada_esp = tk.Entry(ventana)
entrada_esp.pack(pady=5)

entrada_ing = tk.Entry(ventana)
entrada_ing.pack(pady=5)

tk.Button(ventana, text="Agregar palabra", command=agregar_palabra).pack(pady=10)

ventana.mainloop()