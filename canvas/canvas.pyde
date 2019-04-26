from World import World

world = World()
def setup():
    size(400, 400)
    

def draw():
    background(255)
    world.run()
    
