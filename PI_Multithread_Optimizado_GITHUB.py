# Prueba github

from decimal import Decimal, getcontext
from math import factorial
from queue import Queue
from threading import Thread

# cantidad de hilos
cantidadhilos = []

# valores de salida de los hilos
resultadohilo = Queue()
dividendovar = Queue()
divisorvar = Queue()


def dividendo(ks, dividendoqueue):
    dividendoqueue.put(
        Decimal(Decimal(pow(-1, ks)) * Decimal(factorial(6 * ks)) * (Decimal((545140134 * ks) + 13591409))))


def divisor(ks, divisorqueue):
    divisorqueue.put(Decimal(Decimal(factorial(3 * ks)) * Decimal(pow(factorial(ks), 3)) * Decimal(
        pow(640320, (Decimal((3 * ks) + (3 / 2)))))))


# calculo de pi
def serie(kin, outqueue, precision):
    getcontext().prec = precision
    resultado = 0
    if kin > 0:
        for ks in range(0, kin):
            threaddividendo = Thread(target=dividendo, args=(ks, dividendovar))
            threaddivisor = Thread(target=divisor, args=(ks, divisorvar))
            threaddividendo.start()
            threaddivisor.start()
            threaddividendo.join()
            threaddivisor.join()
            resultado += Decimal(dividendovar.get() / divisorvar.get())
        pi = Decimal(1 / (12 * resultado))
    else:
        pi = 3.1415926535897
    outqueue.put(pi)


hilos = int(input("Favor elegir la cantidad de hilos a usar: "))
for hilo in range(0, hilos):
    print("Elija el valor de K para el hilo " + str(hilo + 1))
    k = int(input())
    prec = 14 * k
    cantidadhilos.append(hilo)
    cantidadhilos[hilo] = Thread(target=serie, args=(k, resultadohilo, prec))
    cantidadhilos[hilo].start()
for hilo in range(0, hilos):
    cantidadhilos[hilo].join()
    print(f"El hilo {hilo + 1} calculó el valor: {resultadohilo.get()}")

input("Toque una tecla para salir...")