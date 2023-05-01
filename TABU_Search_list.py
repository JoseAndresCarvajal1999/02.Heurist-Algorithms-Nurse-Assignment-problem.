import numpy as np 
import random 
import time 
import matplotlib.pyplot as plt 


def restricciones(matriz_Asignacion,numero_enfermeras, turnos, maximo_turnos, 
                  matriz_de_turnos, Li, Ui):
    
    matriz_aux = matriz_Asignacion
    for i in range(numero_enfermeras):
        c1 = 0
        c2 = 2
        
        while(c1 <= dias*turnos-2):
            if (matriz_aux[i,c1] + matriz_aux[i,c1+1] + matriz_aux[i,c1+2] >maximo_turnos):
                a = random.randint(0,2)
                matriz_aux[i,c1+a] = 0                
            c1 = c1 + 3    
            
        while (c2<= dias*turnos-16):
            if (matriz_aux[i,c2] + matriz_aux[i,c2+3] + matriz_aux[i,c2+6]
            + matriz_aux[i,c2+9] + matriz_aux[i,c2+12] + matriz_aux[i,c2+15]>5):
                matriz_aux[i,c2+15] = 0
            c2 = c2+ 3
                
        for c3 in range(0,64,21):
            dia = 0 
            for c4 in range(0,19,3):
               if (matriz_aux[i,c3+c4] + matriz_aux[i,c3+c4+1] + matriz_aux[i,c3+c4+2] !=0):
                   dia = dia + 1
            if(dia == 7):
                c5 = random.randrange(0,19,3)
                matriz_aux[i,c3+c5] = 0
                matriz_aux[i,c3+c5+1] = 0
                matriz_aux[i,c3+c5+2] = 0 
                
        suma_producto = int(np.dot(matriz_aux[i,:],matriz_de_turnos))
        
        while(suma_producto <= Li): 
            c6 = random.randrange(1,82,3)
            if (matriz_aux[i,c6-1] == 0 and matriz_aux[i,c6+1] == 0 and 
                matriz_aux[i,c6] == 1):
                    matriz_aux[i,c6-1] = 1
                    
            elif (matriz_aux[i,c6-1] == 1 and matriz_aux[i,c6+1] == 0 and 
                matriz_aux[i,c6] == 0):
                    matriz_aux[i,c6] = 1
            
            suma_producto = int(np.dot(matriz_aux[i,:],matriz_de_turnos))
                    
        while(suma_producto >= Ui):
             c7 = random.randint(0,dias*turnos-1)
             matriz_aux[i,c7] = 0
             suma_producto = int(np.dot(matriz_aux[i,:],matriz_de_turnos))
             
    return matriz_aux
            
  
def y(matriz_asignacion, matriz_de_turnos):
    n,m = np.shape(matriz_asignacion)
    auxiliar =  []
    for i in range(n):
        suma_producto = int(np.dot(matriz_asignacion[i,:],matriz_de_turnos)) 
        auxiliar.append(suma_producto)
    return sum(auxiliar)

    
def matriz_turnos(turnos, dias):
    matriz_hora_turno = np.zeros((turnos, dias))
    vector_turnos = np.array([10,6,8])
    for i in range(turnos):
        matriz_hora_turno[i,:] = vector_turnos[i]
    matriz_turno_t = np.transpose(matriz_hora_turno)
    matriz = matriz_turno_t.reshape(-1,1)
    return matriz

def funcion_objetivo(y, numero_enfermeras, matriz_asignacion, matriz_de_turnos):
    vector_de_valores = []
    for i in range(numero_enfermeras):
        valor = np.abs(y/numero_enfermeras - 
                       int(np.dot(matriz_asignacion[i,:],matriz_de_turnos)))
        vector_de_valores.append(valor)
    return sum(vector_de_valores)
    
def Penalizacion_funcion_objetivo(matriz_Asignacion,numero_enfermeras, turnos, maximo_turnos, 
                  matriz_de_turnos, Li, Ui):
    
    matriz_aux = matriz_Asignacion
    for i in range(numero_enfermeras):
        c1 = 0
        c2 = 2
        
        while(c1 <= dias*turnos-2):
            if (matriz_aux[i,c1] + matriz_aux[i,c1+1] + matriz_aux[i,c1+2] >maximo_turnos):
                return False               
            c1 = c1 + 3    
            
        while (c2<= dias*turnos-16):
            if (matriz_aux[i,c2] + matriz_aux[i,c2+3] + matriz_aux[i,c2+6]
            + matriz_aux[i,c2+9] + matriz_aux[i,c2+12] + matriz_aux[i,c2+15]>5):

                return False
            c2 = c2+ 3
                
        for c3 in range(0,64,21):
            dia = 0 
            for c4 in range(0,19,3):
               if (matriz_aux[i,c3+c4] + matriz_aux[i,c3+c4+1] + matriz_aux[i,c3+c4+2] !=0):
                   dia = dia + 1
            if(dia == 7):

                return False
                
        suma_producto = int(np.dot(matriz_aux[i,:],matriz_de_turnos))
        
        if(suma_producto <= Li or suma_producto >= Ui):

            return False
                    
    return True
    
