import random

class Vehicle:

    #Supplied by the world
    world_height = 0
    world_width = 0
    
    #Configuration Variables
    size = 5
    max_speed = 0
    max_acceleration_rate = 0
    vision_radius = 0
    vision_awareness = 0
    carnivore = False
    faction = 0
    health_decay_per_tick = 1
    border_size = 20
    
    #State variables
    current_state = 'Wander'
    current_health = 0
    current_position = [float(0),float(0)]
    current_speed = 0
    current_angle = 0
    
    #Constructor - called upon agent creation
    def __init__(self, w, h):
        #Store dimensions of the world
        self.world_height = h
        self.world_width = w
        #Initialise to a random position
        x = random.random() * self.world_width
        y = random.random() * self.world_height
        self.current_angle = random.random() * 2 * PI
        self.current_position = [x,y]
        #assume zero velocity
        self.current_speed = 5.0
    
    #update - called every tick
    def update(self):
        self.show()
        self.advance_current_position()
    
    def advance_current_position(self):
        self.current_position[0] += (self.current_speed * cos(self.current_angle))
        self.current_position[1] += (self.current_speed * sin(self.current_angle))
        self.checkBorders()
    
    def checkBorders(self):
        if (self.current_position[0] < self.border_size):
            self.current_angle += PI
        if (self.current_position[0] > self.world_width-self.border_size):
            self.current_angle += PI
        if (self.current_position[1] < self.border_size) :
            self.current_angle += PI
        if (self.current_position[1] > self.world_height-self.border_size):
           self.current_angle += PI
        pass
    
    def show(self):
        bottom_left_corner_x = 0 - self.size
        bottom_left_corner_y = 0 - self.size 
        bottom_right_corner_x = 0 + self.size
        bottom_right_corner_y = 0 - self.size 
        top_vertex_x = 0
        top_vertex_y = 0 + (1.5 * self.size)          
        fill(0)
        pushMatrix();
        translate(self.current_position[0], self.current_position[1])
        compensation_factor = 0 - (PI/2)
        # We add a 90 degree rotation because Processing takes 0 degrees to be EAST
        # whereas the triangle is drawn as if 0 degrees is NORTH i.e. pointing upwards
        rotate(self.current_angle + compensation_factor)
        beginShape(TRIANGLES);               
        vertex(bottom_left_corner_x,bottom_left_corner_y)
        vertex(bottom_right_corner_x,bottom_right_corner_y)
        vertex(top_vertex_x,top_vertex_y)
        endShape();
        popMatrix();
        
        pass
    
