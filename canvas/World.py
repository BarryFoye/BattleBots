class World:
    from Food import Food
    from Obstacle import Obstacle
    width_ = 0
    height_ = 0     
    food = 0
    obstacle = 0
    
    def __init__(self, w, h):
        id = 0;
        self.width_ = w
        self.height_ = h
        self.food = self.Food() 
        self.obstacle = self.Obstacle()

                
    def run(self):
        self.food.show()
        self.obstacle.show()
