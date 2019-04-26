class Food:
    position = PVector() 
    toxicity = 0
    bigness = 10
    c = 0.0
    
    def __init__(self, position, toxicity, bigness):        
        self.position = position
        self.toxicity = toxicity
        self.bigness = bigness
        self.c = (toxicity, -1.0, 1.0, 0, 255)
        
        
    def show(self):
        noFill()
        stroke(0, self.c, 0)
        circle(self.position.x, self.position.y, self.bigness)
