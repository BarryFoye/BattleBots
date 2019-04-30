class World:
    from Food import Food
    from Obstacle import Obstacle
    width_ = 0
    height_ = 0     
    food = []
    obstacle = []
    
    def __init__(self, w, h, pop_food, pop_obstacles):
        id = 0;
        self.width_ = w
        self.height_ = h
        for i in range(0, pop_food):
            self.food.append(self.Food()) 
        
        for i in range(0, pop_obstacles):
            self.obstacle.append(self.Obstacle())

                
    def run(self):
        for i in range(0, len(self.food)):
            self.food[i].show()
            
        for i in range(0, len(self.obstacle)):
            self.obstacle[i].show()
