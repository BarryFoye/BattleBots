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
    max_speed = 0.5
    max_acceleration_rate = 1.0
    max_angular_rate = 0.1
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
    current_angle = 3.14
    current_target = PVector(0.0,0.0)
    
    #Constructor - called upon agent creation
    def __init__(self, world):
        #Store dimensions of the world
        self.world = world
        #Initialise to a random position
        x = random.random() * self.world.width_
        y = random.random() * self.world.height_
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
        #
        #Paint the vehicle
        self.show()
        #
        #Work out engine power required
        thrust_required = self.calculate_thrust_required()
        #
        #Work out rotation required
        rotational_required = self.calculate_rotation_required()
        #
        #Steer and apply throttle
        self.apply_rotation(rotational_required)
        self.apply_thrust(thrust_required)
        #
        #Calculate the new position
        self.apply_acceleration()
        self.apply_velocity()
        #
        #Hard limits
        self.checkBorders()
        #
        #
                   
    def calculate_rotation_required(self):
        current_angle = self.current_angle
        desired_angle = atan2((self.current_target.y - self.current_position.y),(self.current_target.x - self.current_position.x))
        println("DesiredAngle: " + str(desired_angle) + " CurrentAngle: " + str(self.current_angle))
        return desired_angle - current_angle
    
    def apply_rotation(self,rotation_required):       
        if rotation_required > self.max_angular_rate:
            rotation = self.max_angular_rate
        elif rotation_required < (-1 * self.max_angular_rate):
            rotation = (-1 * self.max_angular_rate)
        else:
            rotation = rotation_required 
        self.add_angle(rotation)

    def add_angle(self,angle):
        self.current_angle += angle    
            
    def calculate_thrust_required(self):
        #PID controller for thrust
        p_gain  = 10
        i_gain = 0.0
        d_gain = 50
        lookahead = 10.0
        #Proportional
        error_signal = self.current_position.dist(self.current_target)     
        proportional_component = error_signal * p_gain
        #Differential
        u = copy.deepcopy(self.current_velocity)
        a = copy.deepcopy(self.current_acceleration)
        destination = self.current_position + (u.mult(lookahead))        
        future_dist_to_target = destination.dist(self.current_target)       
        derivitive_component = d_gain * (1/lookahead) * future_dist_to_target
        desired_thrust =  proportional_component - derivitive_component
        println("At " + str( self.current_position) + ", tgt: " + str(self.current_target) + " Proj dest: " + str(future_dist_to_target) + " thrust: " + str(desired_thrust))
        if desired_thrust > 8:
            return 8
        else:
            return desired_thrust    
    
    def apply_thrust(self, thrust):
        #Using newton's second law F=ma. 
        #Asssume mass is proportional to size so bigger agents take more effort to turn and start/stop.
        #self.current_acceleration.add(thrust_vector.div(self.mass))
        effective_thrust_vector = PVector(0,thrust,0)
        effective_thrust_vector.rotate(self.current_angle - HALF_PI)
        self.current_acceleration.add(effective_thrust_vector)
        #self.current_acceleration.limit(self.max_acceleration_rate)
    
    def apply_acceleration(self):
        self.current_velocity.add(self.current_acceleration)
        self.current_velocity.limit(self.max_speed)
    
    def apply_velocity(self):
        self.current_position.add(self.current_velocity)
    

    def checkBorders(self):
        #Handle the corders on the four sides
        if (self.current_position.x < self.border_size):
            self.current_position.x = self.border_size
        if (self.current_position.x > (self.world.width_-self.border_size)):
            self.current_position.x = (self.world.width_-self.border_size)
        if (self.current_position.y < self.border_size):
            self.current_position.y = self.border_size
        if (self.current_position.y > self.world.height_-self.border_size):
            self.current_position.y = self.world.height_-self.border_size
        pass
    
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
        rotate(self.current_angle + (0.5 * PI))
        beginShape(TRIANGLES);               
        vertex(bottom_left_corner_x,bottom_left_corner_y)
        vertex(bottom_right_corner_x,bottom_right_corner_y)
        vertex(top_vertex_x,top_vertex_y)
        endShape();        
        popMatrix();
        circle(self.current_target[0],self.current_target[1],20)
        
        pass
    
    
    
