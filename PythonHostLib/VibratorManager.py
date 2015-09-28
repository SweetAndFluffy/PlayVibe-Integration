class VibratorManager:
    vibes = list()
    points = 0
    
    def add_vibe(self, vibe):
        self.vibes.append(vibe)
    
    def update_vibes(self, t, mt):
        print("UPDATE VIBES")
        for vibe in self.vibes:
            vibe.update(t, mt, self.points)
            
    def set_points(self, value):
        self.points = value