from VibratorAdapter import VibratorAdapter

class VibratorManager:
    vibes = list()
    points = 0
    
    def add_vibe(self, vibe):
        self.vibes.append(vibe)
    
    def update_vibes(self, t, mt):
        for vibe in self.vibes:
            vibe.update(t, mt, self.points)
            
    def set_points(self, value):
        self.points = value
    def get_points(self):
        return self.points
    def clear():
        self.vibes = list()
