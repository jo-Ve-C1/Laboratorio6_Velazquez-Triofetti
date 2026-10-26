#
#INFORMATICA II - Laboratorio VI.1 
#Estudiantes:
#            Trionfetti, Facundo
#            Velazquez Cruz, Joel
#
#Github: https://github.com/jo-Ve-C1/Laboratorio6_Velazquez-Triofetti
#
import math
from tkinter import *
from tkinter import ttk, messagebox
import numpy as np

#Funciones auxiliares para evaluar el polinomio hasta grado 6

def eval_polinomio(coefs, x):
    res = 0.0
    for i, c in enumerate(coefs):
        grado = 6 - i
        res += c * (x ** grado)
    return res

def eval_derivada_analitica(coefs, x):
    res = 0.0
    for i, c in enumerate(coefs[:-1]):
        grado = 6 - i
        res += c * grado * (x ** (grado - 1))
    return res

def obtener_coeficientes():
    try:
        return [float(e.get().replace(",", ".")) for e in entries_coefs]
    except ValueError:
        messagebox.showerror("Error", "Ingrese coeficientes numéricos válidos.")
        return None

def cargar_valores_prueba():
    vals_coefs = [0, 1, 0, -8, 0, 82, -25] # f(x) = x^5 - 8x^3 + 82x - 25
    for e, v in zip(entries_coefs, vals_coefs):
        e.delete(0, END); e.insert(0, str(v))

def borrar_todo():
    for e in entries_coefs: e.delete(0, END)

# --- VENTANA PRINCIPAL ---
raiz = Tk()
raiz.title("Laboratorio VI.1 - Commit 1")
raiz.geometry("750x200")

frame_poli = LabelFrame(raiz, text="Coeficientes del polinomio (a6 a a0)", padding=5)
frame_poli.pack(fill="x", padx=10, pady=10)

entries_coefs = []
for i in range(7):
    Label(frame_poli, text=f"a{6-i}").grid(row=0, column=i, padx=2)
    e = Entry(frame_poli, width=7, justify="center")
    e.grid(row=1, column=i, padx=2)
    entries_coefs.append(e)

Button(frame_poli, text="Borrar", command=borrar_todo, width=10).grid(row=0, column=7, padx=5)
Button(frame_poli, text="Valores de prueba", command=cargar_valores_prueba, width=14).grid(row=1, column=7, padx=5)

cargar_valores_prueba() # Carga inicial para testear
raiz.mainloop()