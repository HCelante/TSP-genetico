import sys
import numpy as np
import math
import random
import copy
import time
from matplotlib import pyplot as plt

################## ELITISMO #####################
def elitismo(pop, listfit, qtd):
    newpop = []
    sortedFit = selection(listfit)
    for i in range(qtd):
        newpop.append(pop[sortedFit[i]])
    return newpop

                                                
##############################################

def getDist(i, j, matriz):
    return matriz[i][j]

def fitness(pop, matriz):
    psum = 0
    listFit = []

    for i in range (len(pop)):
        for j in range (len(pop[i])-1):
            psum += getDist(pop[i][j], pop[i][j+1], matriz)
        psum += getDist(pop[i][j], pop[i][0], matriz)
        listFit.append(psum)
        psum = 0

    return listFit

###################### MUTACOES #########################################
def mutation2 (chromossome):
    n = len (chromossome) - 1
    gene = random.randint(0, n)
    rand = random.randint(0, n)
    while rand == gene:
        rand = random.randint(0, n)
    aux = chromossome[gene]
    chromossome[gene] = chromossome[rand]
    chromossome[rand] = aux
    return chromossome

def mutation1 (chromossome):
    n = len (chromossome) - 1
    gene = random.randint(0, n)
    if gene == n:
        aux = chromossome[gene]
        chromossome[gene] = chromossome[0]
        chromossome[0] = aux
    else:
        aux = chromossome[gene]
        chromossome[gene] = chromossome[gene+1]
        chromossome[gene+1] = aux
    return chromossome
########################################################################

def selection(listFit):
    ordedFit = sorted(range (len(listFit)), key= lambda k: listFit[k])
    return ordedFit

def crossOverOrd(p1, p2):
    r = copy.copy(p1)
    p = random.sample(range(0, len(p1)), random.randint(1, len(p1)-1))
    p.sort()
    s = []
    for i in p:
        s.append(p1[i])
    p_ord = []
    for i in p2:
        if i in s:
            p_ord.append(s.index(i))
    for i in range (len(s)):
        r[p[i]] = s[p_ord[i]]
    return r

def crossOverAlt(p1, p2):
    corte = random.randrange (0, len(p1)-1)
    r = copy.copy(p1[0:corte])
    pos = 0
    while len(r) < len(p1):
        if (p1[pos] not in r[0:len(r)]):
            r.append(p1[pos])
            pos += 1
        elif (p2[pos] not in r[0:len(r)]):
            r.append(p2[pos])
            pos += 1

        else:
            prox = encontraprox(p1, p2, r)
            r.append(prox)
            pos += 1
    return r

def encontraprox(p1, p2, r):
    prox = []
    for j in range(len(p2)):
        if(p2[j] not in r[0:len(r)]):
            prox = p2[j]
            break
    
    return prox

def genNewPop(pop, matriz, cRate, mRate, mType, alter, elit, iters):
    newPop = []
    newFits = fitness(pop, matriz)
    i = 0
    ordedFit = selection(newFits)
    cNum  = ((len(pop)*cRate)/100)
    while i < cNum:
        aux = ordedFit[i]
        if alter == True:
            if aux == len(pop)-1:
                newPop.append(crossOverAlt(pop[aux], pop[0]))
            else:
                newPop.append(crossOverAlt(pop[aux], pop[aux+1]))
        else:
            if aux == len(pop)-1:
                newPop.append(crossOverOrd(pop[aux], pop[0]))
            else:
                newPop.append(crossOverOrd(pop[aux], pop[aux+1]))
        
        if random.randrange(100)<= mRate:
            if mType == 1:
                newPop[i] = mutation1(newPop[i])
            else:
                newPop[i] = mutation2(newPop[i])
        i+=1
    if elit == True:
        for x in range (len(pop)):
            newPop.append(pop[x])
        newFits = fitness(newPop, matriz)
        newPop = elitismo(newPop, newFits, len(pop))
        ordedFit=selection(newFits)
    
    return newPop
            
##########################################################################
def genFirstPop(matriz, n):
    pop = []
    m = len(matriz)
    for i in range (n):
        pop.append(random.sample(range(0, m), n))

    return pop

###########################################################################
############# FUNCAO DE DISTANCIA EUCLIDIANA ##############################
def euclidean(no1, no2):
    xno1 = float(no1[0])
    yno1 = float(no1[1])
    xno2 = float(no2[0])
    yno2 = float(no2[1])
    Dxynos = 0.0

    # distancia euclidiana
    Dxynos = ((((xno1 - xno2) ** 2)+((yno1 - yno2) ** 2)) ** (0.5))
    return Dxynos
###########################################################################
def calcDist(lista):
    matriz=np.zeros(shape=(len(lista),len(lista)))
    for i in range (len(lista)):
        for j in range (len(lista)):
            matriz[i][j]=euclidean(lista[i], lista[j])
    return matriz

def start (auxList, estag, graph = True):
    mtAdj = calcDist(auxList)
    pop = genFirstPop(mtAdj,len(auxList))
    listFit = fitness(pop, mtAdj)
    ordedFits = selection(listFit)
    bestSolution = listFit[ordedFits[0]]
    minFits = []
    meanFits = []

    for i in range (estag):
        newPop = genNewPop(pop, mtAdj, 100, 10, 1, False, True, estag)
        newFits = fitness(newPop, mtAdj)
        pop = newPop
        ordedFits = selection(newFits)
        minFits.append(newFits[ordedFits[0]])
        meanFits.append(sum(newFits) / len(newFits))
        if min(minFits) < bestSolution:
            bestSolution = newFits[ordedFits[0]]
        print (meanFits[i])
    if graph:
        plt.figure()
        plt.plot(range(estag),  meanFits, label='Fitness medio')
        plt.plot(range(estag), minFits, label='Fitness maximo')
        plt.legend()
        plt.ylabel('Fitness')
        plt.xlabel('Geracoes')
        plt.show()
    bestChromo = newPop[ordedFits[0]]
    print bestChromo

if __name__ == "__main__":
    ################## LEITURA DE ARQUIVO ######################
    auxList = []
    with open((sys.argv[1]), "r") as f:
        dimension = [line.strip().split(" ") for line in f.readlines()[3:4]]
        dimension = int(dimension[0][1])
        dimension += 6
    f.close()
    with open((sys.argv[1]), "r") as f:
        auxList1 = [map(float, line.strip().split()) for line in f.readlines()[6:dimension]]
        auxList = [[x[1], x[2]] for x in auxList1]
    f.close()
    ini = time.time()
    start (auxList, 500)
    fim = time.time()
    print "Demorou: ", fim-ini
    ############################################################