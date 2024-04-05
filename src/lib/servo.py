from gpiozero import Servo
 
servo = None

def init_servo(pin, correction = 0.45):
    min_pw = ( 1.0 - correction ) / 1000
    max_pw = (2.0 + correction ) / 1000
    
    global servo
    servo = Servo(pin,min_pulse_width=min_pw,max_pulse_width=max_pw)

    close_gate()

def close_gate():
    if (servo is None):
        print("[Servo] ERROR: Servo can't CLOSE because it's initialized!")
        return

    print("[Servo] Close")
    servo.max()

def open_gate():
    if (servo is None):
        print("[Servo] ERROR: Servo can't OPEN because it's initialized!")
        return
    
    print("[Servo] Open")
    servo.mid()