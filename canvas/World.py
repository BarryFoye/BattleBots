class World:
    from Food import Food
    from Obstacle import Obstacle
    from Vehicle import Vehicle
    width_ = 0
    height_ = 0     
    food = []
    obstacle = []
    vehicle = []
    
    def __init__(self, w, h, pop_food, pop_obstacles, pop_vehicles):
        id = 0;
        self.width_ = w
        self.height_ = h
        for i in range(0, pop_food):
            self.food.append(self.Food()) 
        
        for i in range(0, pop_obstacles):
            self.obstacle.append(self.Obstacle())
            
        for i in range(0, pop_vehicles):
            self.vehicle.append(self.Vehicle(w,h))

                
    def run(self):
        for i in range(0, len(self.food)):
            self.food[i].show()
            
        for v in self.vehicle:
            v.update()
        
        
            
        for i in range(0, len(self.obstacle)):
            self.obstacle[i].show()
