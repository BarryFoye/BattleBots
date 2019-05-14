import random

# #Abstract interface that AI classes must comply to:
# class VehicleAI:
#     def GetTargetCoordinates(self, vehicle, world):
#         raise NotImplementedError()
    
#     def GetWorldDimensions(world):
#         return [world.width_, world.height_]
    
#     def __init__(self):
#         return self

#Vehicle wanders around the map with no real purpose or sense of direction
class WanderAI():
    
    def GetRandomPoint(world):
        [w,h] = super.GetWorldDimensions(world)
        x = random.random() * w
        y = random.random() * h
    
    def GetTargetCoordinates(self, vehicle, world):
        #return GetRandomPoint(world)
        return [0,0]
   
# #Vehicle is looking for food
# class ChaseFoodAI(VehicleAI):
#     def GetTargetCoordinates(self, vehicle, world):
#         raise NotImplementedError()


# #Vehicle is being chased by a predator
# class RunAwayAI(VehicleAI):
#     def GetTargetCoordinates(self, vehicle, world):
#         raise NotImplementedError()
