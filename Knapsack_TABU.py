from random import random
import matplotlib.pyplot as plt

# función de crear un gen con valores de 0 o 1 (lleva o no lleva), recibe el largo del gen y retorna el gen con 0 y 1
def Creagen(lr):
  return [int(random()*2) for i in range(lr)]

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

# la función la solucion con los valores para evaluar la restricción
# Devuelve el valor de 1 si se incumple la restricción o 0 si se cumple
def R2(sol):      
        if sol[0]== 1 and sol[3]== 1:
          return 1
        else:
          return 0

# la función la solucion con los valores para evaluar la restricción
# Devuelve el valor de 1 si se incumple la restricción o 0 si se cumple
def R3(sol):       
        if (sol[7]== 1 and sol[14]== 1):
          return 1
        else:
          return 0

# función de evaluar Función Objetivo (multiplicación de los valores de costos por el gen)
def FO(sol, coef):
    FO = 0
    for i in range(len(sol)):
        FO += sol[i] * coef[i]
    return FO

# recibe la solución actual, 
def Espacio(v1):
# crear la lista de lista
    booleanMatrix = []    
    for i in range(len(v1)):
      v2 = v1[:]
      if v1[i] == 1:
        v2[i] = 0
      else:
        v2[i] = 1
      booleanMatrix.append(v2)
    return booleanMatrix

# Recibe el espacio y la lista tabu
def Mejor (espacio, tabu, FVO, MJFO):
    # valor de la mejor solución del espacio
    mayor = 0
    # almacenar la posición
    indice = 0
    for i in range(len(FVO)): #(Si es mejor que el mejor valor no importa y se salta el no estar en la tabú (ASPIRACIÓN))
        if FVO[i] > MJFO:
          mayor = FVO[i]
          indice = i
        elif FVO[i] > mayor and tabu[i] == 0:
          mayor = FVO[i]
          indice = i                
    solucion = espacio[indice]
    return solucion, mayor, indice

# actualización tabú, recibe la lista tabú y el nuevo movimiento
def ActTabu (tabu, Nmov, Ttabu):
    tabu[Nmov] = Ttabu
    for i in range(len(tabu)):
        if tabu[i] > 0:
          tabu[i] = tabu[i]-1
    return tabu

# Recibe solución actual y la nueva solución

def NuevaSolucion (actualsol, nueva, FO1, FO2):  
    if FO2 > FO1:
      actualsol = nueva
      FO1 = FO2
      return actualsol, FO1
    else:
      return actualsol, FO1

if __name__ == '__main__':
### Datos a seleccionar 
    Ttabu = 4           # largo de la población
    Nitera = 1000       # Cantidad de iteraciones
    largo = 20          # largo del vector

# Parámetros items y morral
    Peso = [10, 19, 23, 8, 11, 16, 18, 7, 21, 24, 13, 1, 25, 17, 18, 1, 5, 1, 2, 6]
    Valor = [63, 67, 74, 85, 43, 22, 12, 38, 32, 82, 70, 20, 27, 55, 44, 0, 20, 80, 38, 10]
    Capacidad = 100

# Penalización por incumplimiento de restricciones
    Penaliza = 1000

# generación de párametros iniciales
    inicio = Creagen(largo)
    FOinicio = FO(inicio, Valor)
    tabu = [0 for i in range(largo)]
    VSol = inicio
    MejFO = [0 for i in range(Nitera)]
    MejFO[0] = FOinicio - Penaliza*(R1(inicio, Peso, Capacidad)+R2(inicio)+R3(inicio))
    datoI = []
    Actual =[[]]
    Actual[0] = inicio

for j in range(Nitera-1):
    # generación de espacio de solución
    Esolucion = Espacio(Actual[0])
    # evaluación de las FO de cada una de las soluciones
    fitness = [FO(Esolucion[i],Valor) - Penaliza*(R1(Esolucion[i], Peso, Capacidad)+R2(Esolucion[i])+R3(Esolucion[i])) for i in range(largo)]    
    # seleccion de la mejor solución actual
    Actual = Mejor (Esolucion, tabu, fitness, max(MejFO))
    # actualización de la lista tabu
    tabu= ActTabu(tabu, Actual[2], Ttabu)    
    # actualización de la solución actual
    VSol, MejFO[j+1] = NuevaSolucion(Actual[0], VSol, Actual[1], max(MejFO))
    # actualización de la mejor solución
    datoI.append(Actual[1])

print(f'La función objetivo es: {Actual[1]}')
# gráfico de cambio de la respuesta a medida que itera el programa
plt.plot(datoI, 'red', label = 'Comportamiento función objetivo')
plt.grid(True)
plt.legend()