class World:
    from Food import Food
    width_ = 0
    height_ = 0
    randomX = 0        
    food = 0
    
    def __init__(self, w, h):
        id = 0;
        self.width_ = w
        self.height_ = h
        self.food = self.Food(PVector(floor(random(0, self.width_)), floor(random(0, self.height_))), random(-1.0, 1.0), random(10, 20)) 

                
    def run(self):
        self.food.show()
