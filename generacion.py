import math
import random


def traductor_accion(ac : int):
    salida = 0
    if ac == 0:
        salida = "01"
    elif ac == 1:
        salida = "2"
    elif ac == 2:
        salida = "3"
    elif ac == 3:
        salida = "4"
    elif ac == 4:
        salida = "5"
    else:
        salida = "67"
    return salida


def gen_secuencia(ac):
    salida = ""
    insertar = 0
    if ac == 0:
        insertar = "0"
    elif ac == 1:
        insertar = "1"
    elif ac == 2:
        insertar = "2"
    else:
        insertar = "3"
    if ac not in [3, 4]:
        for i in range(3, 10):
            salida = salida + insertar
    elif ac == 3:
        for i in range(3, 10):
            salida = salida + "5"
        for i in range(3, 10):
            salida = salida + "4"
    else:
        for i in range(3, 10):
            salida = salida + "4"
        for i in range(3, 10):
            salida = salida + "5"
    return salida


def minDist(list_number):
    min_dist = 999999999999999999
    for i in range(len(list_number)):
        for j in range(i+1, len(list_number)):
            if min_dist > abs(list_number[i] - list_number[j]):
                min_dist = abs(list_number[i] - list_number[j])
    return min_dist


def gen_ruido(secuencia):
    num_elem = random.randint(1, 5)
    posiciones = []
    dist = 0
    while dist < 4:
        posiciones = []
        for i in range(num_elem):
            posiciones.append(random.randint(0, len(secuencia)))
        dist = minDist(posiciones)
    for num in posiciones:
        actual = str(random.randint(0, 5))
        secuencia = secuencia[:num] + actual + secuencia[num:]
    return secuencia



def gen_num_salida():
    secuencia = ""
    accion = ""
    anterior = ""
    
    for i in range(6):
        accion_actual = random.randint(0, 5)

        while anterior == accion_actual:
            accion_actual = random.randint(0, 5)

        accion = accion + traductor_accion(accion_actual)
        secuencia = secuencia + gen_secuencia(accion_actual)
        anterior = accion_actual

    ruido = random.randint(0, 1)
    if ruido == 1:
        secuencia = gen_ruido(secuencia)

    with open("./salida.csv", mode="a") as csv:
        csv.writelines(f"{secuencia},{accion}\n")



for i in range(1000):
    gen_num_salida()
