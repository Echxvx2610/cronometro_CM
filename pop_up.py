import PySimpleGUI as sg

def pop_up():
    # Definir la lista de opciones
    opciones = ["Rollo mal montado","Cogiscan fallando","Rollos con estatica","Falla electrica","Falla mecanica","Error de operacion","Setup Ok!",]

    # Crear la ventana
    layout = [[sg.Text('Selecciona una opción')],
              [sg.Combo(opciones, key='-OPCION-', enable_events=True,size=(25,1))],
              [sg.Button('Aceptar')]]

    window = sg.Window('Selección', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Aceptar':
            opcion_seleccionada = values['-OPCION-']
            #print(opcion_seleccionada)
            #sg.popup(f'Opción seleccionada: {opcion_seleccionada}')
            window.close()
            return opcion_seleccionada
            
            
    window.close()

if __name__ == '__main__':
    pop_up()