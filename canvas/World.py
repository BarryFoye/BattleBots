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
            
        if(self.spawn_prob() < 0.001):
            self.food.append(self.Food()) 
   
                     
    def spawn_prob(self):
        # what are the chances of food spawning (how often)
        return random(0,1)
    
    def spawn_distrib(self):
        # what is the likleyhood of food spawning in a certain area given food in its neighbourhood
        return 0


    def spawn_density(self):
        # if food spawns how much/dense spawns given obstacles in its neighbourhood
        return 0
