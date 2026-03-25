import tkinter as tk
from tkinter import messagebox

# cargar palabras desde archivo
def cargar_archivo():
    dic = {}
    try:
        with open("diccionario.txt", "r") as f:
            for linea in f:
                esp,ing = linea.strip().split(",")
                dic[esp.lower()] = ing.lower()
    except:
        pass
    return dic

# guardar nueva palabra
def guardar_palabra(esp, ing):
    with open("diccionario.txt", "a") as f:
        f.write(f"{esp},{ing}\n")

# traducir
def traducir():
    palabra =entrada.get().lower()
    dic =cargar_archivo()
    if opcion.get() == 1:  #español-inglés
        resultado = dic.get(palabra, "No encontrada")
    else:
        inv_dic = {v: k for k, v in dic.items()}
        resultado = inv_dic.get(palabra, "No encontrada")

    lbl_resultado.config(text=resultado)
# agregar nueva palabra
def agregar():
    esp = entrada_esp.get().lower()
    ing = entrada_ing.get().lower()

    if esp == "" or ing == "":
        messagebox.showerror("Error", "Campos vacíos")
        return

    guardar_palabra(esp, ing)
    messagebox.showinfo("Éxito", "Palabra agregada")

# =================
# INTERFAZ
root = tk.Tk()
root.title("Traductor")
root.geometry("350x350")

# entrada
entrada = tk.Entry(root)
entrada.pack(pady=10)

# opcion idioma
opcion = tk.IntVar(value=1)

tk.Radiobutton(root, text="Español - Inglés", variable=opcion, value=1).pack()
tk.Radiobutton(root, text="Inglés - Español", variable=opcion, value=2).pack()

# boton traducir
tk.Button(root, text="Traducir", command=traducir).pack(pady=10)

# resultado
lbl_resultado = tk.Label(root, text="")
lbl_resultado.pack(pady=10)

# seccion de agregar
tk.Label(root, text="Agregar nueva palabra").pack()

entrada_esp = tk.Entry(root)
entrada_esp.pack()
entrada_esp.insert(0, "Español")

entrada_ing = tk.Entry(root)
entrada_ing.pack()
entrada_ing.insert(0, "Inglés")

tk.Button(root, text="Agregar", command=agregar).pack(pady=10)

root.mainloop()