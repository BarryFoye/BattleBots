class World:
    from Food import Food
    width_ = 0
    height_ = 0     
    food = 0
    
    def __init__(self, w, h):
        id = 0;
        self.width_ = w
        self.height_ = h
        self.food = self.Food() 

                
    def run(self):
        self.food.show()
