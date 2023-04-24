import os
import csv
import pandas as pd
from pandas import DataFrame
import PySimpleGUI as sg
import time as time_
from datetime import datetime,timedelta,time
import shutil   


#Definicion de tema(ingresa letras alazar para ver un tema aleaotorio,ejemplo: sg.theme())
sg.theme('Black')

# Define la interfaz gráfica de usuario
layout_izq = [
    [sg.Image(r'C:\cronometro_CM\img\LOGO_NAVICO_1_90.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-'),sg.Push()],
    [sg.VPush()],
    [sg.Push(),
     sg.Text('Tiempo de Inicio',font='Helvetica 20',expand_x=False),
     sg.Push()],
    [sg.Push(),
     sg.Text('00:00',text_color='#00FF00',key='-TT-',
                       font=('Helvetica',20,'bold'),
                       enable_events=True,
                       expand_x=False),
     sg.Push()],
    [sg.Text('00',text_color='red',font=('Helvetica', 48), justification='center', size=(10, 1), key='-TIMER-')],
    [sg.Button('Iniciar', size=(15, 2), font=('Helvetica', 14), key='-START-')],
    [sg.Button('Reiniciar', size=(15, 2), font=('Helvetica', 14), key='-RESET-',disabled=True)],
    [sg.Button(">>>>", size=(21, 1), font=('Helvetica', 10), key='-SIZEMAX-')],
    [sg.VPush()]]

#Setup para tabla de csv(sg.Table)
try:
    analisisTiempo = pd.read_csv(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv',usecols=['Ensamble','H_Inicio','T_Cambio','Fecha'])
    df_tiempo = pd.DataFrame(analisisTiempo).tail(5)
    columns = list(df_tiempo.columns)
    order_columns = [columns[0],"Secuencia",columns[1],columns[2],columns[3]]
    data = df_tiempo.values #data empaquetada dentro de otra lista [[], [], [], [], []]
    
    #notas para el desarrollo
    #print(df_tiempo,'\n')
    #print("columnas:",columns,'\n')
    #print("order_columns:",order_columns,'\n')
    #values = []
    #for i in data: #bucle for para desempacar una lista de lista en una sola lista []
    #    values.extend(i)
    #print("values:",data,'\n')

    #Acaba el setup para la tabla de CSV(sg.Table)


    layout_der = [
        [sg.Text("Tiempos de Cambios Recientes",font='Helvetica 20'),],          
        [sg.Table(values=data,
                headings=order_columns,
                max_col_width=5,
                auto_size_columns=False,
                justification='center',
                num_rows=5,
                key='-TABLE-',
                )],
        [sg.Button("<<<<", size=(21, 1), font=('Helvetica', 10), key='-SIZEMIN-')]
    ]
except:
    print("No se pudo leer el archivo")

layout_full = [
    [sg.Column(layout_izq,element_justification='center'),
     sg.VSeparator(),
     sg.Column(layout_der,element_justification='center')],
]

# Crea la ventana de la aplicación
window = sg.Window('Cronómetro', layout_full,icon=r'C:\cronometro_CM\ico\favicon.ico',
                   element_justification='center',
                   no_titlebar=False,
                   grab_anywhere = True,
                   finalize = True,
                   resizable=True,
                   size=(300,430))
window.set_min_size((300,430))

# Inicializa las variables del cronómetro
start_time = 0
paused_time = 0
elapsed_time = 0
paused = True


# Función para formatear el tiempo en minutos y segundos
def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f'{minutes:02}'#:{seconds:02}'

# Bucle principal de la aplicación
while True:
    event, values = window.read(timeout=10)
    if event == sg.WINDOW_CLOSED:
        break
    
    elif event == '-START-':
        # Inicia o pausa el cronómetro
        if paused:
            start_time = time_.time()
            paused = False
            hora_actual = datetime.time(datetime.now()).strftime('%H:%M') #tiempo actual(hora y minuto)
            window['-TT-'].update(hora_actual)
            window['-START-'].update('Pausar')
            sg.popup_no_wait('Cronómetro iniciado')
        else:
            paused_time += time_.time() - start_time
            paused = True
            window['-START-'].update('Iniciar')
            window['-START-'].Widget.configure(state='disabled')
            ensamble = sg.PopupGetText('Ingrese el ensamble',title='Cronómetro',no_titlebar=False,grab_anywhere=True)
            window['-RESET-'].Widget.configure(state='active')
            #modificar formato hora_actual para restar tl tiempo de cambio
            modif_hora_actual = hora_actual.replace(':',',')
            tiempo_time = list(modif_hora_actual.split(','))
            H_actual = int(tiempo_time[0])
            M_actual = int(tiempo_time[1])
            t1 = timedelta(hours=H_actual,minutes=M_actual)
            fecha_actual = datetime.now().strftime('%d-%m-%Y')   
            sg.popup(f'Tiempo de cambio: {format_time(elapsed_time)}'+' minuto(s)', title='Cronómetro')
            #visualizacion de datos en dataframe(utilizado en desarrollo)
            df = pd.DataFrame(
            {'Ensamble':ensamble,
            'H_Inicio':[str(t1)],
            'T_Cambio':[f'{format_time(elapsed_time)}:00'], 
            'Fecha':f'{fecha_actual}'
            })
            print(df)
            #condicion para crear csv con headers y guardar en el mismo directorio
            # if set(['Ensamble','Hora_inicio','Tiempo_de_cambio','Fecha']).issubset(df.columns):
            #     print("Yes")
            # else:
            #     print("No")
        
            if not os.path.exists(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv'):
                #print("No existian pero se creo un csv con headers")
                with open(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv','a+',newline="") as f: 
                    df.to_csv(f,sep=',',header=['Ensamble','H_Inicio','T_Cambio','Fecha'] ,index=False)
            elif os.path.exists(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv'):
                #print("Ya existia un csv con headers")
                with open(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv','a+',newline="") as f: 
                    df.to_csv(f,sep=',',header = False,index=False)
                    
            shutil.copy2(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv',r'H:\Temporal\CapturaDeTiemposSMT\LINEA 5') #LINEA n (ruta cambia dependiendo la linea)

    elif event == '-RESET-':
        # Reinicia el cronómetro y muestra el tiempo transcurrido
        if not paused:
            paused_time += time_.time() - start_time
            
        elapsed_time = round(paused_time)
        paused_time = 0
        paused = True
        start_time = 0
        window['-START-'].Widget.configure(state='active')
        window['-TIMER-'].update("00")
        window['-TT-'].update("00:00")
        window['-RESET-'].Widget.configure(state='disabled')
        window['-TABLE-'].update(values=data)
        data_actualizada = pd.read_csv(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv',usecols=['Ensamble','H_Inicio','T_Cambio','Fecha'])
        df_actual = pd.DataFrame(data_actualizada).tail(5)
        data_actual = df_actual.values
        print(data_actual)
        window['-TABLE-'].update(values=data_actual)
    # Actualiza el cronómetro si no está pausado
    if not paused:
        elapsed_time = round(paused_time + time_.time() - start_time)
        # Muestra el tiempo en la interfaz
        window['-TIMER-'].update(format_time(elapsed_time))
        
    if event == '-SIZEMIN-':
        #print("Ventana ajustada")
        window.size = (300,430)
        
    if event == '-SIZEMAX-':
        #print("Ventana ajustada")
        window.size = (930,430)
        
        
window.close()        
