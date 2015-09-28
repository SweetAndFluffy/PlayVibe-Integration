import RPi.GPIO as GPIO

def pin_not_usable(pin, value):
    print("The pin number " + pin + " cannot be used!")

def set_pwm_pin(pin, value):
    pwms[pin].ChangeDutyCycle(value)

pinFunctions = {
        1: pin_not_usable,
        2: pin_not_usable,
        3: pin_not_usable,
        4: pin_not_usable,
        5: pin_not_usable,
        6: pin_not_usable,
        7: pin_not_usable,
        8: pin_not_usable,
        9: pin_not_usable,
        10: pin_not_usable,
        11: pin_not_usable,
        12: pin_not_usable,
        13: pin_not_usable,
        14: pin_not_usable,
        15: pin_not_usable,
        16: pin_not_usable,
        17: pin_not_usable,
        18: set_pwm_pin, 
        19: pin_not_usable, 
        20: pin_not_usable, 
        20: pin_not_usable, 
        21: pin_not_usable, 
        22: pin_not_usable, 
        23: pin_not_usable, 
        24: pin_not_usable, 
        25: pin_not_usable, 
        26: pin_not_usable, 
        27: pin_not_usable, 
        28: pin_not_usable, 
        29: pin_not_usable, 
    }

pwms = {
        18: None
    }

def set_pin(pin, value):
    if value > 100:
        value = 100
    if value < 0:
        value = 0
        
    pinFunctions[pin]()

def init():
    GPIO.setmode(GPIO.BCM)
    
    for pin, pwm in pwms:
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pwmPin, 50)
        pwm.start(0)
    
def destroy():
    global pwms
    
    for pwm in pwms:
        pwm.stop()
    
    GPIO.cleanup()