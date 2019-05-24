from World import World
w = 400
h = 400

<<<<<<< HEAD
world = World(w, h, 0, 0, 0)
=======
world = World(w, h,3, 3, 3)
>>>>>>> fcc5d63bd651ce49bce4178066fc32530b4f2769
def setup():
    size(w, h)
    

def draw():
    background(255)
    world.run()
