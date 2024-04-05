from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from pathlib import Path
import threading

from lib.oled.utils.text import center_text

serial = None
device = None
initialized = False

primary_font_path = str(Path(__file__).parent.parent.parent.joinpath("fonts", "roboto.ttf"))
secondary_font_path = str(Path(__file__).parent.parent.parent.joinpath("fonts", "ptsans.ttf"))

title_font = ImageFont.truetype(primary_font_path, 18)
subtitle_font = ImageFont.truetype(secondary_font_path, 12)

def init_oled(init_port = 1, init_address = 0x3C):
    global serial, device, initialized
    serial = i2c(port=init_port, address=init_address)
    device = sh1106(serial, rotate=0)
    initialized = True

def display_common_screen(message="Bievenido"):
    if (initialized is not True):
        print("[Servo] ERROR: It's not initialized!")
        return;

    # Crear una imagen PIL
    image = Image.new("1", (device.width, device.height), "black")
    draw = ImageDraw.Draw(image)

    # Dibujar en la imagen
    center_text(draw, "PlumIA", title_font, (0, 0, device.width, device.height), 5)
    center_text(draw, message, subtitle_font, (0, 0, device.width, device.height), 25)

    # Mostrar la imagen en la pantalla OLED
    device.display(image)


def display_loading_screen(message="Espere un momento"):
    stop_spinner_event = threading.Event()
    
    def draw_spinner():
        wait_time=0.02
        thickness=2
        arc_extent=90
        
        # Center coordinates
        center_x = device.width // 2
        center_y = (device.height // 2) + 20
        # Outer radius
        outer_radius = min(device.width, device.height) // 9
        # Initial angle
        initial_angle = 0
        # Angle increment per frame
        angle_increment = 20

        while not stop_spinner_event.is_set():
            with canvas(device) as draw:
                # Draw the "Loading" text at the top
                center_text(draw, "PlumIA", title_font, (0, 0, device.width, device.height), 5)
                center_text(draw, message, subtitle_font, (0, 0, device.width, device.height), 25)
                
                # Draw the animated arc
                for thickness_index in range(thickness):
                    radius = outer_radius - thickness_index
                    draw.arc((center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                            start=initial_angle, end=initial_angle + arc_extent, fill="white")
                initial_angle += angle_increment
            sleep(wait_time)

    spinner_thread = threading.Thread(target=draw_spinner)

    spinner_thread.start()

    def stop_spinner():
        print("Deteniendo")
        stop_spinner_event.set()
        spinner_thread.join()


    return stop_spinner


def show_empty_screen():
    device.clear()