class Mode:
    name = "Unknown Name"
    min = 0
    max = 100
    
    def __init__(self):
        return
    
    def calculate_intensity(self, t, mt, npp):
        """Calculates the intensity of the vibrator. t = time passed in the current sequence, mt = sequence length, npp = normalized pleasure points"""
        return pp;