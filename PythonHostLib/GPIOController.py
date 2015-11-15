import imp

gpio_found = False

try: 
    imp.find_module('RPi.GPIO')
    gpio_found = True
    import RPi.GPIO as GPIO
except ImportError:
    gpio_found = False

def pin_not_usable(pin, value):
    print("The pin number " + str(pin) + " cannot be used!")

def set_pwm_pin(pin, value):
    if gpio_found:
        pwms[pin].ChangeDutyCycle(value)

pwms = {
        18: None
    }

def set_pin(pin, value):
    if value > 100:
        value = 100
    if value < 0:
        value = 0
        
    if pin == 0:
        pin_not_usable(pin, value)
    if pin == 1:
        pin_not_usable(pin, value)
    if pin == 2:
        pin_not_usable(pin, value)
    if pin == 3:
        pin_not_usable(pin, value)
    if pin == 4:
        pin_not_usable(pin, value)
    if pin == 5:
        pin_not_usable(pin, value)
    if pin == 6:
        pin_not_usable(pin, value)
    if pin == 7:
        pin_not_usable(pin, value)
    if pin == 8:
        pin_not_usable(pin, value)
    if pin == 9:
        pin_not_usable(pin, value)
    if pin == 10:
        pin_not_usable(pin, value)
    if pin == 11:
        pin_not_usable(pin, value)
    if pin == 12:
        pin_not_usable(pin, value)
    if pin == 13:
        pin_not_usable(pin, value)
    if pin == 14:
        pin_not_usable(pin, value)
    if pin == 15:
        pin_not_usable(pin, value)
    if pin == 16:
        pin_not_usable(pin, value)
    if pin == 17:
        pin_not_usable(pin, value)
    if pin == 18:
        set_pwm_pin(pin, value)
    if pin == 19:
        pin_not_usable(pin, value)

def init():
    if gpio_found:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
    
        for pin, pwm in pwms.iteritems():
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 50)
            pwm.start(0)
            pwms[pin] = pwm
    else:
        print("GPIO not found, doing dummy-run.")
    
def destroy():
    if gpio_found:
        global pwms
        
        for pwm in pwms:
            pwm.stop()
        
        GPIO.cleanup()
