import serial
import time

# Configurez le port série et le débit en bauds
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

def send_command(command):
    arduino.write(bytes(command, 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    return data

#while True:
    command = input("Entrez 'on' pour allumer la LED, 'off' pour l'éteindre: ")
    response = send_command(command)
    print(response.decode('utf-8'))
