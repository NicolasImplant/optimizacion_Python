from random import random
import numpy as np
import matplotlib.pyplot as plt
import heapq

### creación de particulas - posiciones 
def CreaX(lr):
  return [int(random()*2) for i in range(lr)]

### evaluación fitness de la partícula
# función de evaluar fitness o FO (multiplicación de los valores de costos por el gen)
def FO (sol, coef):
    FO = 0
    for i in range(len(sol)):
        FO += sol[i] * coef[i]
    return FO

# la función recibe el gen, los valores que acompañan para evaluar la restricción y el limite
# Devuelve el valor de 1 si se incumple la restricción o 0 si se cumple
def R1(sol, coef, lim):
    LI = 0
    for i in range(len(sol)):
        LI += sol[i] * coef[i]
    if LI < lim:
        return 0
    else:
        return 1

## selección mejor por particula
def MejorF (sol1, FO1, sol2, FO2):
    if FO1 > FO2:
      mejor = sol1
      FMJ = FO1
    else:
      mejor = sol2
      FMJ = FO2
    return mejor, FMJ

## selección mejor por de todas las partículas
def MejorG (PobF, FVO):
    MejFO = max(FVO)
    indica = FVO.index(max(FVO))
    Respuesta = PobF[indica]
    return MejFO, Respuesta


if __name__ == '__main__':
### Parámetros
# largo de la partícula
    l = 20
## número de particulas
    NPar = 20
# número de iteraciones
    NRI = 200
# inercia
    w = 2
# constantes
    c1 = 1
    c2 = 3
# Penalización por incumplimiento de restricciones
    Penaliza = 1000
# Parámetros items y morral
    Peso = [10, 19, 23, 8, 11, 16, 18, 7, 21, 24, 13, 1, 25, 17, 18, 1, 5, 1, 2, 6]
    Valor = [63, 67, 74, 85, 43, 22, 12, 38, 32, 82, 70, 20, 27, 55, 44, 0, 20, 80, 38, 10]
    Capacidad = 100
# Vector soluciones
    datoI = []
# inicialización
# creación de pocisiones de la particula
    X = np.asarray([CreaX(l) for i in range(NPar)])
# creación de velocidades de las partículas
    V = np.asarray([CreaX(l) for i in range(NPar)])
### evaluación de las partículas
    fitness = [FO(X[i],Valor)- Penaliza*R1(X[i], Peso, Capacidad) for i in range(NPar)]    
# la mejor solución es la actual
    fbest = X[:]
# mejores FO actuales
    FOFbest = fitness[:]
## de las mejores selecciona la mejor global
    FOGbest, gbest = MejorG(fbest, FOFbest)

## Algoritmo

for k in range(NRI):
    V = [[w*V[i][j]+c1*random()*(fbest[i][j]-X[i][j])+c2*random()*(gbest[i]-X[i][j])  for j in range(l)] for i in range(NPar)]
    X=[[(1 if (int(X[i][j] + V[i][j]) % 2 == 1) else 0) for j in range(l)] for i in range(NPar)]
    fitness = [FO(X[i],Valor)- Penaliza*R1(X[i], Peso, Capacidad) for i in range(NPar)]   
    ## actualizar f best y fbest
    fbest = [MejorF(X[i], fitness[i], fbest[i], FOFbest[i])[0] for i in range(NPar)]
    FOFbest = [MejorF(X[i], fitness[i], fbest[i], FOFbest[i])[1] for i in range(NPar)]
    ## actualizar gbest
    FOGbest, gbest = MejorG (fbest, FOFbest)
    datoI.append(FOGbest)

print(f'El vector que genera la solución optima es: {gbest}')
print(f'La función objetivo tiene un valor de: {FOGbest}')

# gráfico de cambio de la respuesta a medida que itera el programa
plt.plot(datoI)