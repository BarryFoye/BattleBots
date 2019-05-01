class Obstacle:
    position = 0
    rotation = 0
    bignessX = 0
    bignessY = 0
    
    def __init__(self):
        self.position = PVector(floor(random(120, 280)), floor(random(120, 280)))
        self.rotation = random(0, TWO_PI)
        self.bignessX = floor(random(20, 60))
        self.bignessY = floor(random(20, 60))
    
    def show(self):
        
        pushMatrix();
        fill(0)
        translate(self.position.x, self.position.y)        
        rotate(self.rotation)
        rect(0, 0, self.bignessX, self.bignessY)
        popMatrix()
