# Prueba github

from decimal import Decimal, getcontext
from math import factorial
from queue import Queue
from threading import Thread
from tkinter import *

# cantidad de hilos
cantidadhilos = []

# valores de salida de los hilos
resultadohilo = Queue()
dividendovar = Queue()
divisorvar = Queue()
resultadof = []

prin = Tk()
prin.title("Prueba de GUI")
prin.resizable(False, False)

hilosnum = IntVar()
knum = []
hiloactual = IntVar()
okVar = IntVar()


def dividendo(ks, dividendoqueue):
    dividendoqueue.put(
        Decimal(Decimal(pow(-1, ks)) * Decimal(factorial(6 * ks)) * (Decimal((545140134 * ks) + 13591409))))


def divisor(ks, divisorqueue):
    divisorqueue.put(Decimal(Decimal(factorial(3 * ks)) * Decimal(pow(factorial(ks), 3)) * Decimal(
        pow(640320, (Decimal((3 * ks) + (3 / 2)))))))


def serie(kin, outqueue, precision):
    getcontext().prec = precision
    resultado = 0
    if kin > 0:
        for ks in range(0, kin):
            threaddividendo = Thread(target=dividendo, args=(ks, dividendovar))
            threaddivisor = Thread(target=divisor, args=(ks, divisorvar))
            threaddividendo.start()
            threaddivisor.start()
            # threaddividendo.join()
            # threaddivisor.join()
            resultado += Decimal(dividendovar.get() / divisorvar.get())
        pi = Decimal(1 / (12 * resultado))
    else:
        pi = 3.1415926535897
    outqueue.put(pi)


def iniciarhilo():
    prec = 14 * int(knum[int(hiloactual.get())].get() * 50)
    cantidadhilos.append(int(hiloactual.get()))
    cantidadhilos[int(hiloactual.get())] = Thread(target=serie,
                                                  args=(knum[int(hiloactual.get())].get(), resultadohilo, prec))
    cantidadhilos[int(hiloactual.get())].start()


def siguiente():
    okVar.set(1)
    iniciarhilo()


def insertarhilos():
    contador = 5
    for hilo in range(0, int(hilosnum.get())):
        knum.append(hilo)
        knum[hilo] = IntVar()
        Label(prin, text=f"Elija el valor de K para el hilo {hilo}").grid(row=contador, column=1, padx=10, pady=10)
        k = Entry(prin, textvariable=knum[hilo])
        k.grid(row=contador, column=2)
        k.config(fg="red", justify="center")
        contador += 1
        hiloactual.set(hilo)
        boton2 = Button(prin, text="Ingresar K", command=siguiente)
        boton2.grid(row=contador, column=2)
        contador += 1
        boton2.wait_variable(okVar)
    Label(prin, text=f"Calculo realizado con exito").grid(
        row=contador, column=1, padx=10, pady=10)
    Label(prin, text=f"Cierre esta ventana").grid(
        row=contador+1, column=1, padx=10, pady=10)
    Label(prin, text=f"Revise el documento resultadof.txt").grid(
        row=contador+2, column=1, padx=10, pady=10)
    for hilo in range(0, int(hilosnum.get())):
        cantidadhilos[hilo].join()
        resultadof.append(f"El hilo {hilo} calculó el valor: {resultadohilo.get()} \n")
    # print(resultadof)
    with open("resultadof.txt", "w+") as file:
        for line in range(0, len(resultadof)):
            file.write(resultadof[line])


Label(prin, text="Favor elegir la cantidad de hilos a usar:").grid(row=1, column=1, padx=10, pady=10)
hilos = Entry(prin, textvariable=hilosnum)
hilos.grid(row=1, column=2)
hilos.config(fg="red", justify="center")
boton1 = Button(prin, text="Ingresar cantidad de hilos", command=insertarhilos)
boton1.grid(row=4, column=2)

prin.mainloop()
