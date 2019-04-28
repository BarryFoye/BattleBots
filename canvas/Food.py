class Food:
    position = PVector() 
    toxicity = 0
    bigness = 10
    r = 0
    g = 0
    b = 0
    
    def __init__(self, position, toxicity, bigness):     
        self.position = position
        self.toxicity = toxicity
        self.bigness = bigness
        self.r = map(self.toxicity, -1.0, 1.0, 255, 0)
        self.g = map(self.toxicity, -1.0, 1.0, 0, 255)
        #self.b = map(toxicity, -1.0, 1.0, 0, 255)


    def show(self):
        noStroke()
        fill(self.r, self.g, self.b)
        circle(self.position.x, self.position.y, self.bigness)
        
    
    def potency(self):
        return self.bigness * self.toxicity
