#archivo de pruebas para la minipulacion de tiempos
#puedes borrarlo o dejarlo para dudas etc

import PySimpleGUI as sg
import pandas as pd
from pandas import DataFrame
import time as time_
from datetime import datetime,timedelta,time


print(dir(datetime))
print('\n')


hora = datetime.time(datetime.now()).strftime('%H:%M:%S')
hora_final = datetime.time(datetime.now()).strftime('%H:%M:%S')
print(hora,'\n')


modif_hora = hora.replace(':',',')
tiempo = list(modif_hora.split(','))
H = int(tiempo[0])
M = int(tiempo[1])
S = int(tiempo[2])
t1 = time(H,M,S)
t2 = time(minute=M,second=S)

tiempo_pausado = 0
tiempo_inicial = time_.time() - tiempo_pausado
print(H,M,S,'\n')
print(t1,'\n')
print(t2,'\n')
print(tiempo_inicial,'\n')


#resta de tiempos

tiempo1 = datetime.time(datetime.now()).strftime('%H:%M:%S')
timpo2 = datetime.time(datetime.now()).strftime('%H:%M:%S')

tiempo1_modif = tiempo1.replace(':',',')
tiempo1_nuevo = list(tiempo1_modif.split(','))
H_tiempo1 = int(tiempo1_nuevo[0])
M_tiempo2 = int(tiempo1_nuevo[1])
S_tiempo2 = int(tiempo1_nuevo[2])
t1_tiempo1 = timedelta(hours=H_tiempo1,minutes=M_tiempo2,seconds=S_tiempo2)
t2_tiempo1 = timedelta(hours=H,minutes=12,seconds=S)
fecha_actual = datetime.now().strftime('%H:%M:%S,%d-%m-%Y')
print(t1_tiempo1,'\n')
print(t2_tiempo1,'\n')
print(t1_tiempo1-t2_tiempo1,'\n') #resta de tiempo(tipo de dato int)


captura = '28343-1C'+str(t2_tiempo1)+ str(t1_tiempo1)
print(captura,'\n')

#df = pd.DataFrame(captura)
df = pd.DataFrame({'Ensamble':['28343-1C'],'tiempo1':[str(t1_tiempo1)],'tiempo2':[str(t2_tiempo1)],'fecha':[fecha_actual]})
print(df,'\n')








####pruebas de tiempo##########


# Definir la función del cronómetro
def cronometro(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    # Imprimir el tiempo transcurrido
    print(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

# Definir el tiempo inicial
tiempo_inicial = time_.time()

while True:
    tiempo_transcurrido = int(time_.time() - tiempo_inicial)
    cronometro(tiempo_transcurrido)
    time_.sleep(1)





