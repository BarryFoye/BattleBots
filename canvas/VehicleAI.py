import random

#Abstract interface that AI classes must comply to:
class VehicleAI(object):
    
    current_target = PVector(200,200)
    
    def GetTargetCoordinates(self, vehicle, world):
        raise NotImplementedError()
    
    def GetDistanceToTarget(self,vehicle,current_target):
        return vehicle.current_position.dist(vehicle.current_target)
         
    def GetWorldDimensions(self, world):
        return(world.width_, world.height_)
   
##########################################################


class WanderAI(VehicleAI):
    #Vehicle wanders around the map with no real purpose or sense of direction. 
    
    def GetRandomPoint(self,world):
        [w,h] = super(WanderAI,self).GetWorldDimensions(world)
        x = random.random() * w
        y = random.random() * h
        return PVector(x,y)
    
    def Get_Current_Target(self, vehicle):
        if super(WanderAI,self).GetDistanceToTarget(vehicle,self.current_target) < 25:
            self.current_target = self.GetRandomPoint(vehicle.world)
        return self.current_target
    
    def Get_Next_AI_Mode(self,vehicle):
        #If there is food in sight move to ChaseFoodAI
        #IF there is a predator in sight move to RunAwayAI
        #If there is prey insight move to ChaseFoodAI
        #But, for now, just...
        return self
    
   
# #Vehicle is looking for food
# class ChaseFoodAI(VehicleAI):
#     def GetTargetCoordinates(self, vehicle, world):
#         raise NotImplementedError()


# #Vehicle is being chased by a predator
# class RunAwayAI(VehicleAI):
#     def GetTargetCoordinates(self, vehicle, world):
#         raise NotImplementedError()
