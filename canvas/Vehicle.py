import random
import VehicleAI
import copy
import pid as PID

class Vehicle:

    #reference to the world
    world = [ ]
    
    friction = 5
    
    #Configuration Variables
    mass = 5
    max_speed = 0
    max_acceleration_rate = 0
    max_angular_rate = 0.1
    max_thrust = 100
    vision_radius = 0
    vision_awareness = 0
    carnivore = False
    faction = 0
    health_decay_per_tick = 1
    border_size = 20
    
    #State variables
    current_ai = VehicleAI.WanderAI() 
    current_health = 0
    current_position = PVector(0.0,0.0)
    previous_position = PVector(0.0,0.0)
    current_angle = 3.14
    current_target = PVector(0.0,0.0)
    thrust_pid = []
    
    #Constructor - called upon agent creation
    def __init__(self, world):
        #Store dimensions of the world
        self.world = world
        #Initialise to a random position
        x = random.random() * self.world.width_
        y = random.random() * self.world.height_
        #self.current_angle = random.random() * 2 * PI
        self.current_position = PVector(x,y)
        self.previous_position = PVector(x,y)
        self.current_velocity = PVector(0.0,0.0)
        self.current_acceleration = PVector(0.0,0.0)
        self.current_target = PVector(0.0,0.0)
        self.max_speed = random.random() * 2
        self.max_acceleration_rate = random.random() * 2
        self.world = world
        self.ai = VehicleAI.WanderAI()    
        #set up thrust PID
        P = 0.5
        I = 0.5
        D= 0.0
        self.thrust_pid = PID.PID(P, I, D)  
        self.thrust_pid.SetPoint=0.0
        self.thrust_pid.setSampleTime(1)
    
    #update - called every tick
    def update(self):
        #
        #Run AI to work out where we want to go
        self.current_target = self.current_ai.Get_Current_Target(self)
        #
        #Paint the vehicle
        self.show()
        #
        #Work out engine power required
        thrust_required = self.calculate_thrust_required()
        println("At " + str( self.current_position) + " thrust: " + str(thrust_required)) # ", tgt: " + str(self.current_target) + " Proj dest: " + str(future_dist_to_target) + 
        #
        #println("Angle faced: " + str(self.current_angle * 180/PI) + " Angle travelling: " + str(self.calculate_effective_angle() * 180/PI) + " Slip angle: " + str(slip_angle * 180/PI))
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
        self.store_current_posn()
                   
    def store_current_posn(self):
        self.previous_position = PVector(self.current_position.x, self.current_position.y)
                   
    def calculate_rotation_required(self):
        effective_vector = PVector(self.current_position.y - self.previous_position.y, self.current_position.x - self.previous_position.x)
        #slip_angle = effective_angle - self.current_angle
        #current_angle = effective_angle#self.current_angle
        desired_angle = atan2((self.current_target.y - self.current_position.y),(self.current_target.x - self.current_position.x))
        desired_angle = desired_angle #- slip_angle
        #println("DesiredAngle: " + str(desired_angle) + " CurrentAngle: " + str(self.current_angle))
        return desired_angle -self.current_angle
    
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
        error_signal = self.current_position.dist(self.current_target) 
        self.thrust_pid.update(error_signal * -1)
        return self.thrust_pid.output
      
    def apply_thrust(self, thrust):
        #Using newton's second law F=ma. 
        #Asssume mass is proportional to size so bigger agents take more effort to turn and start/stop.
        #self.current_acceleration.add(thrust_vector.div(self.mass))
        effective_thrust_vector = PVector(0,thrust,0)
        effective_thrust_vector.rotate(self.current_angle - HALF_PI)
        self.current_acceleration.add(effective_thrust_vector)
        self.current_acceleration.normalize()
        self.current_acceleration.mult(self.max_acceleration_rate)
    
    def apply_acceleration(self):
        self.current_velocity.add(self.current_acceleration)
        if ((self.current_velocity.mag) > self.max_speed):
            self.current_velocity.normalize()
            self.current_velocity.mult(self.max_speed)

          
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
    
