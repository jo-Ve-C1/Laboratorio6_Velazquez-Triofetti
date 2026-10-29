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
    
def calcular_raiz():
    coefs = obtener_coeficientes()
    if coefs is None: return
    metodo = var_metodo.get()
    
    try:
        if var_criterio.get() == "es":
            es = float(entry_es.get().replace(",", "."))
        else:
            cifras = int(entry_cifras.get())
            es = 0.5 * (10 ** (2 - cifras)) # Criterio de Scarborough[cite: 76]
        max_iter = int(entry_max_iter.get())
    except ValueError:
        messagebox.showerror("Error", "Revise los campos numéricos de tolerancia.")
        return

    raiz, iters, ea, fr = None, 0, 0.0, 0.0

    try:
        if metodo == "Biseccion":
            xl = float(entry_xl.get().replace(",", "."))
            xu = float(entry_xu.get().replace(",", "."))
            if eval_polinomio(coefs, xl) * eval_polinomio(coefs, xu) >= 0:
                messagebox.showerror("Error", "El intervalo no presenta cambio de signo.")
                return
            xr = xl
            for k in range(1, max_iter + 1):
                xr_old = xr
                xr = (xl + xu) / 2.0
                iters = k
                if xr != 0: ea = abs((xr - xr_old) / xr) * 100
                test = eval_polinomio(coefs, xl) * eval_polinomio(coefs, xr)
                if test < 0: xu = xr
                elif test > 0: xl = xr
                else: ea = 0.0
                if k > 1 and ea <= es: break
            raiz = xr

        elif metodo == "Newton":
            xr = float(entry_xl.get().replace(",", "."))
            for k in range(1, max_iter + 1):
                df = eval_derivada_analitica(coefs, xr)
                if df == 0:
                    messagebox.showerror("Error", "Derivada nula detectada.")
                    return
                xr_next = xr - eval_polinomio(coefs, xr) / df
                iters = k
                if xr_next != 0: ea = abs((xr_next - xr) / xr_next) * 100
                xr = xr_next
                if ea <= es: break
            raiz = xr

        elif metodo == "Secante":
            x_im1 = float(entry_xl.get().replace(",", "."))
            xi = float(entry_xu.get().replace(",", "."))
            for k in range(1, max_iter + 1):
                f_xi = eval_polinomio(coefs, xi)
                f_xim1 = eval_polinomio(coefs, x_im1)
                den = f_xim1 - f_xi
                if den == 0:
                    messagebox.showerror("Error", "División por cero en Secante.")
                    return
                x_next = xi - (f_xi * (x_im1 - xi)) / den
                iters = k
                if x_next != 0: ea = abs((x_next - xi) / x_next) * 100
                x_im1, xi = xi, x_next
                if ea <= es: break
            raiz = xi

        fr = eval_polinomio(coefs, raiz)
        res_raiz.config(state="normal"); res_raiz.delete(0, END); res_raiz.insert(0, f"{raiz:.6f}"); res_raiz.config(state="readonly")
        res_iter.config(state="normal"); res_iter.delete(0, END); res_iter.insert(0, str(iters)); res_iter.config(state="readonly")
        res_ea.config(state="normal"); res_ea.delete(0, END); res_ea.insert(0, f"{ea:.4f}%"); res_ea.config(state="readonly")
        res_fr.config(state="normal"); res_fr.delete(0, END); res_fr.insert(0, f"{fr:.6e}"); res_fr.config(state="readonly")
    except Exception as e:
        messagebox.showerror("Error", f"Fallo: {e}")

def calcular_derivada():
    coefs = obtener_coeficientes()
    if coefs is None: return
    try:
        x0 = float(entry_x0_der.get().replace(",", "."))
        h = float(entry_h_der.get().replace(",", "."))
        # Diferencia finita centrada[cite: 108]
        df_num = (eval_polinomio(coefs, x0 + h) - eval_polinomio(coefs, x0 - h)) / (2 * h)
        res_der.config(state="normal"); res_der.delete(0, END); res_der.insert(0, f"{df_num:.6f}"); res_der.config(state="readonly")
    except ValueError:
        messagebox.showerror("Error", "Verifique los valores de x0 y dx.")

def cargar_valores_prueba():
    vals_coefs = [0, 1, 0, -8, 0, 82, -25]
    for e, v in zip(entries_coefs, vals_coefs):
        e.delete(0, END); e.insert(0, str(v))
    entry_x0_der.delete(0, END); entry_x0_der.insert(0, "1")
    entry_h_der.delete(0, END); entry_h_der.insert(0, "0.1")

