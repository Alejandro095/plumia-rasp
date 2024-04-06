from gpiozero import Button
from lib.servo import init_servo, open_gate, close_gate
from time import sleep
from lib.oled.main import init_oled, display_common_screen, display_loading_screen, display_qr_screen
import requests

from lib.requests import getSpotsAvailable

from alpr.main import read_number_plate
from time import time

init_servo(26)
init_oled()

is_reading = False

input_sensor = Button(15)
output_sensor = Button(14)

def input_pressed_callback():
    global is_reading, input_sensor

    is_reading = True
    
    stop_loading_screen = display_loading_screen("Leyendo placa")

    def handler_license_plate(license_plate):
        body = {
            "licensePlate": license_plate,
            "mallId": "1"
        }
        response = requests.post("https://plumia-bot.onrender.com/api/visit/arrived", json=body)
        
        data = response.json()

        message = data.get("message")

        if (message == "Vehicle not found"):
            stop_loading_screen()
            display_qr_screen('t.me/PlumIA_bot')


        return response.status_code == 200
    
    lcp = read_number_plate(handler_license_plate, input_sensor)

    stop_loading_screen()

    print(lcp)

    if (lcp is not None):
        display_common_screen(f'Matricula: {lcp}')
        open_gate()
    else:
        is_reading = False 


def output_pressed_callback():
    global is_reading
    is_reading = False
    close_gate()

input_sensor.when_activated = input_pressed_callback
output_sensor.when_deactivated = output_pressed_callback

prev = time()

while True:
    
    if (is_reading):
        continue

    display_common_screen()
    sleep(10)

    if (is_reading):
        continue

    data = getSpotsAvailable()

    if (data != None):
        free = data.get("free")
        total = data.get("total")

        if (str(free) != '0'):
            display_common_screen("¡Lugares disponibles!", f"{free} / {total} libres")
        else:
            display_common_screen("Sin lugares disp.", "Vuelve mas tarde")
        
        sleep(10)
    if (is_reading):
        continue

    display_common_screen("¡Maneja con precaución!")
    sleep(10)