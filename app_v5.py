import os
import csv
import pandas as pd
from pandas import DataFrame
import PySimpleGUI as sg
import time as time_
from datetime import datetime,timedelta,time


#seleccion de tema
sg.theme('Black')

# Define la interfaz gráfica de usuario
layout = [
    [sg.Image(r'C:\cronometro_CM\img\LOGO_NAVICO_1_90.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-'),sg.Push()],
    [sg.VPush()],
    [sg.Push(),
     sg.Text('Tiempo de Inicio',font='Helvetica 20',expand_x=False),
     sg.Push()],
    [sg.Push(),
     sg.Text('00:00:00',text_color='#00FF00',key='-TT-',
                       font=('Helvetica',20,'bold'),
                       enable_events=True,
                       expand_x=False),
     sg.Push()],
    [sg.Text('00:00',text_color='red',font=('Helvetica', 48), justification='center', size=(10, 1), key='-TIMER-')],
    [sg.Button('Iniciar/Pausar', size=(15, 2), font=('Helvetica', 14), key='-START-')],
    [sg.Button('Reiniciar', size=(15, 2), font=('Helvetica', 14), key='-RESET-')],
    [sg.VPush()]]

# Crea la ventana de la aplicación
window = sg.Window('Cronómetro', layout,icon=r'C:\cronometro_CM\ico\favicon.ico',
                   element_justification='center',
                   no_titlebar=False,
                   grab_anywhere = True,
                   finalize = True,
                   resizable=False,
                   size=(300,400))

# Inicializa las variables del cronómetro
start_time = 0
paused_time = 0
elapsed_time = 0
paused = True
hora_actual = datetime.time(datetime.now()).strftime('%H:%M:%S')
# Función para formatear el tiempo en minutos y segundos
def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f'{minutes:02d}:{seconds:02d}'

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
            window['-TT-'].update(hora_actual)
            sg.popup_no_wait('Cronómetro iniciado')
        else:
            paused_time += time_.time() - start_time
            paused = True
            window['-START-'].Widget.configure(state='disabled')
    elif event == '-RESET-':
        # Reinicia el cronómetro y muestra el tiempo transcurrido
        if not paused:
            paused_time += time_.time() - start_time
            
        elapsed_time = round(paused_time)
        paused_time = 0
        paused = True
        start_time = 0
        
        #Modificar formato hora_actual para restar el tiempo de cambio
        modif_hora_actual = hora_actual.replace(':',',')
        tiempo_time = list(modif_hora_actual.split(','))
        H_actual = int(tiempo_time[0])
        M_actual = int(tiempo_time[1])
        S_actual = int(tiempo_time[2])
        t1 = timedelta(hours=H_actual,minutes=M_actual,seconds=S_actual)
        
        ensamble = sg.PopupGetText('Ingrese el ensamble',title='Cronómetro',no_titlebar=False,grab_anywhere=True)
        fecha_actual = datetime.now().strftime('%d-%m-%Y')
        
        sg.popup(f'Tiempo de cambio: {format_time(elapsed_time)}', title='Cronómetro')
        window['-START-'].Widget.configure(state='active')
        window['-TIMER-'].update("00:00")
        window['-TT-'].update("00:00")
        #Visualizacion de datos en dataframe(utilizado en desarrollo)
        df = pd.DataFrame(
            {'Ensamble':ensamble,
            'Hora_inicio':[str(t1)],
            'Tiempo_de_cambio':[f'{format_time(elapsed_time)}'],
            'Fecha':[fecha_actual]
            })
        #guardado de datos en dataframe-csv
        with open(r'C:\cronometro_CM\csv\Captura_de_tiempo.csv', 'a' ,newline="") as f: 
            df.to_csv(f, header=None ,index=False)
        
    # Actualiza el cronómetro si no está pausado
    if not paused:
        elapsed_time = round(paused_time + time_.time() - start_time)
        # Muestra el tiempo en la interfaz
        window['-TIMER-'].update(format_time(elapsed_time))
        
window.close()