def borrar_todo():
    for e in entries_coefs: e.delete(0, END)



# --- VENTANA PRINCIPAL ---

raiz = Tk()
raiz.title("Laboratorio VI.1 - Commit 2")
raiz.geometry("780x420")

frame_poli = ttk.LabelFrame(raiz, text="Coeficientes del polinomio (a6 a a0)", padding=5)
frame_poli.pack(fill="x", padx=10, pady=10)
entries_coefs = []
for i in range(7):
    Label(frame_poli, text=f"a{6-i}").grid(row=0, column=i, padx=2)
    e = Entry(frame_poli, width=7, justify="center"); e.grid(row=1, column=i, padx=2)
    entries_coefs.append(e)
Button(frame_poli, text="Valores de prueba", command=cargar_valores_prueba).grid(row=1, column=7, padx=5)

# Panel Raíces
frame_raiz = ttk.LabelFrame(raiz, text="Cálculo de una raíz (Punto 1)", padding=5)
frame_raiz.pack(fill="x", padx=10, pady=5)
var_metodo = StringVar(value="Biseccion")
Radiobutton(frame_raiz, text="Bisección", variable=var_metodo, value="Biseccion").grid(row=0, column=1)
Radiobutton(frame_raiz, text="Newton-Raphson", variable=var_metodo, value="Newton").grid(row=0, column=2)
Radiobutton(frame_raiz, text="Secante", variable=var_metodo, value="Secante").grid(row=0, column=3)

Label(frame_raiz, text="Xb / X0 / X-1:").grid(row=1, column=0, sticky="e")
entry_xl = Entry(frame_raiz, width=8, justify="center"); entry_xl.grid(row=1, column=1)
Label(frame_raiz, text="Xu / X0:").grid(row=1, column=2, sticky="e")
entry_xu = Entry(frame_raiz, width=8, justify="center"); entry_xu.grid(row=1, column=3)
Button(frame_raiz, text="Calcular", command=calcular_raiz, width=10).grid(row=1, column=4, rowspan=2, padx=10)

var_criterio = StringVar(value="es")
Radiobutton(frame_raiz, text="es (%):", variable=var_criterio, value="es").grid(row=2, column=0, sticky="w")
entry_es = Entry(frame_raiz, width=8, justify="center"); entry_es.grid(row=2, column=1)
Label(frame_raiz, text="Máx. iter.:").grid(row=3, column=0, sticky="e")
entry_max_iter = Entry(frame_raiz, width=8, justify="center"); entry_max_iter.grid(row=3, column=1)
Label(frame_raiz, text="Cifras signif.:").grid(row=2, column=2, sticky="e")
entry_cifras = Entry(frame_raiz, width=8, justify="center"); entry_cifras.grid(row=2, column=3)

# Resultados Raíz
Label(frame_raiz, text="Raíz:").grid(row=0, column=5, sticky="e")
res_raiz = Entry(frame_raiz, width=12, state="readonly", justify="center"); res_raiz.grid(row=0, column=6)
Label(frame_raiz, text="Iteraciones:").grid(row=1, column=5, sticky="e")
res_iter = Entry(frame_raiz, width=12, state="readonly", justify="center"); res_iter.grid(row=1, column=6)
Label(frame_raiz, text="ea (%):").grid(row=2, column=5, sticky="e")
res_ea = Entry(frame_raiz, width=12, state="readonly", justify="center"); res_ea.grid(row=2, column=6)
Label(frame_raiz, text="f(raíz):").grid(row=3, column=5, sticky="e")
res_fr = Entry(frame_raiz, width=12, state="readonly", justify="center"); res_fr.grid(row=3, column=6)

# Panel Derivada (Punto 2)
frame_der = ttk.LabelFrame(raiz, text="Cálculo de la derivada primera (diferencia centrada)[cite: 108, 343]", padding=5)
frame_der.pack(fill="x", padx=10, pady=5)

Label(frame_der, text="x0:").grid(row=0, column=0)
entry_x0_der = Entry(frame_der, width=8, justify="center"); entry_x0_der.grid(row=0, column=1)
Label(frame_der, text="dx:").grid(row=0, column=2)
entry_h_der = Entry(frame_der, width=8, justify="center"); entry_h_der.grid(row=0, column=3)
Button(frame_der, text="Calcular", command=calcular_derivada, width=10).grid(row=0, column=4, padx=15)
Label(frame_der, text="Derivada f'(x0):").grid(row=0, column=5)
res_der = Entry(frame_der, width=14, state="readonly", justify="center"); res_der.grid(row=0, column=6)

cargar_valores_prueba()
raiz.mainloop()