def Tabu(matriz_asignacion, numero_enfermeras,turnos,maximo_turnos,
            matriz_turnos,Li,Ui,tano_bloque, numero_vecinos,numero_iteraciones, ruta_guardar):
    
    lista_Soluciones = []
    lista_funciones_objetivo = []
    lista_tabu = []
    soluciones_minimas = []
    
    for j in range(numero_iteraciones):        
        lista_Soluciones = []
        lista_funciones_objetivo = []
        dia = random.randrange(0,63,21)
        for i in range(numero_vecinos):
            matriz_asignacion_aux = matriz_asignacion.copy()
            aleatorio1 = random.randint(0,numero_enfermeras - 2*tano_bloque)
            bloque1 = matriz_asignacion_aux[aleatorio1:aleatorio1+tano_bloque,dia:dia+21] 
            aleatorio2 = random.randint(aleatorio1+1,numero_enfermeras - tano_bloque)
            bloque2 = matriz_asignacion_aux[aleatorio2:aleatorio2+tano_bloque,dia:dia+21]        
            matriz_asignacion_aux[aleatorio1:aleatorio1+tano_bloque,dia:dia+21] = bloque2
            matriz_asignacion_aux[aleatorio2:aleatorio2+tano_bloque,dia:dia+21] = bloque1
                        
            if (any(np.array_equal(matriz_asignacion_aux,matriz) for matriz in lista_tabu) == False):
                factibilidad  = Penalizacion_funcion_objetivo(matriz_asignacion_aux,
                                                              numero_enfermeras, 
                                                              turnos,maximo_turnos, 
                                                              matriz_de_turnos, Li, Ui)
                variable_auxiliar = y(matriz_asignacion_aux, matriz_de_turnos)
                funcion_Objetivo = funcion_objetivo(variable_auxiliar, numero_enfermeras, 
                                                    matriz_asignacion_aux
                                                    , matriz_de_turnos)
                if (factibilidad == False):
                    funcion_Objetivo = funcion_Objetivo*1000000
                    
                lista_Soluciones.append(matriz_asignacion_aux)
                lista_funciones_objetivo.append(funcion_Objetivo)
                lista_tabu.append(matriz_asignacion_aux)
                
        minimo = min(lista_funciones_objetivo)
        print(minimo)
        soluciones_minimas.append(minimo)
        indice = lista_funciones_objetivo.index(minimo)
        np.savetxt(ruta_guardar + '\\'+ 'Iteración.{}.txt'.format(j),lista_Soluciones[indice], 
                   delimiter = '\t')
        matriz_asignacion = lista_Soluciones[indice]
        
        
        
    return soluciones_minimas 



tiempo_inicial = time.time()           
numero_enfermeras = 60
dias = 28
turnos = 3 
maximo_turnos = 2
Li = 192
Ui = 340
tano_bloque = 5
numero_vecinos = 100
numero_iteraciones = 25
ruta_guardar = r''

matriz_asignacion = np.random.randint(2, size = (numero_enfermeras,dias*turnos))
copia = matriz_asignacion.copy()
matriz_de_turnos = matriz_turnos(turnos, dias)

nueva_matriz = restricciones(copia,numero_enfermeras, turnos, maximo_turnos,
                             matriz_de_turnos, Li, Ui)
nueva_matriz_aux =  nueva_matriz.copy()

variable_y = y(nueva_matriz, matriz_de_turnos)

funcion_Objetivo = funcion_objetivo(variable_y, numero_enfermeras, 
                                    nueva_matriz, matriz_de_turnos)
soluciones_minimas = Tabu(nueva_matriz_aux, numero_enfermeras,
                                    turnos,maximo_turnos,
            matriz_turnos,Li,Ui, tano_bloque, numero_vecinos,numero_iteraciones,
            ruta_guardar)




tiempo_final = time.time()
tiempo_total =  tiempo_final - tiempo_inicial
print('El tiempo de computo fué', tiempo_total)

maximo = max(soluciones_minimas)

plt.plot(soluciones_minimas/maximo)
plt.title('Funciones objetivo normalizada  de: '+ str(numero_iteraciones))
plt.xlabel('Número de iteraciones')
plt.ylabel('Función objetivo normalizada')
plt.show()









