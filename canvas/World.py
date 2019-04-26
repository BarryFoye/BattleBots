class World:
    from Food import Food
    
    food = Food(PVector(100, 100), random(-1.0, 1.0), 20)
    
    def __init__(self):
        id = 0;
    
    def run(self):
        self.food.show()
