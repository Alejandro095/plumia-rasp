from lib.servo import init_servo, open_gate, close_gate
from time import sleep
from lib.oled.main import init_oled, display_common_screen, display_loading_screen

init_servo(26)
init_oled()

close_gate()
display_common_screen()
sleep(4)

stop = display_loading_screen("Leyendo placa")
sleep(4)

stop()
display_common_screen()

open_gate()
sleep(4)
close_gate()

sleep(100)