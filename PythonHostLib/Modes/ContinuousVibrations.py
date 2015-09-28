from Mode import Mode

class ContinuousVibrations(Mode):
    """Sets the vibrator to the current pleasure points"""
    name = "Continuous Vibrations"
    
    def __init__(self):
        return
    
    def calculate_intensity(self, t, mt, pp):
        return pp;