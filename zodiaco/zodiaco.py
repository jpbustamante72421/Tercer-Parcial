import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#diccionario de imagenes
imagenes = {
    "Buey":"buey.png",
    "Caballo":"caballo.png",
    "Cabra":"cabra.png",
    "Cerdo":"cerdo.png",
    "Conejo":"conejo.png",
    "Dragon":"dragon.png",
    "Gallo":"gallo.png",
    "Mono":"mono.png",
    "Perro":"perro.png",
    "Rata":"rata.png",
    "Serpiente":"serpiente.png",
    "Tigre":"tigre.png"

}

an_actual = 2026
mes_actual = 3
dia_actual = 23

def zodia_chin(anio):
    animales = [
        "Mono", 
        "Gallo", 
        "Perro", 
        "Cerdo",
        "Rata",
        "Buey", 
        "Tigre", 
        "Conejo",
        "Dragón", 
        "Serpiente", 
        "Caballo", 
        "Cabra"
    ]
    return animales[anio % 12]

# calcular la edad
def calcular_edad(dia, mes, an):
    edad = an_actual - an
    if mes > mes_actual or (mes == mes_actual and dia > dia_actual):
        edad -= 1
    return edad

# imagenes
def mostrar_imagen(signo):
    try:
        nombre_archivo = imagenes.get(signo)

        if not nombre_archivo:
            messagebox.showerror("Error", "Signo no válido")
            return

        img = Image.open(nombre_archivo)
        img = img.resize((120, 120))
        img = ImageTk.PhotoImage(img)

        label_imagen.config(image=img)
        label_imagen.image = img

    except Exception as e:
        messagebox.showerror("Error", f"No se encontró la imagen\n{e}")

#imprimir
def imprimir():
    try:
        nombre = entrada_nombre.get()
        ap = entrada_apaterno.get()
        am = entrada_apmaterno.get()
        di = int(entrada_dia.get())
        me = int(entrada_mes.get())
        an = int(entrada_anio.get())
        s = sexo.get()

        if nombre == "" or ap == "" or am == "" or s == "":
            messagebox.showerror("Error", "Llena todos los campos")
            return

        edad = calcular_edad(di, me, an)
        zodiaco = zodia_chin(an)

        resultado.config(
            text=f"Nombre: {nombre} {ap} {am}\n"
                 f"Edad: {edad}\n"
                 f"Sexo: {s}\n"
                 f"Zodiaco Chino: {zodiaco}"
        )

        mostrar_imagen(zodiaco)

    except ValueError:
        messagebox.showerror("Error", "Ingresa números válidos en la fecha")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ventana principal
ventana = tk.Tk()
ventana.title("Signos del Zodiaco")
ventana.geometry("1200x500")

tk.Label(ventana, text="Datos Personales", font=("Arial", 10, "bold")).place(x=270, y=20)

tk.Label(ventana, text="Nombre:").place(x=100, y=80)
entrada_nombre = tk.Entry(ventana)
entrada_nombre.place(x=200, y=80)

tk.Label(ventana, text="A. Paterno:").place(x=100, y=120)
entrada_apaterno = tk.Entry(ventana)
entrada_apaterno.place(x=200, y=120)

tk.Label(ventana, text="A. Materno:").place(x=100, y=160)
entrada_apmaterno = tk.Entry(ventana)
entrada_apmaterno.place(x=200, y=160)

tk.Label(ventana, text="Fecha de Nacimiento", font=("Arial", 10, "bold")).place(x=250, y=210)

tk.Label(ventana, text="Día:").place(x=150, y=260)
entrada_dia = tk.Entry(ventana, width=5)
entrada_dia.place(x=190, y=260)

tk.Label(ventana, text="Mes:").place(x=260, y=260)
entrada_mes = tk.Entry(ventana, width=5)
entrada_mes.place(x=300, y=260)

tk.Label(ventana, text="Año:").place(x=370, y=260)
entrada_anio = tk.Entry(ventana, width=8)
entrada_anio.place(x=410, y=260)

tk.Label(ventana, text="Sexo:").place(x=300, y=310)

sexo = tk.StringVar()

tk.Radiobutton(ventana, text="Masculino", variable=sexo, value="Masculino").place(x=250, y=340)
tk.Radiobutton(ventana, text="Femenino", variable=sexo, value="Femenino").place(x=350, y=340)

btn = tk.Button(ventana, text="Imprimir", command=imprimir)
btn.place(x=260, y=380)

tk.Label(ventana, text="Resultado", font=("Arial", 10, "bold")).place(x=800, y=50)

resultado = tk.Label(ventana, text="", font=("Arial", 11), justify="left")
resultado.place(x=750, y=100)

label_imagen = tk.Label(ventana)
label_imagen.place(x=800, y=200)

ventana.mainloop()