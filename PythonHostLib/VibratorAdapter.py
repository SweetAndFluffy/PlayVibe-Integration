import GPIOController

# Vibrator Modes Imports
from Modes import ContinuousVibrations

class VibratorAdapter:
    intensity = 0
    modes = set()
    name = "Unnamed"
    
    gpioPin = 0
    
    def __init__(self):
        intensity = 0;
        
    def __init__(self, vibe):
        self.name = vibe['name']
        for mode in vibe['modes']:
            if mode['mode'] is 'ContinuousVibrations':
                conVibes = ContinuousVibrations()
                conVibes.min = mode['min']
                conVibes.max = mode['max']
                self.modes.add(conVibes)
    
    def set_intensity(self, new_intensity):
        self.intensity = new_intensity;
        GPIOController.set_pin(self.gpioPin, new_intensity)
        
    def set_modes(self, modes):
        self.modes = modes;
        
    def get_active_mode(self, pp):
        for mode in self.modes:
            if mode.min <= pp and mode.max > pp:
                return mode
        
    def get_npp(self, pp):
        active_mode = self.get_active_mode(pp)
        return pp - active_mode.min
        
    def update(self, t, mt, pp):
        if len(self.modes) > 0:
            print("UPDATE MODES")
            self.set_intensity(self.get_active_mode().calculate_intensity(t, mt,
                self.get_npp()))
        else:
            self.set_intensity(pp)
        
    def set_gpio_pin(self, pin):
        self.gpioPin = pin;
        