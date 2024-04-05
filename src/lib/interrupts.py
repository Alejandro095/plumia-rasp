from gpiozero import Button
from time import sleep

btn = Button(15)
btn2 = Button(14)

def button_pressed_callback():
    print("Entrar")

def button_pressed_callback2():
    print("Salir")


btn.when_activated = button_pressed_callback
btn2.when_activated = button_pressed_callback2

while True:
    sleep(100)