import random
import VehicleAI
import copy

class Vehicle:

    #reference to the world
    world = [ ]

    #Supplied by the world
    world_height = 0
    world_width = 0
    
    #Configuration Variables
    mass = 5
    max_speed = 5.0
    max_acceleration_rate = 1.0
    max_angular_rate = 5
    vision_radius = 0
    vision_awareness = 0
    carnivore = False
    faction = 0
    health_decay_per_tick = 1
    border_size = 20
    
    #State variables
    current_ai =  [ ]
    current_health = 0
    current_position = PVector(0.0,0.0)
    current_speed = 0
    current_angle = 0
    current_target = PVector(0.0,0.0)
    
    #Constructor - called upon agent creation
    def __init__(self, world):
        #Store dimensions of the world
        self.world = world
        #Initialise to a random position
        #x = random.random() * self.world.width_
        #y = random.random() * self.world.height_
        x = 100.0
        y = 100.0
        #self.current_angle = random.random() * 2 * PI
        self.current_position = PVector(x,y)
        self.current_velocity = PVector(0.0,0.0)
        self.current_acceleration = PVector(0.0,0.0)
        self.current_target = PVector(0.0,0.0)
        self.world = world
        #####
        mid_x = 0.5 * self.world.width_
        mid_y = 0.5 * self.world.height_  
        self.current_target = PVector(mid_x, mid_y)
        
    
    #update - called every tick
    def update(self):
        self.show()        
        #desired_angle = self.calc_desired_angle(self.current_position, self.current_target)        
        #self.current_angle = self.increment_angle(self.current_angle, desired_angle, self.max_angular_rate)
        #println("DesiredAngle: " + str(desired_angle) + " CurrentAngle: " + str(self.current_angle))
        force_required = self.calculate_force_required()
        self.apply_force(force_required)
        self.apply_acceleration()
        self.apply_velocity()
        #self.checkBorders()
    
    def calculate_force_required(self):
        #PID controller for thrust
        p_gain  = 10
        i_gain = 0.0
        d_gain = 50
        lookahead = 10.0
        #Proportional
        error_signal = copy.deepcopy(self.current_target)
        error_signal.sub(self.current_position)      
        proportional_component = error_signal * p_gain
        #Differential
        u = copy.deepcopy(self.current_velocity)
        a = copy.deepcopy(self.current_acceleration)
        destination = self.current_position + (u.mult(lookahead))
        destination.sub(self.current_target)
        derivitive_component = d_gain * (1/lookahead) * destination
        end_vector = PVector(0.0,0.0)
        PVector.sub(proportional_component,derivitive_component,end_vector) 
        end_vector.limit(8)
        println("At " + str( self.current_position) + ", tgt: " + str(self.current_target) + " Proj dest: " + str(destination) + " Force vector: " + str(end_vector))
        return end_vector
    
    def apply_force(self, force_vector):
        #Using newton's second law F=ma. 
        #Asssume mass is proportional to size so bigger agents take more effort to turn and start/stop.
        #self.current_acceleration.add(force_vector.div(self.mass))
        self.current_acceleration.add(force_vector)
        #self.current_acceleration.limit(self.max_acceleration_rate)
    
    def apply_acceleration(self):
        self.current_velocity.add(self.current_acceleration)
        self.current_velocity.limit(self.max_speed)
    
    def apply_velocity(self):
        self.current_position.add(self.current_velocity)
    
    # def increment_current_position(self,current_position,angle,speed):
    #     x = current_position[0]
    #     x += speed * cos(angle)
    #     y = current_position[1]
    #     y += speed * sin(angle)
    #     return [x,y]       
    
    # def calc_desired_angle(self, current_position, target_position):
    #       v1 = PVector(current_position[0], current_position[1])
    #       v2 = PVector(target_position[0],target_position[1])
    #       return (PVector.angleBetween(v1, v2))
    
    # def increment_angle(self, current_angle, desired_angle, max_angular_rate):
    #     angular_adjustment = desired_angle - current_angle
    #     if (abs(angular_adjustment)) > max_angular_rate:
    #         if (angular_adjustment < 0):
    #             return current_angle - max_angular_rate
    #         else:
    #             return current_angle + max_angular_rate
    #         pass
    #     else:
    #         return desired_angle
    
    # def checkBorders(self):
    #     #handle the four extreme corners
    #     if ((self.current_position[0] < self.border_size) and (self.current_position[1] < self.border_size)):
    #         self.current_angle += (1.0/2.0) * PI
    #     elif ((self.current_position[0] < self.border_size) and (self.current_position[1] > self.world_width-self.border_size)):
    #         self.current_angle += (1.0/2.0) * PI
    #     elif ((self.current_position[0] > self.world_width-self.border_size) and (self.current_position[1] < self.border_size)):
    #         self.current_angle += (1.0/2.0) * PI
    #     elif ((self.current_position[0] > self.world_width-self.border_size) and (self.current_position[1] > self.world_width-self.border_size)):
    #         self.current_angle += (1.0/2.0) * PI
            
    #     #Handle the corders on the four sides
    #     elif (self.current_position[0] < self.border_size):
    #         self.current_angle += (1.0/4.0) * PI
    #     elif (self.current_position[0] > self.world_width-self.border_size):
    #         self.current_angle += (3.0/4.0) * PI
    #     elif (self.current_position[1] < self.border_size) :
    #         self.current_angle += (1.0/4.0) * PI
    #     elif (self.current_position[1] > self.world_height-self.border_size):
    #        self.current_angle += (3.0/4.0) * PI
    #     pass
    
    def show(self):
        bottom_left_corner_x = 0 - self.mass
        bottom_left_corner_y = 0 + self.mass 
        bottom_right_corner_x = 0 + self.mass
        bottom_right_corner_y = 0 + self.mass 
        top_vertex_x = 0
        top_vertex_y = 0 - (1.5 * self.mass)          
        fill(0)
        pushMatrix();
        translate(self.current_position[0], self.current_position[1])
        # We add a 90 degree rotation because Processing takes 0 degrees to be EAST
        # whereas the triangle is drawn as if 0 degrees is NORTH i.e. pointing upwards
        rotate(self.current_angle)
        beginShape(TRIANGLES);               
        vertex(bottom_left_corner_x,bottom_left_corner_y)
        vertex(bottom_right_corner_x,bottom_right_corner_y)
        vertex(top_vertex_x,top_vertex_y)
        endShape();
        popMatrix();
        
        pass
    
    
    
