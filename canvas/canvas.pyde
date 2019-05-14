from World import World
w = 400
h = 400

world = World(w, h, 0, 1, 0)
def setup():
    size(w, h)
    

def draw():
    background(255)
    world.run()
