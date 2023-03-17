import time

# Definir la función del cronómetro
def cronometro(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    # Imprimir el tiempo transcurrido
    print(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

# Definir el tiempo inicial
tiempo_inicial = time.time()

while True:
    tiempo_transcurrido = int(time.time() - tiempo_inicial)
    cronometro(tiempo_transcurrido)
    time.sleep(1)
