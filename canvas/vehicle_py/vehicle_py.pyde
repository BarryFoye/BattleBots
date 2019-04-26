import random

class vehicle:

    #Stuff that I still need
    world_height = 480
    world_width = 480
    
    #Configuration Variables
    size = 0
    max_speed = 0
    max_acceleration_rate = 0
    vision_radius = 0
    vision_awareness = 0
    carnivore = False
    faction = 0
    health_decay_per_tick = 1
    
    #State variables
    current_health = 0
    current_position = [0,0]
    current_speed = 0
    current_angle = 0
    
    #Constructor - called upon agent creation
    def __init__(self):
        #Initialise to a random position
        x = random.random() * self.world_width
        y = random.random() * self.world_height
        self.current_angle = random.random() * 2 * PI
        self.current_position = [x,y]
        #assume zero velocity
        self.current_speed = 0
    
    #update - called every tick
    def update():
        pass
    pass
        
    def show(self):
        draw_radius = 5
        fill(0)
        beginShape(TRIANGLES);
        bottom_left_corner_x = v.current_position[0] - draw_radius
        bottom_left_corner_y = v.current_position[1] - draw_radius 
        bottom_right_corner_x = v.current_position[0] + draw_radius
        bottom_right_corner_y = v.current_position[1] - draw_radius 
        top_vertex_x = v.current_position[0]
        top_vertex_y = v.current_position[1] + (1.5 * draw_radius)                 
        vertex(bottom_left_corner_x,bottom_left_corner_y)
        vertex(bottom_right_corner_x,bottom_right_corner_y)
        vertex(top_vertex_x,top_vertex_y)
        endShape();
        pass
        
        
v = vehicle()
    
#Processing calls 
def setup():
    size(480, 480)
    
def draw():
    background(255)
    v.show()
